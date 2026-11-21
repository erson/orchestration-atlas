#!/usr/bin/env python3
"""Fetch GitHub metrics for every project in data/projects.json, then render README.md and data/projects.csv.

Needs the GitHub CLI (gh), signed in with read access to public repositories. Repository data comes from the
GraphQL API in batches; contributors come from the REST API, because GraphQL does not expose them.

    python3 scripts/update.py                 fetch metrics older than 7 days, then render
    python3 scripts/update.py --spread        also fetch the oldest records, about a seventh of the index per run
    python3 scripts/update.py --refresh       fetch every project again, then render
    python3 scripts/update.py --render-only   render from data/metrics.json, no network calls
    python3 scripts/update.py --only a/b c/d  fetch only these projects (always fresh), then render
    python3 scripts/update.py --discover      search GitHub for new projects, write data/candidates.json
    python3 scripts/update.py --check         validate the data files; writes nothing, no network calls
"""

import argparse
import concurrent.futures as cf
import csv
import html
import io
import json
import os
import re
import statistics
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

if __package__:
    from . import discovery_stats, history, readme_editor
else:
    import discovery_stats
    import history
    import readme_editor

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_FILE = ROOT / "data" / "projects.json"
METRICS_FILE = ROOT / "data" / "metrics.json"
CSV_FILE = ROOT / "data" / "projects.csv"
FEATURES_FILE = ROOT / "data" / "features.json"
DISCOVERY_FILE = ROOT / "data" / "discovery.json"
DISCOVERY_STATS_FILE = ROOT / "data" / "discovery-stats.json"
DISCOVERY_STATE_FILE = ROOT / "data" / "discovery-state.json"
CANDIDATES_FILE = ROOT / "data" / "candidates.json"
README_FILE = ROOT / "README.md"

NOW = datetime.now(timezone.utc)
TODAY = NOW.date()
MAX_AGE = timedelta(days=7)               # repository metrics
CONTRIBUTORS_MAX_AGE = timedelta(days=30)  # REST contributor lists change slowly and cost the most calls
SPREAD_DAYS = 7                            # --spread: each run fetches at least 1/SPREAD_DAYS of the projects
SPREAD_MIN_AGE = timedelta(hours=12)       # --spread never picks a record fetched more recently than this
GH_TIMEOUT = 120                           # seconds before a hanging `gh api` call is abandoned
BATCH = 20                                 # repositories per GraphQL query; halved when GitHub times out
README_BATCH = 10
README_CHARS = 60_000
README_PATHS = ["README.md", "readme.md", "Readme.md", "README.MD", "README.markdown", "README.rst",
                "README.txt", "README", "docs/README.md"]
RELEASE_PAGES = 20                         # at most 2,000 releases read per repository
REST_WORKERS = 2                           # GitHub asks clients to avoid concurrent requests; keep this small
RESERVE = 100                              # pause when fewer calls or points than this are left
TRANSIENT = {500, 502, 503, 504}           # retried; a failure keeps the previous snapshot
GONE = {404, 410, 451}                     # the repository no longer exists or is blocked
GAP_FIELDS = {
    "contributors": ["contributors", "bots", "top_author_share", "contributors_fetched_at"],
    "releases": ["latest_release_tag", "latest_release_at", "latest_release_prerelease", "releases_12m",
                 "releases_12m_capped"],
    "readme": ["features", "readme_found"],
}
STATUSES = ["Active", "Recent", "Slow", "Stale", "Archived", "Unavailable", "Not fetched"]
STATUS_ICON = {"Active": "🟢", "Recent": "🟡", "Slow": "🟠", "Stale": "🔴", "Archived": "📦", "Unavailable": "⚫",
               "Not fetched": "⚪"}
SHORT = {
    "terminal": "Terminal",
    "desktop": "Desktop & web",
    "swarms": "Swarms",
    "loops": "Loop runners",
    "tasks": "Task runners",
    "infra": "Infrastructure",
    "assistants": "Assistants",
    "resting": "Resting",
    "adjacent": "Adjacent frameworks",
}
CSV_FIELDS = [
    "repo", "name", "category", "origin", "status", "stars", "forks",
    "contributors", "bots", "top_author_share", "commits_90d", "commits_all_time",
    "last_commit_at", "days_since_commit", "created_at", "age_months", "stars_per_month",
    "latest_release_tag", "latest_release_at", "releases_12m", "open_issues", "open_prs",
    "license", "language", "languages", "features", "homepage", "archived", "topics", "url", "description",
]
TITLE = "Orchestration Atlas"
INTRO = (
    "Before you write another orchestrator, check whether someone already has. This repo indexes "
    "{total} open-source and source-available tools that run, supervise, or coordinate AI agents: "
    "parallel coding agents, multi-agent swarms, loop and task runners, infrastructure, and personal assistants. "
    "{active} of them had a commit in the last 30 days.\n\n"
    "Most of these projects are doing the same few things: running several agent sessions side by side, "
    "isolating them in worktrees or containers, and routing tasks between them. The gap is rarely another "
    "orchestrator. It is maturity: more contributors, releases, docs, and tests. Pick one that is close to "
    "what you need and contribute to it, or fork it. If you still build your own, use this list to see what "
    "already exists and say what yours does differently.\n\n"
    "Every project has live GitHub metrics: stars, contributors, commit activity, releases, open work, license, "
    "languages, and how recently it was updated, plus the agents, isolation, and interfaces its README mentions. "
    "The [Single-maintainer risk](#single-maintainer-risk) table shows projects that depend on one person. "
    "Figures are a snapshot; see [Methodology](#methodology)."
)
METHOD = """## Methodology

**Source.** Projects start from [andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators) (CC0-1.0). Projects marked _(new)_ were found by GitHub search, the source's own references, and web search, and were not in that list. Each new project had to meet the same scope: it orchestrates, supervises, or coordinates several AI agents or agent sessions; it is open source or source-available; and it is active. Adjacent frameworks are general-purpose agent SDKs. They are listed separately because many teams use them for multi-agent orchestration. New candidates are found with saved GitHub searches (`data/discovery.json`) and reviewed by hand before they are added.

**Data.** GitHub GraphQL API for repository metadata, commits, releases, issues, pull requests, languages, and READMEs; GitHub REST API for contributors, which GraphQL does not expose. Both go through the GitHub CLI, collected on the date shown above (UTC). Repository figures refer to the default branch. Statuses and day counts are judged as of each project's collection date. Contributor lists are refreshed every 30 days, other figures every 7. The daily run fetches about a seventh of the projects, oldest first, so collection dates within one snapshot differ by up to a week.

| Column | Definition |
|---|---|
| Stars, Forks | Repository metadata. |
| Language | Share of the repository's code by bytes, as GitHub's linguist detects it. Languages under 5% are left out of the tables. |
| Features | Agents, isolation, interfaces, protocols, and workflow features found by keyword in the README, the GitHub description, and topics (`data/features.json`). It is a heuristic: a passing mention also counts, and a feature the README does not name is missed. |
| License | The SPDX id GitHub detects. Check the license file before reuse; detection can be wrong. "None" means no license was detected, so default copyright applies. |
| Contributors | GitHub accounts (type `User`) with at least one commit on the default branch. Bots are excluded and counted separately in `data/metrics.json`. |
| Commits (90d) | Commits on the default branch in the 90 days before the snapshot. |
| Last commit | Committer date of the newest default-branch commit. `pushed_at` is not used, because it also changes when other branches are pushed. |
| Status | 🟢 **Active**: last commit within 30 days. 🟡 **Recent**: 31 to 90 days. 🟠 **Slow**: 91 to 365 days. 🔴 **Stale**: older than a year, or no commits. 📦 **Archived**: archived on GitHub. ⚫ **Unavailable**: the repository no longer exists, or the API call failed and there is no earlier snapshot. Unavailable projects are excluded from the available-project count. When a fetch fails temporarily, the previous snapshot is kept. |
| Latest release | Newest non-draft GitHub Release, pre-releases included. Projects that only push tags show "—". |
| Open and closed issues | Aggregate GitHub issue totals. Pull requests are counted separately. |
| Issue responsiveness | Rotating sample, targeting a two-day refresh when budget permits, of up to six external human reports aged 7–90 days among the 30 newest issues, and up to six recent closures among the 30 most recently updated closed issues. Reports are spread across each eligible list. Only replies by a human owner, member, or collaborator other than the reporter count. We read metadata for the first five comments. Truncated threads with an unresolved seven-day window are unknown. Timing medians require three observations. Closed as completed is the maintainer’s recorded reason. |

**Also in `data/projects.csv`.** Top-author share (the top human contributor's share of human contributions; values near 100% mean one person does almost all of the work), commits across all time on the default branch, releases in the last 12 months, stars per month since creation, age in months, every detected language with its share, and the detected features. A value that starts with `=`, `+`, `-`, or `@` (some release tags do) carries a leading apostrophe, so a spreadsheet does not run it as a formula.

**Limitations.** Stars are a popularity signal, not a quality measure, and can be inflated. Contributor counts cover GitHub accounts only, so commits made under unlinked emails are not counted. Feature detection reads text, not code. Stale does not mean unusable; many small tools are finished. All figures are a point-in-time snapshot.
"""
MAINTAIN = """## Keeping it current

```sh
python3 scripts/update.py                # fetch metrics older than 7 days, then re-render
python3 scripts/update.py --spread       # also fetch the oldest seventh, to even out daily runs
python3 scripts/update.py --refresh      # fetch everything again
python3 scripts/update.py --only a/b    # fetch these projects now, then re-render
python3 scripts/update.py --render-only  # rebuild this README from data/metrics.json
python3 scripts/update.py --discover     # search GitHub for new projects; results go to data/candidates.json
python3 scripts/update.py --check        # validate the data files without writing anything
```

The script needs the GitHub CLI (`gh`) signed in. It runs GraphQL queries one at a time, and waits when GitHub's rate limits run low. To add a project, append an entry to `data/projects.json` with `repo`, `name`, `category`, `origin`, and `description`, then run the script. To stop a reviewed candidate from coming back, add it to `rejected` in `data/discovery.json`. Feature keywords live in `data/features.json`.

A GitHub Actions workflow (`.github/workflows/update.yml`) refreshes about a seventh of the projects every day (`--spread`) and commits the result. Every Monday it runs discovery and rewrites the open issue labelled `candidates` with the projects to review. Projects that moved or disappeared are listed in the issue labelled `maintenance`. The Monday discovery summary also counts moved, unavailable, and archived repositories using the latest daily snapshots. The daily job summary shows successful refreshes, seven-day coverage, and the age of the oldest snapshot. Weekly discovery resumes interrupted searches and samples older, recently active repositories once a month within the same eight-minute budget. The candidates issue lists new finds first and shows each candidate’s matching searches, evidence, and last observation. The discovery summary counts candidates found by each query, candidates found only by that query, and review outcomes. A weekly one-page README search and a monthly rotating search share the existing discovery budget. Acceptance rates use reviewed candidates only. Historical results cover the query matches still present when tracking began. Before pushing, the bot validates the generated files against the local cache. Pull requests that touch the data, script, or workflows run offline validation and show a README and CSV preview in the job summary.

After successful Monday discovery, the README editor uses ZenMux to select and arrange verified findings for the weekly brief. The editor runs in the `Orchestrate` environment with `ZENMUX_API_KEY`. DeepSeek is the primary model and HY4 is the provider fallback. The editor sends at most 24 short facts in one request with a 512-token output limit. Daily renders reuse the last published brief. The editor can also switch the index snapshot between the Spec and Stat Markdown designs from [MDXCN](https://www.mdxcn.dev/docs).
"""
CREDITS = """## Credits

The starting list, its categories, and its one-line descriptions come from [andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators), released under CC0-1.0. The descriptions here are shortened rewrites; the originals are kept in `data/projects.json` as `list_description`.

The list starts from [andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators) (CC0-1.0) and adds projects that list does not cover.
"""

REPO_FIELDS = """
  nameWithOwner url description homepageUrl stargazerCount forkCount isArchived isFork createdAt pushedAt
  licenseInfo { spdxId }
  primaryLanguage { name }
  languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { totalSize edges { size node { name } } }
  repositoryTopics(first: 20) { nodes { topic { name } } }
  issues(states: OPEN) { totalCount }
  closedIssues: issues(states: CLOSED) { totalCount }
  pullRequests(states: OPEN) { totalCount }
  releases(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
    pageInfo { hasNextPage endCursor }
    nodes { tagName publishedAt createdAt isDraft isPrerelease }
  }
  defaultBranchRef { target { ... on Commit {
    committedDate
    recent: history(since: $since) { totalCount }
    all: history { totalCount }
  } } }
"""
RELEASES_QUERY = """
query($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    releases(first: 100, after: $after, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes { tagName publishedAt createdAt isDraft isPrerelease }
    }
  }
}
"""
SEARCH_QUERY = """
query($q: String!, $after: String) {
  search(query: $q, type: REPOSITORY, first: 50, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes { ... on Repository {
      nameWithOwner url description stargazerCount createdAt pushedAt isFork isArchived
      primaryLanguage { name }
      repositoryTopics(first: 20) { nodes { topic { name } } }
    } }
  }
}
"""


# --- GitHub access ---------------------------------------------------------------------------------------------

class GhError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


class BudgetExceeded(Exception):
    """The run reached its time budget (--max-minutes). Work stops; what was fetched is kept."""


class Stopped(Exception):
    """Fetching gave up (circuit breaker). What was fetched is kept and rendered; the run then exits non-zero."""


DEADLINE = None          # time.monotonic() value after which no new work starts; set by --max-minutes
MAX_REST_PAGES = 50      # contributor lists are capped by GitHub anyway; this guards against a pagination loop
MAX_FAILED_BATCHES = 3   # consecutive batches where every repository failed: stop instead of retrying forever


def check_budget(extra=0):
    if DEADLINE is not None and time.monotonic() + extra > DEADLINE:
        raise BudgetExceeded()


def gh_once(args, stdin=None):
    """Run `gh api --include` once and return (status, lower-cased headers, body). Status is None without a response."""
    timeout = GH_TIMEOUT
    if DEADLINE is not None:
        timeout = min(timeout, DEADLINE - time.monotonic())
        if timeout <= 0:
            raise BudgetExceeded()
    try:
        proc = subprocess.run(["gh", "api", "--include", *args], input=stdin, capture_output=True, text=True,
                              timeout=timeout)
    except subprocess.TimeoutExpired:   # a hung call must not outlive the time budget
        check_budget()
        return None, {}, f"gh api did not answer within {GH_TIMEOUT} seconds"
    if not proc.stdout.startswith("HTTP/"):
        return None, {}, proc.stderr.strip()
    head, *rest = re.split(r"\r?\n\r?\n", proc.stdout, maxsplit=1)
    lines = head.splitlines()
    status = int(lines[0].split()[1])
    headers = {}
    for line in lines[1:]:
        key, sep, value = line.partition(":")
        if sep:
            headers[key.strip().lower()] = value.strip()
    return status, headers, rest[0] if rest else ""


def _int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def pause(seconds, why):
    seconds = min(max(seconds, 1), 3700)
    check_budget(seconds)   # never start a wait that would run past the time budget
    if seconds >= 30:
        print(f"  {why}; waiting {seconds / 60:.1f} min", flush=True)
    time.sleep(seconds)


def call(args, stdin=None, retry_transient=True):
    """One API request with GitHub's rate-limit rules applied.

    Primary limit: when `x-ratelimit-remaining` is 0, wait until `x-ratelimit-reset`. Secondary limit: honour
    `retry-after`, otherwise wait at least a minute with exponential backoff. Before returning, pause if fewer
    than RESERVE calls or points are left, so the next request does not hit the limit."""
    for attempt in range(6):
        status, headers, body = gh_once(args, stdin)
        remaining = _int(headers.get("x-ratelimit-remaining"), None)
        reset = _int(headers.get("x-ratelimit-reset"), 0)
        if status is None:
            if attempt < 3:
                check_budget(3 * 2 ** attempt)
                time.sleep(3 * 2 ** attempt)
                continue
            raise GhError(None, body)
        limited = (status in (403, 429) and ("rate limit" in body.lower() or "retry-after" in headers or remaining == 0)) \
            or (status == 200 and '"type":"RATE_LIMITED"' in body.replace(" ", ""))
        if limited:
            if "retry-after" in headers:
                pause(_int(headers["retry-after"], 60) + 1, "secondary rate limit")
            elif remaining == 0:
                pause(reset - time.time() + 5, f"{headers.get('x-ratelimit-resource', 'API')} rate limit reached")
            else:
                pause(60 * 2 ** min(attempt, 3), "secondary rate limit")
            continue
        if status in TRANSIENT and retry_transient and attempt < 3:
            check_budget(3 * 2 ** attempt)
            time.sleep(3 * 2 ** attempt)
            continue
        if remaining is not None and remaining < RESERVE:
            pause(reset - time.time() + 5, f"only {remaining} {headers.get('x-ratelimit-resource', 'API')} calls left")
        return status, headers, body
    raise GhError(429, "rate limit persisted")


def graphql(query, variables, retry_transient=True):
    """Run a GraphQL query. Returns (data, errors); GitHub reports per-alias errors next to partial data."""
    status, _, body = call(["graphql", "--input", "-"], json.dumps({"query": query, "variables": variables}),
                           retry_transient)
    if status != 200:
        raise GhError(status, body[:300])
    try:
        doc = json.loads(body)
    except json.JSONDecodeError as err:
        raise GhError(None, f"bad GraphQL response: {err}") from err
    return doc.get("data") or {}, doc.get("errors") or []


def rest_pages(endpoint):
    """Yield the JSON items of a paginated REST endpoint, following the Link header."""
    url = endpoint
    for _ in range(MAX_REST_PAGES):
        if not url:
            return
        status, headers, body = call([url])
        if status == 204:
            return
        if status != 200:
            raise GhError(status, body[:300])
        yield from json.loads(body)
        found = re.search(r'<https://api\.github\.com/([^>]+)>;\s*rel="next"', headers.get("link", ""))
        url = found.group(1) if found else None


def rate_status():
    status, _, body = call(["rate_limit"])
    if status != 200:
        raise GhError(status, body[:300])
    res = json.loads(body)["resources"]
    return res["core"]["remaining"], res["graphql"]["remaining"]


def parse_ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def split_repo(repo):
    owner, _, name = repo.partition("/")
    return owner, name


# --- Features ----------------------------------------------------------------------------------------------------

def load_features():
    """Compile data/features.json into [(group, label, regex)], keeping the file's order."""
    groups = json.loads(FEATURES_FILE.read_text(encoding="utf-8"))["groups"]
    return [(group, label, re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE))
            for group, labels in groups.items() for label, patterns in labels.items()]


def detect_features(compiled, *texts):
    """Labels whose keywords appear in any of the texts, in the order of data/features.json."""
    blob = "\n".join(t for t in texts if t)
    return [label for _, label, regex in compiled if regex.search(blob)]


# --- Fetching ----------------------------------------------------------------------------------------------------

def error_record(repo, code, message):
    return {"repo": repo, "fetched_at": NOW.isoformat(timespec="seconds"), "error": code,
            "error_message": (message or "")[:300]}


def published(nodes):
    return [r for r in nodes if r and not r.get("isDraft") and r.get("publishedAt")]


def record_from_graphql(repo, g):
    """Map one GraphQL repository object to the fields stored in data/metrics.json."""
    target = (g.get("defaultBranchRef") or {}).get("target") or {}
    langs = g.get("languages") or {}
    total = langs.get("totalSize") or 0
    record = {
        "repo": repo,
        "fetched_at": NOW.isoformat(timespec="seconds"),
        "full_name": g["nameWithOwner"],
        "url": g["url"],
        "github_description": g.get("description") or "",
        "homepage": g.get("homepageUrl") or "",
        "stars": g["stargazerCount"],
        "forks": g["forkCount"],
        "archived": g["isArchived"],
        "fork": g["isFork"],
        "created_at": g["createdAt"],
        "pushed_at": g["pushedAt"],
        "license": (g.get("licenseInfo") or {}).get("spdxId") or "",
        "language": (g.get("primaryLanguage") or {}).get("name") or "",
        "languages": [{"name": e["node"]["name"], "share": round(e["size"] / total, 3)}
                      for e in langs.get("edges") or []] if total else [],
        "topics": [n["topic"]["name"] for n in (g.get("repositoryTopics") or {}).get("nodes") or []],
        "open_issues": g["issues"]["totalCount"],
        "closed_issues": g["closedIssues"]["totalCount"],
        "open_prs": g["pullRequests"]["totalCount"],
        "last_commit_at": target.get("committedDate"),
        "commits_90d": (target.get("recent") or {}).get("totalCount", 0),
        "commits_all_time": (target.get("all") or {}).get("totalCount", 0),
    }
    rel = g.get("releases") or {}
    record["_releases"] = published(rel.get("nodes") or [])
    record["_release_cursor"] = rel["pageInfo"]["endCursor"] if (rel.get("pageInfo") or {}).get("hasNextPage") else None
    record["_release_oldest"] = min((r["createdAt"] for r in rel.get("nodes") or [] if r and r.get("createdAt")),
                                    default=None)
    return record


def batch_query(repos):
    params = ["$since: GitTimestamp!"]
    parts = []
    variables = {"since": (NOW - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")}
    for i, repo in enumerate(repos):
        owner, name = split_repo(repo)
        params += [f"$o{i}: String!", f"$n{i}: String!"]
        variables[f"o{i}"], variables[f"n{i}"] = owner, name
        parts.append(f"r{i}: repository(owner: $o{i}, name: $n{i}) {{ {REPO_FIELDS} }}")
    return f"query({', '.join(params)}) {{\n" + "\n".join(parts) + "\n}", variables


def fetch_batch(repos):
    """Fetch metadata for several repositories in one GraphQL query. When GitHub times out, split the batch."""
    query, variables = batch_query(repos)
    try:
        data, errors = graphql(query, variables, retry_transient=len(repos) == 1)
    except GhError as err:
        if len(repos) > 1 and (err.code in TRANSIENT or err.code is None):
            mid = len(repos) // 2
            return {**fetch_batch(repos[:mid]), **fetch_batch(repos[mid:])}
        return {repo: error_record(repo, err.code or "unknown", err.message) for repo in repos}
    by_alias = {}
    for e in errors:
        path = e.get("path") or []
        if path:
            by_alias.setdefault(path[0], e)
    out = {}
    for i, repo in enumerate(repos):
        g = data.get(f"r{i}")
        if g:
            out[repo] = record_from_graphql(repo, g)
            continue
        e = by_alias.get(f"r{i}") or (errors[0] if errors else {})
        code = 404 if e.get("type") == "NOT_FOUND" else "graphql"
        out[repo] = error_record(repo, code, e.get("message", "no data returned"))
    return out


def finish_releases(record):
    """Read further release pages while they still fall inside the last 12 months, then summarise releases."""
    cutoff = NOW - timedelta(days=365)
    releases = record.pop("_releases")
    cursor = record.pop("_release_cursor")
    oldest = record.pop("_release_oldest")
    pages, capped = 1, False
    owner, name = split_repo(record["full_name"])
    while cursor and oldest and parse_ts(oldest) >= cutoff:
        if pages >= RELEASE_PAGES:
            capped = True
            break
        data, errors = graphql(RELEASES_QUERY, {"owner": owner, "name": name, "after": cursor})
        rel = (data.get("repository") or {}).get("releases")
        if not rel:
            raise GhError("graphql", (errors[0] if errors else {}).get("message", "no releases returned"))
        nodes = rel.get("nodes") or []
        releases += published(nodes)
        oldest = min((r["createdAt"] for r in nodes if r and r.get("createdAt")), default=None)
        cursor = rel["pageInfo"]["endCursor"] if rel["pageInfo"]["hasNextPage"] else None
        pages += 1
    if releases:
        newest = max(releases, key=lambda r: r["publishedAt"])
        record.update(latest_release_tag=newest["tagName"], latest_release_at=newest["publishedAt"],
                      latest_release_prerelease=newest["isPrerelease"])
    record["releases_12m"] = sum(parse_ts(r["publishedAt"]) >= cutoff for r in releases)
    if capped:
        record["releases_12m_capped"] = True


def fetch_readmes(full_names):
    """Return {full_name: README text or None}, trying the usual README file names. Splits on timeouts."""
    if not full_names:
        return {}
    params, parts, variables = [], [], {}
    lookups = " ".join(f'p{j}: object(expression: "HEAD:{path}") {{ ... on Blob {{ text }} }}'
                       for j, path in enumerate(README_PATHS))
    for i, full in enumerate(full_names):
        owner, name = split_repo(full)
        params += [f"$o{i}: String!", f"$n{i}: String!"]
        variables[f"o{i}"], variables[f"n{i}"] = owner, name
        parts.append(f"r{i}: repository(owner: $o{i}, name: $n{i}) {{ {lookups} }}")
    query = f"query({', '.join(params)}) {{\n" + "\n".join(parts) + "\n}"
    try:
        data, _ = graphql(query, variables, retry_transient=len(full_names) == 1)
    except GhError as err:
        if len(full_names) > 1 and (err.code in TRANSIENT or err.code is None):
            mid = len(full_names) // 2
            return {**fetch_readmes(full_names[:mid]), **fetch_readmes(full_names[mid:])}
        raise
    out = {}
    for i, full in enumerate(full_names):
        repo = data.get(f"r{i}") or {}
        text = next((repo[f"p{j}"]["text"] for j in range(len(README_PATHS))
                     if (repo.get(f"p{j}") or {}).get("text")), None)
        out[full] = text[:README_CHARS] if text else None
    return out


def fetch_contributors(full_name):
    pairs = [(c.get("type"), c.get("contributions", 0)) for c in rest_pages(f"repos/{full_name}/contributors?per_page=100")]
    humans = [n for kind, n in pairs if kind == "User"]
    return {
        "contributors": len(humans),
        "bots": sum(kind == "Bot" for kind, _ in pairs),
        "top_author_share": round(max(humans) / sum(humans), 3) if humans and sum(humans) else None,
        "contributors_fetched_at": NOW.isoformat(timespec="seconds"),
    }


def contributors_due(old, refresh):
    if refresh or not old or old.get("error") or old.get("contributors") is None:
        return True
    stamp = old.get("contributors_fetched_at") or old.get("fetched_at")
    return parse_ts(stamp) < NOW - CONTRIBUTORS_MAX_AGE


def needs_fetch(cached, refresh):
    if refresh or cached is None or cached.get("last_error"):
        return True
    if cached.get("error"):
        # A repository that is gone is checked again on the normal schedule; other failures are retried every run.
        return cached["error"] not in GONE or parse_ts(cached["fetched_at"]) < NOW - MAX_AGE
    if "languages" not in cached:   # written before languages and features were collected
        return True
    return parse_ts(cached["fetched_at"]) < NOW - MAX_AGE


def select_targets(projects, cache, refresh, spread):
    """Repos to fetch now: everything that is due, plus (with spread) the oldest other records up to the quota.

    Without spread, records fetched on the same day all fall due on the same day, so one run in seven does all
    the work. With spread every run takes the oldest seventh, which keeps each run small and inside the API limits."""
    todo = [p["repo"] for p in projects if needs_fetch(cache.get(p["repo"].lower()), refresh)]
    if not spread:
        return todo
    quota = -(-len(projects) // SPREAD_DAYS)
    due = set(todo)
    rest = sorted((cache[p["repo"].lower()]["fetched_at"], p["repo"]) for p in projects if p["repo"] not in due)
    extra = [repo for stamp, repo in rest if parse_ts(stamp) <= NOW - SPREAD_MIN_AGE]
    return todo + extra[:max(quota - len(todo), 0)]


def merge_record(old, new):
    """Combine a fresh fetch with the cached record.

    A repository that is gone replaces the cache. A temporary failure keeps the previous snapshot and notes the
    error, so a 502 or a rate limit does not wipe a project's metrics. Fields a step failed to return are
    carried over from the previous snapshot."""
    usable = old if old and not old.get("error") else None
    if new.get("error"):
        if new["error"] in GONE or usable is None:
            return new
        kept = {k: v for k, v in usable.items() if not k.startswith("last_error")}
        return {**kept, "last_error": new["error"], "last_error_message": new.get("error_message", ""),
                "last_error_at": new["fetched_at"]}
    if usable:
        for gap in new.get("gaps", []):
            for key in GAP_FIELDS.get(gap.split(":")[0], []):
                if key not in new and key in usable:
                    new[key] = usable[key]
        if new.get("contributors") is not None and not new.get("contributors_fetched_at"):
            new["contributors_fetched_at"] = usable.get("fetched_at")   # see enrich(): keep the list ageing
    return new


def write_atomic(path, text):
    """Write to a temporary file, then rename it, so an interrupted run never leaves a truncated file."""
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    os.replace(tmp, path)


def save_metrics(cache):
    payload = {"generated_at": NOW.isoformat(timespec="seconds"), "repos": cache}
    write_atomic(METRICS_FILE, json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def preflight():
    try:
        core, points = rate_status()
    except GhError as err:
        sys.exit(f"cannot reach the GitHub API through gh; run `gh auth status`.\n{err.message}")
    print(f"  GraphQL points left this hour: {points:,} · REST calls left: {core:,}", flush=True)


def enrich(records, cache, refresh, features):
    """Add releases, README features, and contributors to freshly fetched records, in place."""
    ok = [r for r in records if not r.get("error")]
    for record in ok:
        try:
            finish_releases(record)
        except GhError as err:
            for key in ("_releases", "_release_cursor", "_release_oldest"):
                record.pop(key, None)
            record.setdefault("gaps", []).append(f"releases:{err.code}")
    for start in range(0, len(ok), README_BATCH):
        chunk = ok[start:start + README_BATCH]
        try:
            texts = fetch_readmes([r["full_name"] for r in chunk])
        except GhError as err:
            for record in chunk:
                record.setdefault("gaps", []).append(f"readme:{err.code}")
            continue
        for record in chunk:
            text = texts.get(record["full_name"])
            record["readme_found"] = text is not None
            record["features"] = detect_features(features, text, record["github_description"], " ".join(record["topics"]))

    def contributors(record):
        old = cache.get(record["repo"].lower())
        if not contributors_due(old, refresh):
            for key in GAP_FIELDS["contributors"]:
                if key in old:
                    record[key] = old[key]
            # Records written before the stamp existed: date the list by the snapshot it came with. Without
            # this the age check falls back to the record's own fetch date, which is always recent, so the
            # list would never be refreshed.
            if not record.get("contributors_fetched_at"):
                record["contributors_fetched_at"] = old.get("fetched_at")
            return
        try:
            record.update(fetch_contributors(record["full_name"]))
        except GhError as err:   # e.g. 403 when the contributor list is too large for the API
            record.setdefault("gaps", []).append(f"contributors:{err.code}")

    with cf.ThreadPoolExecutor(max_workers=REST_WORKERS) as pool:
        list(pool.map(contributors, ok))


def collect(projects, cache, refresh, features, spread=False):
    """Fetch the projects that are due and store them in the cache. Returns how many were processed."""
    todo = select_targets(projects, cache, refresh, spread)
    print(f"fetching {len(todo)} of {len(projects)} projects", flush=True)
    if not todo:
        return 0
    preflight()
    done, failed_batches = 0, 0
    for start in range(0, len(todo), BATCH):
        try:
            check_budget()
        except BudgetExceeded:
            print(f"  time budget reached; {len(todo) - done} projects left for the next run", flush=True)
            return done
        chunk = todo[start:start + BATCH]
        try:
            fetched = fetch_batch(chunk)
            enrich(list(fetched.values()), cache, refresh, features)
        except BudgetExceeded:
            print(f"  time budget reached; {len(todo) - done} projects left for the next run", flush=True)
            return done
        except Exception as exc:  # keep going; the previous snapshot of these repos is kept
            fetched = {repo: error_record(repo, "exception", str(exc)) for repo in chunk}
        for repo, record in fetched.items():
            cache[repo.lower()] = merge_record(cache.get(repo.lower()), record)
        done += len(chunk)
        save_metrics(cache)
        print(f"  {done}/{len(todo)}", flush=True)
        # Circuit breaker: if whole batches keep failing (bad token, GitHub outage), stop rather than burn the run.
        if all(r.get("error") and r["error"] not in GONE for r in fetched.values()):
            failed_batches += 1
            if failed_batches >= MAX_FAILED_BATCHES:
                raise Stopped(f"stopping: {failed_batches} batches in a row failed completely "
                              f"(last error: {next(iter(fetched.values())).get('error_message', '')[:200]})")
        else:
            failed_batches = 0
    return done


def attention(projects, cache):
    """Projects that need attention in data/projects.json, as [(heading, hint, [(repo, detail)])].

    Only repository names and error codes go in: an error message can quote text from GitHub, and this list is
    posted to an issue."""
    gone, failing, renamed, capped = [], [], [], []
    for p in projects:
        m = cache.get(p["repo"].lower()) or {}
        if m.get("error"):
            gone.append((p["repo"], f"{m['error']}, last checked {day(m.get('fetched_at'))}"))
        if m.get("last_error"):
            failing.append((p["repo"], f"{m['last_error']}, kept snapshot from {day(m.get('fetched_at'))}"))
        if m.get("full_name") and m["full_name"].lower() != p["repo"].lower():
            renamed.append((p["repo"], f"now {m['full_name']}"))
        if m.get("releases_12m_capped"):
            capped.append((p["repo"], ""))
    return [(heading, hint, items) for heading, hint, items in [
        ("Unavailable", "The repository is gone or blocked. Remove it from `data/projects.json`, or point it at "
                        "the new location.", gone),
        ("Fetch failed", "A temporary error; the previous snapshot is kept and the fetch is retried every run.",
         failing),
        ("Renamed or moved", "Update `repo` in `data/projects.json` to the new name.", renamed),
        (f"More than {RELEASE_PAGES * 100} releases", "The 12-month release count is a lower bound.", capped),
    ] if items]


def report(projects, cache):
    """Print projects that need attention in data/projects.json."""
    for heading, _, items in attention(projects, cache):
        print(f"{heading.lower()} ({len(items)}):")
        for repo, detail in items:
            print(f"  {repo}" + (f" ({detail})" if detail else ""))


def freshness_summary(projects, cache, previous):
    snapshots = []
    refreshed = 0
    for project in projects:
        key = project["repo"].lower()
        record = cache.get(key)
        if not record or record.get("error") or not record.get("fetched_at"):
            continue
        snapshots.append(parse_ts(record["fetched_at"]))
        if record is not previous.get(key) and not record.get("last_error"):
            refreshed += 1
    fresh = sum(stamp >= NOW - MAX_AGE for stamp in snapshots)
    total = len(projects)
    coverage = f"{fresh / total:.0%}" if total else "n/a"
    oldest = f"{(NOW - min(snapshots)).days} days" if snapshots else "n/a"
    return (f"## Metrics freshness\n\n"
            f"- Successfully refreshed this run: {refreshed}\n"
            f"- Measured within seven days: {fresh}/{total} ({coverage})\n"
            f"- Oldest successful snapshot: {oldest}\n\n")


def maintenance_markdown(projects, cache):
    """Review list for the maintenance issue and the job summary; empty when nothing needs attention."""
    # Only what an edit to data/projects.json fixes. Failed fetches clear themselves on a later run, and capped
    # release counts cannot be fixed, so either would keep the issue open (or reopen it) for nothing.
    fixable = ("Unavailable", "Renamed or moved")
    groups = [g for g in attention(projects, cache) if g[0] in fixable]
    if not groups:
        return ""
    lines = ["Projects in `data/projects.json` that need a manual fix, from the latest metrics run. "
             "This issue is rewritten on every run and closed when the list is empty."]
    for heading, hint, items in groups:
        lines += ["", f"### {heading} ({len(items)})", "", hint, ""]
        for repo, detail in items:
            # Names come from data/projects.json and from GitHub; neither is trusted in an issue body.
            name = f"[{untrusted(repo)}](https://github.com/{repo})" if REPO_NAME.match(repo) else untrusted(repo)
            lines.append(f"- {name}" + (f" — {untrusted(str(detail))}" if detail else ""))
    return "\n".join(lines)[:65000] + "\n"


def weekly_link_summary(projects, cache):
    counts = {title: len(items) for title, _, items in attention(projects, cache)}
    statuses = [status_of(cache.get(p["repo"].lower())) for p in projects]
    return ("## Catalog links\n\n"
            f"Latest daily snapshots for {len(projects)} indexed repositories. "
            f"Moved: {counts.get('Renamed or moved', 0)} · Unavailable: {counts.get('Unavailable', 0)} · "
            f"Archived: {statuses.count('Archived')} · Fetch failed with a previous snapshot: "
            f"{counts.get('Fetch failed', 0)} · Awaiting a first fetch: {statuses.count('Not fetched')}.\n\n"
            "[Review moved or unavailable repositories](https://github.com/erson/orchestration-atlas/issues?q=is%3Aissue+is%3Aopen+label%3Amaintenance)"
            " · [Browse archived projects](https://erson.github.io/orchestration-atlas/?status=Archived#directory)\n")


# --- Validation --------------------------------------------------------------------------------------------------

REPO_NAME = re.compile(r"^[A-Za-z0-9-]+/[A-Za-z0-9._-]+$")
ORIGINS = {"awesome-list", "discovered", "adjacent"}


def check_data(doc):
    """Problems in the hand-edited data files, as a list of messages. Makes no network calls."""
    problems = []
    if not isinstance(doc, dict):
        return ["data/projects.json: the top level must be an object"]
    cats = doc.get("categories")
    if not isinstance(cats, list) or not cats:
        return ["data/projects.json: `categories` must be a non-empty list"]
    if not all(isinstance(c, dict) for c in cats):
        return ["data/projects.json: every category must be an object"]
    if not isinstance(doc.get("projects"), list) or not all(isinstance(p, dict) for p in doc["projects"]):
        return ["data/projects.json: `projects` must be a list of objects"]
    ids = [c.get("id") for c in cats]
    for c in cats:
        if not c.get("id") or not c.get("title"):
            problems.append(f"data/projects.json: category without id or title: {c}")
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"data/projects.json: category id `{dup}` appears more than once")
    seen = {}
    for n, p in enumerate(doc.get("projects") or [], 1):
        where = f"data/projects.json: project {n} ({p.get('repo', '?')})"
        repo = p.get("repo")
        if not isinstance(repo, str) or not REPO_NAME.match(repo):
            problems.append(f"{where}: `repo` must look like owner/name")
        elif repo.lower() in seen:
            problems.append(f"{where}: duplicate of project {seen[repo.lower()]}")
        else:
            seen[repo.lower()] = n
        for key in ("name", "description"):
            if not isinstance(p.get(key), str) or not p[key].strip():
                problems.append(f"{where}: `{key}` is missing or empty")
        if "guide_task" in p and (not isinstance(p["guide_task"], str) or not p["guide_task"].strip()):
            problems.append(f"{where}: `guide_task` must be a non-empty string")
        if p.get("category") not in ids:
            problems.append(f"{where}: unknown category `{p.get('category')}` (known: {', '.join(ids)})")
        if p.get("origin") not in ORIGINS:
            problems.append(f"{where}: `origin` must be one of {', '.join(sorted(ORIGINS))}")
    if not seen:
        problems.append("data/projects.json: `projects` is empty")

    try:
        cfg = json.loads(DISCOVERY_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        return problems + [f"data/discovery.json: {err}"]
    if not isinstance(cfg, dict):
        return problems + ["data/discovery.json: expected an object"]
    if not cfg.get("queries") or not isinstance(cfg["queries"], list) or not all(isinstance(q, str) and q.strip() for q in cfg["queries"]):
        problems.append("data/discovery.json: `queries` must be a list of non-empty strings")
    if "older_queries" in cfg:
        older = cfg["older_queries"]
        if not isinstance(older, list) or not older or not all(isinstance(q, str) and q.strip() for q in older):
            problems.append("data/discovery.json: older_queries must be a non-empty list of search queries")
    if "readme_query" in cfg:
        readme = cfg["readme_query"]
        if not isinstance(readme, str) or "in:readme" not in readme.split():
            problems.append("data/discovery.json: readme_query must include in:readme")
        elif isinstance(cfg.get("queries"), list) and readme in cfg["queries"]:
            problems.append("data/discovery.json: readme_query must be separate from regular searches")
    if "older_query" in cfg and not (isinstance(cfg["older_query"], str) and cfg["older_query"].strip()):
        problems.append("data/discovery.json: older_query must be a non-empty string")
    for key in ("min_stars", "window_days"):
        if key in cfg and (not isinstance(cfg[key], int) or cfg[key] < 0):
            problems.append(f"data/discovery.json: `{key}` must be a non-negative integer")
    for repo in cfg.get("rejected", []):
        if not isinstance(repo, str) or not REPO_NAME.match(repo):
            problems.append(f"data/discovery.json: rejected entry `{repo}` must look like owner/name")
        elif repo.lower() in seen:
            problems.append(f"data/discovery.json: `{repo}` is rejected but also listed in data/projects.json")
    return problems


# --- Discovery ---------------------------------------------------------------------------------------------------

def check_discovery_state():
    if not DISCOVERY_STATE_FILE.exists():
        return []
    try:
        state = json.loads(DISCOVERY_STATE_FILE.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            raise ValueError("expected an object")
        month = state.get("older_month")
        if month is not None:
            datetime.strptime(month, "%Y-%m")
        if "readme_week" in state:
            datetime.strptime(state["readme_week"], "%Y-%m-%d")
        if "older_topic" in state and not isinstance(state["older_topic"], str):
            raise ValueError("invalid older_topic")
        if not isinstance(state.get("next_query"), str) or not state["next_query"].strip():
            raise ValueError("missing next_query")
        pages = state.get("pages", 0)
        if type(pages) is not int or not 0 <= pages < 20:
            raise ValueError("invalid page count")
        if pages:
            if not isinstance(state.get("after"), str) or not state["after"]:
                raise ValueError("missing page cursor")
            datetime.strptime(state["window_start"], "%Y-%m-%d")
            if not isinstance(state.get("filters"), str):
                raise ValueError("missing cursor search filters")
        elif state.get("after") is not None:
            raise ValueError("cursor without completed pages")
    except (OSError, ValueError, KeyError, TypeError) as err:
        return [f"data/discovery-state.json: {err}"]
    return []


def discovery_page(query, qualifiers, after, found, previous, excluded, features, performance=None):
    check_budget()
    data, errors = graphql(SEARCH_QUERY, {"q": f"{query} {qualifiers}", "after": after})
    result = data.get("search")
    if errors or not result:
        raise GhError(None, (errors[0] if errors else {}).get("message", "search returned no data"))
    if performance is not None:
        discovery_stats.record_page(performance, query, len(result["nodes"]))
    for node in result["nodes"]:
        if not node or not node.get("nameWithOwner"):
            continue
        key = node["nameWithOwner"].lower()
        if key in excluded or node["isFork"] or node["isArchived"]:
            continue
        topics = [n["topic"]["name"] for n in (node.get("repositoryTopics") or {}).get("nodes") or []]
        entry = found.setdefault(key, {
            "repo": node["nameWithOwner"], "url": node["url"], "description": node.get("description") or "",
            "stars": node["stargazerCount"], "language": (node.get("primaryLanguage") or {}).get("name") or "",
            "topics": topics, "created_at": node["createdAt"], "pushed_at": node["pushedAt"],
            "features": detect_features(features, node.get("description"), " ".join(topics)),
            "first_seen": previous.get(key, {}).get("first_seen", TODAY.isoformat()),
            "last_seen": TODAY.isoformat(), "queries": list(previous.get(key, {}).get("queries", [])),
        })
        if query not in entry["queries"]:
            entry["queries"].append(query)
    return result["pageInfo"]["endCursor"] if result["pageInfo"]["hasNextPage"] else None


def next_older_query(choices, last_query, totals):
    """Rotate in configuration order, preferring queries with at least one accepted candidate."""
    # Scan from the successor even when the previous topic no longer has eligible candidates.
    offset = choices.index(last_query) + 1 if last_query in choices else 0
    rotated = choices[offset:] + choices[:offset]
    return next((q for q in rotated if totals.get(q, {}).get("accepted", 0)), rotated[0])


def sample_discovery_page(query, qualifiers, seconds, found, previous, excluded, features, performance):
    global DEADLINE
    overall_deadline = DEADLINE
    expires = time.monotonic() + seconds
    DEADLINE = min(expires, overall_deadline) if overall_deadline is not None else expires
    try:
        discovery_page(query, qualifiers, None, found, previous, excluded, features, performance=performance)
        return f"checked one page for `{query}`"
    except (BudgetExceeded, GhError) as err:
        print(f"  sample interrupted: {query} ({err})", flush=True)
        return f"interrupted while checking `{query}`"
    finally:
        DEADLINE = overall_deadline


def reset_search_cursor(state, next_query):
    for key in ("after", "pages", "window_start", "filters"):
        state.pop(key, None)
    state["next_query"] = next_query


def discover(doc, cache, features, days, report=None):
    cfg = json.loads(DISCOVERY_FILE.read_text(encoding="utf-8"))
    days = days or cfg.get("window_days", 30)
    start = (TODAY - timedelta(days=days)).isoformat()
    filters = f"stars:>={cfg.get('min_stars', 10)} fork:false archived:false"
    project_keys = {p["repo"].lower() for p in doc["projects"]}
    indexed = project_keys | {m["full_name"].lower() for key, m in cache.items()
                             if key in project_keys and m.get("full_name")}
    rejected = {r.lower() for r in cfg.get("rejected", [])}
    excluded = indexed | rejected
    previous = {}
    if CANDIDATES_FILE.exists():
        previous = {c["repo"].lower(): c for c in json.loads(CANDIDATES_FILE.read_text(encoding="utf-8"))["candidates"]}
    performance = discovery_stats.load(DISCOVERY_STATS_FILE)
    discovery_stats.attribute(performance, previous.values())
    discovery_stats.reconcile(performance, indexed, rejected)
    found = {}
    queries = list(dict.fromkeys(cfg["queries"]))
    state = json.loads(DISCOVERY_STATE_FILE.read_text(encoding="utf-8")) if DISCOVERY_STATE_FILE.exists() else {}
    if state.get("next_query") not in queries:
        reset_search_cursor(state, queries[0])
    if state.get("after") and state.get("filters") != filters:
        reset_search_cursor(state, state["next_query"])
    preflight()
    month = TODAY.strftime("%Y-%m")
    week = (TODAY - timedelta(days=TODAY.weekday())).isoformat()
    older = cfg.get("older_queries") or ([cfg["older_query"]] if cfg.get("older_query") else [])
    monthly_due = bool(older) and state.get("older_month") != month
    readme_due = bool(cfg.get("readme_query")) and state.get("readme_week") != week
    samples = []
    # Both samples together receive at most one eighth of the remaining time, capped at one minute.
    if monthly_due or readme_due:
        available = max(0, DEADLINE - time.monotonic()) if DEADLINE is not None else 480
        seconds = min(60, available / 8) / (int(monthly_due) + int(readme_due))
    if monthly_due:
        query = next_older_query(older, state.get("older_topic"), discovery_stats.totals(performance))
        state.update(older_month=month, older_topic=query)
        result = sample_discovery_page(query, f"created:<{start} pushed:>={start} {filters} sort:updated-desc",
                                       seconds, found, previous, excluded, features, performance)
        samples.append(f"Monthly search: {result}.")
    if readme_due:
        state["readme_week"] = week
        result = sample_discovery_page(cfg["readme_query"], f"created:>={start} {filters}", seconds,
                                       found, previous, excluded, features, performance)
        samples.append(f"Weekly README experiment: {result}.")
    # A README experiment takes one regular search slot. Resume the deferred query next week.
    regular_target = max(1, len(queries) - int(readme_due))
    completed = 0
    reason = "planned regular queries completed"
    capped = 0
    failure = None
    try:
        while completed < regular_target:
            query = state["next_query"]
            # The GitHub cursor belongs to the exact search used on the preceding run.
            window = state.get("window_start", start)
            after = discovery_page(query, f"created:>={window} {filters}", state.get("after"),
                                   found, previous, excluded, features, performance=performance)
            pages = state.get("pages", 0) + 1
            if after and pages < 20:
                state.update(after=after, pages=pages, window_start=window, filters=filters)
                continue
            if after:
                capped += 1
            completed += 1
            next_query = queries[(queries.index(query) + 1) % len(queries)]
            reset_search_cursor(state, next_query)
            print(f"  completed {query} ({pages} pages)", flush=True)
    except BudgetExceeded:
        reason = "time budget reached"
    except GhError as err:
        failure = err
        reason = "GitHub search interrupted"
        print(f"  {reason}: {err}", flush=True)
        if state.get("after") and "cursor" in str(err).lower():
            # An expired GitHub cursor must not block every following run.
            reset_search_cursor(state, state["next_query"])
    fresh = set(found).difference(previous)
    for key, entry in previous.items():
        if key not in excluded:
            found.setdefault(key, entry)
    candidates = sorted(found.values(), key=lambda c: (-c["stars"], c["repo"].lower()))
    payload = {"generated_at": NOW.isoformat(timespec="seconds"), "window_start": start, "candidates": candidates}
    # Commit progress only after saving the candidates from those pages. Replaying a page is idempotent.
    discovery_stats.attribute(performance, candidates)
    write_atomic(DISCOVERY_STATS_FILE, json.dumps(performance, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    write_atomic(CANDIDATES_FILE, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    write_atomic(DISCOVERY_STATE_FILE, json.dumps(state, indent=2) + "\n")
    coverage = f"Weekly queries completed: {completed}/{len(queries)} ({reason})."
    if completed < len(queries):
        coverage += f" Next query: `{state['next_query']}`."
    if capped:
        coverage += f" Queries at the 1,000-result limit: {capped}."
    if samples:
        coverage += " " + " ".join(samples)
    print(f"{len(candidates)} open candidates, {len(fresh)} new this run. {coverage}")
    if report:
        write_atomic(Path(report), candidates_markdown(candidates, fresh, coverage))
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary, "a", encoding="utf-8") as out:
            print(discovery_stats.markdown(performance), file=out)
    if failure:
        raise SystemExit(f"{reason}: {failure}")


def candidate_evidence(candidate):
    queries = candidate.get("queries") or []
    topics = candidate.get("topics") or []
    features = candidate.get("features") or []
    query = queries[-1] if queries else ""
    matched_topic = next((t for t in topics if f"topic:{t}".lower() in query.lower().split()), None)
    evidence = [f"Query: {untrusted(query)}"] if query else []
    if matched_topic:
        evidence.append(f"Topic: {untrusted(matched_topic)}")
    elif features:
        evidence.append(f"Feature: {untrusted(features[0])}")
    elif topics:
        evidence.append(f"Topic: {untrusted(topics[0])}")
    elif candidate.get("description"):
        evidence.append(f"Description: {untrusted(candidate['description'][:80])}")
    return "<br>".join(evidence) or "—"


def candidates_markdown(candidates, fresh, coverage, limit=150):
    lines = [
        f"{len(candidates)} open candidates, {len(fresh)} new this run. {coverage}", "",
        'To add one, append it to `data/projects.json` with `origin: "discovered"`. To dismiss one, add it to '
        "`rejected` in `data/discovery.json`. This issue is rewritten on every discovery run.",
    ]
    shown = 0
    for heading, is_new in (("New this run", True), ("Previously found", False)):
        group = [c for c in candidates if (c["repo"].lower() in fresh) == is_new]
        lines.extend(["", f"### {heading} ({len(group)})", ""])
        if not group:
            lines.append("None.")
            continue
        if shown == limit:
            continue
        lines.extend(["| Repository | Stars | Last seen | Language | Created | Description | Features | Why matched |",
                      "|---|---:|---|---|---|---|---|---|"])
        for c in group[:limit - shown]:
            desc = untrusted((c["description"] or "")[:140])
            feats = ", ".join(untrusted(f) for f in c.get("features", []))
            lines.append(f"| [{cell(c['repo'])}]({c['url']}) | {c['stars']:,} | {c.get('last_seen') or 'Unknown'} | "
                         f"{cell(c['language']) or '—'} | {day(c['created_at'])} | {desc or '—'} | "
                         f"{feats or '—'} | {candidate_evidence(c)} |")
            shown += 1
    body = "\n".join(lines)
    if shown < len(candidates) or len(body) > 64000:
        body = body[:64000].rsplit("\n", 1)[0] if len(body) > 64000 else body
        body += "\n\nSee the complete list in `data/candidates.json`."
    return body + "\n"


# --- Rendering ---------------------------------------------------------------------------------------------------

def as_of(m):
    """UTC date the record was collected. Statuses and day counts are judged as of that date."""
    return parse_ts(m["fetched_at"]).date() if m.get("fetched_at") else TODAY


def status_of(m):
    if not m:
        return "Not fetched"
    if m.get("error"):
        return "Unavailable"
    if m.get("archived"):
        return "Archived"
    if not m.get("last_commit_at"):
        return "Stale"
    days = (as_of(m) - parse_ts(m["last_commit_at"]).date()).days
    if days <= 30:
        return "Active"
    if days <= 90:
        return "Recent"
    if days <= 365:
        return "Slow"
    return "Stale"


def build_rows(projects, cache):
    rows = []
    for p in projects:
        m = cache.get(p["repo"].lower(), {})
        row = {**p, **m, "status": status_of(m)}
        last = m.get("last_commit_at")
        row["days_since_commit"] = (as_of(m) - parse_ts(last).date()).days if last else None
        created = m.get("created_at")
        months = max((as_of(m) - parse_ts(created).date()).days / 30.44, 1.0) if created else None
        row["age_months"] = round(months, 1) if months else None
        row["stars_per_month"] = round(m.get("stars", 0) / months, 1) if months else None
        rows.append(row)
    return rows


def render_csv(rows):
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        flat = {}
        for key in CSV_FIELDS:
            value = row.get(key)
            if key == "languages":
                value = ";".join(f"{l['name']} {l['share']:.1%}" for l in value or [])
            elif isinstance(value, list):
                value = ";".join(value)
            # A spreadsheet runs a cell that starts with one of these as a formula; a leading quote keeps it text.
            if isinstance(value, str) and value.lstrip()[:1] in ("=", "+", "-", "@"):
                value = "'" + value
            flat[key] = "" if value is None else value
        writer.writerow(flat)
    return buf.getvalue()


def cell(text):
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def untrusted(text):
    """Text written by a repository owner (GitHub description), made inert for Markdown.

    Escapes the characters that start links, images, HTML, and emphasis. A zero-width space breaks @mentions,
    bare URLs (`https://`, `www.`), and issue references (`#1`, `owner/repo#1`, `GH-1`), which GitHub links
    even when escaped. So the text cannot notify people, plant a link, or leave a "mentioned this" entry on
    an issue in another repository."""
    text = re.sub(r"([\\`*_{}\[\]<>()#!~])", r"\\\1", text or "")   # before cell(), which adds its own backslashes
    text = cell(text).replace("@", "@\u200b").replace("#", "#\u200b").replace("://", ":\u200b//")
    return re.sub(r"(?i)\b(www|gh)(?=[.-])", "\\1\u200b", text)


def fmt_int(value):
    return "—" if value is None else f"{value:,}"


def short_num(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    return f"{value / 1000:.0f}k" if value >= 10_000 else f"{value:,}"


def pct(share):
    return "<1%" if 0 < share < 0.005 else f"{share:.0%}"


def bar(share, width=20):
    filled = round(share * width)
    return "`" + "█" * filled + "░" * (width - filled) + "`"


def status_label(status):
    return f"{STATUS_ICON.get(status, '')} {status}".strip()


def day(ts):
    return ts[:10] if ts else "—"


def name_link(row):
    url = row.get("url") or f"https://github.com/{row['repo']}"
    tag = " _(new)_" if row["origin"] == "discovered" else ""
    return f"[{cell(row['name'])}]({url}){tag}"


def license_label(row):
    if row.get("error") or row.get("license") is None:
        return "—"
    if row["license"] == "":
        return "None"
    return "Other" if row["license"] == "NOASSERTION" else row["license"]


def language_label(row):
    shown = [f"{l['name']} {l['share']:.0%}" for l in row.get("languages") or [] if l["share"] >= 0.05][:3]
    return ", ".join(shown) or cell(row.get("language")) or "—"


def features_label(row):
    if not isinstance(row.get("features"), list):
        return "—"
    return ", ".join(row["features"]) or "none detected"


def anchor(title):
    """GitHub's heading anchor: lower-case, drop punctuation, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")


def project_description(row):
    # The first two are written by hand in data/projects.json; GitHub's description is the owner's text.
    desc = cell(row.get("description") or row.get("list_description")) or untrusted(row.get("github_description"))
    if row.get("notes"):
        desc = f"{desc} ({cell(row['notes'])})".strip()
    if len(desc) <= 120:
        return desc or "—"
    escaped = html.escape(desc).replace(r"\|", "&#124;")
    return f"<details><summary>Description</summary>{escaped}</details>"


def project_table(rows):
    lines = [
        "| Project | Popularity | Activity | Other details |",
        "|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda r: (-(r.get("stars") or 0), r["name"].lower())):
        tag = r.get("latest_release_tag")
        if tag:
            tag = re.sub(r"([._/@-])", r"\1<wbr>", html.escape(untrusted(tag), quote=False))
        release = f"{tag} ({day(r.get('latest_release_at'))})" if tag else "—"
        open_work = "—" if r.get("open_prs") is None else f"{fmt_int(r.get('open_issues'))} / {fmt_int(r['open_prs'])}"
        lines.append("| " + " | ".join([
            f"{name_link(r)}<br>{project_description(r)}<br>_Features:_ {features_label(r)}",
            f"**{fmt_int(r.get('stars'))} stars**<br>{fmt_int(r.get('contributors'))} contributors<br>{fmt_int(r.get('forks'))} forks",
            f"**{status_label(r['status'])}**<br>{fmt_int(r.get('commits_90d'))} commits (90d)<br>Last commit: {day(r.get('last_commit_at'))}",
            f"Language: {language_label(r)}<br>Release: {release}<br>Issues / PRs: {open_work}<br>License: {license_label(r)}",
        ]) + " |")
    return "\n".join(lines)


def glance_table(rows):
    contributors = [r["contributors"] for r in rows if r.get("contributors") is not None]
    days = [r["days_since_commit"] for r in rows if r.get("days_since_commit") is not None]
    median = lambda values: f"{statistics.median(values):g}" if values else "—"
    counts = {s: sum(r["status"] == s for r in rows) for s in STATUSES}
    shown = [s for s in STATUSES if counts[s] or s != "Not fetched"]
    return "\n".join([
        "| Projects tracked | Total stars | Median contributors | Median days since last commit |",
        "|:-:|:-:|:-:|:-:|",
        f"| **{len(rows):,}** | **{sum(r.get('stars') or 0 for r in rows):,}** | **{median(contributors)}** "
        f"| **{median(days)}** |",
        "",
        "| " + " | ".join(status_label(s) for s in shown) + " |",
        "|" + ":-:|" * len(shown),
        "| " + " | ".join(f"**{counts[s]:,}**" for s in shown) + " |",
        "",
        "Status is the age of the last commit on the default branch: Active up to 30 days, Recent up to 90, "
        "Slow up to a year, Stale beyond that. See [Methodology](#methodology).",
    ])


def category_overview(categories, rows):
    lines = [
        "| Category | Projects | Total stars | Active or recent | Stale or archived |",
        "|---|--:|--:|--:|--:|",
    ]
    for cat in categories:
        members = [r for r in rows if r["category"] == cat["id"]]
        if not members:
            continue
        active = sum(r["status"] in ("Active", "Recent") for r in members)
        stale = sum(r["status"] in ("Stale", "Archived") for r in members)
        stars = sum(r.get("stars") or 0 for r in members)
        lines.append(f"| [{SHORT.get(cat['id'], cat['id'])}](#{anchor(cat['title'])}) | {len(members)} | {stars:,} "
                     f"| {active} ({active / len(members):.0%}) | {stale} |")
    return "\n".join(lines)


def language_overview(rows):
    live = [r for r in rows if r["status"] != "Unavailable" and r.get("language")]
    counts = {}
    for r in live:
        counts[r["language"]] = counts.get(r["language"], 0) + 1
    lines = ["| Main language | Projects | Share | |", "|---|--:|--:|---|"]
    top = max(counts.values(), default=1)
    for lang, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:10]:
        # Bars are relative to the most common language, with at least one block, so small shares stay visible.
        lines.append(f"| {cell(lang)} | {n} | {pct(n / len(live))} | {bar(max(n / top, 0.05))} |")
    return "\n".join(lines)


def feature_overview(rows, features):
    checked = [r for r in rows if r["status"] != "Unavailable" and isinstance(r.get("features"), list)]
    if not checked:
        return "_Not collected yet._"
    lines = [
        f"Share of the {len(checked)} projects whose README, description, or topics mention each feature. "
        "Keyword matching, so treat it as a rough guide; see [Methodology](#methodology). "
        "Per-project features are in the interactive explorer and in `data/projects.csv`.", "",
        "| Group | Mentioned by |", "|---|---|",
    ]
    groups = {}
    for group, label, _ in features:
        groups.setdefault(group, []).append((sum(label in r["features"] for r in checked), label))
    for group, items in groups.items():
        ranked = sorted(items, key=lambda item: -item[0])   # stable: ties keep the order of data/features.json
        lines.append(f"| **{group}** | " + " · ".join(f"{label} **{pct(n / len(checked))}**" for n, label in ranked) + " |")
    return "\n".join(lines)


def top_by_stars(rows):
    top = sorted(rows, key=lambda r: -(r.get("stars") or 0))[:15]
    lines = ["| # | Project | Category | Stars | Contributors | Status |", "|--:|---|---|--:|--:|---|"]
    for i, r in enumerate(top, 1):
        lines.append(f"| {i} | {name_link(r)} | {SHORT.get(r['category'], r['category'])} | {fmt_int(r.get('stars'))} | {fmt_int(r.get('contributors'))} | {status_label(r['status'])} |")
    return "\n".join(lines)


def recent_commits(rows):
    dated = sorted((r for r in rows if r.get("last_commit_at")), key=lambda r: r["last_commit_at"], reverse=True)[:15]
    lines = ["| # | Project | Category | Last commit | Commits (90d) | Status |", "|--:|---|---|---|--:|---|"]
    for i, r in enumerate(dated, 1):
        lines.append(f"| {i} | {name_link(r)} | {SHORT.get(r['category'], r['category'])} | {day(r['last_commit_at'])} | {fmt_int(r.get('commits_90d'))} | {status_label(r['status'])} |")
    return "\n".join(lines)


def risk_table(rows):
    pool = [r for r in rows if r.get("top_author_share") is not None
            and (r.get("commits_all_time") or 0) >= 100 and not r.get("archived")]
    top = sorted(pool, key=lambda r: -r["top_author_share"])[:10]
    lines = ["| Project | Top author share | Contributors | Commits (all time) | Status |", "|---|--:|--:|--:|---|"]
    for r in top:
        lines.append(f"| {name_link(r)} | {r['top_author_share']:.0%} | {fmt_int(r.get('contributors'))} | {fmt_int(r.get('commits_all_time'))} | {status_label(r['status'])} |")
    return "\n".join(lines)


TASKS = {
    "terminal": "Run parallel coding sessions in a terminal",
    "desktop": "Manage coding agents in a desktop or web UI",
    "swarms": "Coordinate a team of agents",
    "loops": "Repeat an agent loop until a condition is met",
    "tasks": "Delegate a task to an autonomous runner",
    "infra": "Build on orchestration infrastructure",
    "assistants": "Set up a personal assistant",
    "resting": "Explore the resting collection",
    "adjacent": "Build with a general-purpose agent SDK",
}
EXPLORER_FILE = ROOT / "catalog.html"
HISTORY_FILE = ROOT / "data" / "weekly-history.json"


def render_explorer(doc, rows, weeks=None):
    keys = ("repo", "name", "category", "status", "language", "stars", "features", "description",
            "contributors", "commits_90d", "latest_release_at", "last_commit_at", "license",
            "top_author_share", "releases_12m", "fetched_at", "commits_all_time", "open_issues", "closed_issues")
    entries = [{k: r.get(k) for k in keys} for r in rows]
    sample_file = ROOT / "data/issue-samples.json"
    samples = json.loads(sample_file.read_text()) if sample_file.exists() else {}
    for entry in entries:
        sample = samples.get(entry["repo"].lower())
        if sample:
            entry["issues"] = {k: v for k, v in sample.items() if k != "cache"}
        for key in ("latest_release_at", "last_commit_at", "fetched_at"):
            entry[key] = (entry[key] or "")[:10]
    dates = sorted(r["fetched_at"][:10] for r in rows if r.get("fetched_at"))
    snapshot = "unknown" if not dates else " to ".join(dict.fromkeys((dates[0], dates[-1])))
    if weeks is None:
        weeks = history.load(HISTORY_FILE)["weeks"]
    payload = {"snapshot": snapshot, "projects": entries, "history": weeks,
               "categories": {c["id"]: TASKS.get(c["id"], c["title"]) for c in doc["categories"]}}
    # JSON script contents must never contain an HTML closing tag from a project description.
    encoded = json.dumps(payload, separators=(",", ":")).replace("<", r"\u003c")
    template = (ROOT / "scripts/catalog.html").read_text(encoding="utf-8")
    modules = ("project-map.js", "inspect.js", "history.js", "share-view.js")
    scripts = "\n".join((ROOT / "scripts" / name).read_text(encoding="utf-8") for name in modules)
    return template.replace("/*__EXPLORER_MODULES__*/", scripts).replace("__CATALOG_JSON__", encoded)


def render_readme(doc, rows, features):
    cats = doc["categories"]
    dates = sorted({as_of(r).isoformat() for r in rows if r.get("fetched_at")})
    snapshot = dates[0] if len(dates) == 1 else f"{dates[0]} to {dates[-1]}" if dates else TODAY.isoformat()
    live = [r for r in rows if r["status"] != "Unavailable"]
    active = sum(r["status"] == "Active" for r in live)
    editorial = json.loads(readme_editor.STATE.read_text()) if readme_editor.STATE.exists() else {}
    metrics = [("Available projects", f"{len(live):,}"), ("Active in 30 days", f"{active:,}"),
               ("Combined stars", short_num(sum(r.get("stars") or 0 for r in live)))]
    parts = [
        f"# {TITLE}", "",
        "Find tools for running, coordinating, and supervising AI agents. Start with the task you need to do, "
        "then compare activity, releases, and maintenance across projects.", "",
        "**[Open the explorer](https://erson.github.io/orchestration-atlas/)** · [Download for offline use](https://github.com/erson/orchestration-atlas/raw/refs/heads/main/catalog.html) "
        "· [Browse the searchable CSV on GitHub](data/projects.csv) · [Methodology](#methodology)", "",
        "Filter by task, feature, language, or activity "
        "and compare up to four projects side by side. Inspect a project against category peers, "
        "select a region of the project map, or copy a link to your comparison. The downloadable edition also works offline.", "",
        readme_editor.snapshot_figure(metrics, editorial.get("snapshot", "spec")), "",
        f"*Metrics collected {snapshot} (UTC). The index tracks {len(rows)} projects across {len(cats)} categories.*", "",
        *([readme_editor.render(editorial), ""] if editorial else []),
        "## Choose a task", "",
        *(f"- {name_link(r)} — {untrusted(r['guide_task'])}" for r in rows
          if r.get("guide_task") and r["status"] not in ("Archived", "Unavailable")),
        "",
        "| I want to… | Indexed | Commit within 90 days |",
        "|---|---:|---:|",
    ]
    collections = [(c, [r for r in rows if r["category"] == c["id"]]) for c in cats]
    for cat, members in collections:
        lively = sum(r["status"] in ("Active", "Recent") for r in members)
        title = TASKS.get(cat["id"], cat["title"])
        parts.append(f"| [{title}](#{anchor(cat['title'])}) | {len(members)} | {lively} |")
    parts += ["", "## Read the signals", "",
              "Use **last commit** for recency, **latest release** for shipping cadence, and "
              "**contributors** alongside **top author share** for maintenance concentration. "
              "Stars measure attention. Feature matches come from project text and need checking against its docs.", ""]
    analyses = [("At a glance", glance_table(rows)), ("Features", feature_overview(rows, features)),
                ("Languages", language_overview(rows)), ("Top 15 by stars", top_by_stars(rows)),
                ("Most recent commits", recent_commits(rows)), ("Single-maintainer risk", risk_table(rows))]
    for title, content in analyses:
        parts += [f"<details><summary>{title}</summary>", "", content, "", "</details>", ""]
    for cat, members in collections:
        if not members:
            continue
        parts += [f"## {cat['title']}", "", cat.get("description", ""), "",
                  f"<details><summary>Browse {len(members)} projects by name</summary>", "",
                  "| Project | Activity | Main language |", "|---|---|---|"]
        for r in sorted(members, key=lambda r: (r["name"].casefold(), r["repo"])):
            parts.append(f"| {name_link(r)} | {status_label(r['status'])} | {cell(r.get('language')) or '—'} |")
        parts += ["", "</details>", "", "[Back to tasks](#choose-a-task)", ""]
    parts += [METHOD, MAINTAIN, CREDITS]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(parts)).rstrip() + "\n"


def check_candidates():
    try:
        payload = json.loads(CANDIDATES_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        return [f"data/candidates.json: {err}"]
    if not isinstance(payload, dict) or not isinstance(payload.get("candidates"), list):
        return ["data/candidates.json: expected a candidates list"]
    problems = []
    for field in ("generated_at", "window_start"):
        value = payload.get(field)
        try:
            if not isinstance(value, str):
                raise ValueError
            parse_ts(value)
        except ValueError:
            problems.append(f"data/candidates.json: invalid {field}")
    seen = set()
    for n, candidate in enumerate(payload["candidates"], 1):
        where = f"data/candidates.json: candidate {n}"
        if not isinstance(candidate, dict):
            problems.append(f"{where}: expected an object")
            continue
        repo = candidate.get("repo")
        if not isinstance(repo, str) or not REPO_NAME.fullmatch(repo):
            problems.append(f"{where}: invalid repository name")
            continue
        if repo.lower() in seen:
            problems.append(f"{where}: duplicate repository {repo}")
        seen.add(repo.lower())
        if candidate.get("url") != f"https://github.com/{repo}":
            problems.append(f"{where}: URL must match {repo}")
        if type(candidate.get("stars")) is not int or candidate["stars"] < 0:
            problems.append(f"{where}: stars must be a non-negative integer")
        for field in ("description", "language", "first_seen", "created_at"):
            if not isinstance(candidate.get(field), str):
                problems.append(f"{where}: {field} must be a string")
        if "last_seen" in candidate:
            try:
                stamp = datetime.strptime(candidate["last_seen"], "%Y-%m-%d").date()
                if stamp.isoformat() != candidate["last_seen"]:
                    raise ValueError()
            except (TypeError, ValueError):
                problems.append(f"{where}: last_seen must use YYYY-MM-DD")
        for field in ("features", "topics", "queries"):
            values = candidate.get(field)
            if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                problems.append(f"{where}: {field} must be a list of strings")
    return problems


def check(generated=False):
    """--check: fail on broken data files, then render README and CSV in memory to catch rendering errors."""
    problems = []
    try:
        doc = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        sys.exit(f"data/projects.json: {err}")
    problems += check_data(doc)
    problems += check_candidates()
    problems += check_discovery_state()
    try:
        discovery_stats.load(DISCOVERY_STATS_FILE)
    except (OSError, ValueError) as err:
        problems.append(f"data/discovery-stats.json: {err}")
    try:
        weekly = history.load(HISTORY_FILE)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as err:
        problems.append(f"data/weekly-history.json: {err}")
    try:
        features = load_features()
    except (OSError, json.JSONDecodeError, KeyError, AttributeError, re.error) as err:
        problems.append(f"data/features.json: {err}")
        features = None
    if problems:
        sys.exit("\n".join(["data check failed:", *(f"  {p}" for p in problems)]))
    cache = {}
    if METRICS_FILE.exists() or generated:
        try:
            cache = json.loads(METRICS_FILE.read_text(encoding="utf-8"))["repos"]
            if not isinstance(cache, dict) or not all(isinstance(m, dict) for m in cache.values()):
                raise ValueError("expected a repos object containing metric records")
        except (OSError, ValueError, KeyError, TypeError) as err:
            sys.exit(f"data/metrics.json: {err}")
    rows = build_rows(doc["projects"], cache)
    outputs = ((README_FILE, render_readme(doc, rows, features)), (CSV_FILE, render_csv(rows)),
               (EXPLORER_FILE, render_explorer(doc, rows, weekly["weeks"])))
    if generated:
        for path, expected in outputs:
            if not path.is_file() or path.read_bytes() != expected.encode("utf-8"):
                sys.exit(f"{path.relative_to(ROOT)} differs from the cached data; run --render-only")
    missing = sum(p["repo"].lower() not in cache for p in doc["projects"])
    print(f"data check passed: {len(doc['projects'])} projects, {len(doc['categories'])} categories"
          + (f"; {missing} not fetched yet (the next daily run fetches them)" if missing else ""))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", action="store_true", help="fetch every project, not only stale ones")
    parser.add_argument("--spread", action="store_true",
                        help=f"also fetch the oldest records, so each run covers at least 1/{SPREAD_DAYS} of the projects")
    parser.add_argument("--render-only", action="store_true", help="skip GitHub calls and render from the cache")
    parser.add_argument("--only", nargs="+", metavar="OWNER/REPO", help="fetch only these repos, even if fresh")
    parser.add_argument("--discover", action="store_true", help="search GitHub for new projects and write data/candidates.json")
    parser.add_argument("--days", type=int, metavar="N", help="with --discover: projects created in the last N days")
    parser.add_argument("--report", metavar="FILE", help="with --discover: also write a Markdown review list")
    parser.add_argument("--max-minutes", type=float, metavar="N",
                        help="time budget: start no new work (and no rate-limit wait) after N minutes; "
                             "projects not reached are fetched on the next run")
    parser.add_argument("--maintenance", metavar="FILE",
                        help="also write a Markdown list of projects that need a manual fix (empty when none)")
    parser.add_argument("--check", action="store_true",
                        help="validate the data files and render in memory; writes nothing, makes no network calls")
    parser.add_argument("--check-generated", action="store_true",
                        help="validate data and verify README and CSV match the cache; makes no network calls")
    args = parser.parse_args()
    if args.check or args.check_generated:
        others = {k: v for k, v in vars(args).items() if k not in ("check", "check_generated")}
        if any(v not in (None, False) for v in others.values()):
            parser.error("data checks cannot be combined with update options")
        check(generated=args.check_generated)
        return
    global DEADLINE
    if args.max_minutes is not None:
        if args.max_minutes <= 0:
            parser.error("--max-minutes must be positive")
        DEADLINE = time.monotonic() + args.max_minutes * 60
    if args.render_only and (args.refresh or args.only or args.discover or args.spread):
        parser.error("--render-only makes no network calls, so it cannot be combined with other options")
    if (args.days or args.report) and not args.discover:
        parser.error("--days and --report only apply to --discover")
    if args.maintenance and args.discover:
        parser.error("--maintenance does not apply to --discover")

    doc = json.loads(PROJECTS_FILE.read_text(encoding="utf-8"))
    features = load_features()
    cache = {}
    if METRICS_FILE.exists():
        cache = json.loads(METRICS_FILE.read_text(encoding="utf-8")).get("repos", {})

    if args.discover:
        if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(summary, "a", encoding="utf-8") as output:
                print(weekly_link_summary(doc["projects"], cache), file=output)
        discover(doc, cache, features, args.days, args.report)
        return

    stopped = None
    if not args.render_only:
        previous = cache.copy()  # collect replaces records and retains older snapshots on transient errors.
        targets = doc["projects"]
        if args.only:
            wanted = {r.lower() for r in args.only}
            targets = [p for p in targets if p["repo"].lower() in wanted]
            unknown = wanted - {p["repo"].lower() for p in targets}
            if unknown:
                parser.error(f"not in data/projects.json: {', '.join(sorted(unknown))}")
        try:
            # collect() saves after every batch. A run that fetched nothing leaves the file alone, so it
            # produces no timestamp-only commit.
            collect(targets, cache, args.refresh or bool(args.only), features, args.spread and not args.only)
        except Stopped as err:   # render what was fetched, then fail the run below
            stopped = str(err)
        if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(summary, "a", encoding="utf-8") as output:
                output.write(freshness_summary(doc["projects"], cache, previous))

    report(doc["projects"], cache)
    if args.maintenance:
        write_atomic(Path(args.maintenance), maintenance_markdown(doc["projects"], cache))
    rows = build_rows(doc["projects"], cache)
    weekly = history.load(HISTORY_FILE)
    observed_at = NOW.isoformat(timespec="seconds")
    if not args.render_only and not args.only and not stopped:
        updated = any(r.get("fetched_at") == observed_at and not r.get("error") for r in rows)
        if updated and history.observe(weekly, rows, observed_at):
            write_atomic(HISTORY_FILE, json.dumps(weekly, indent=2, ensure_ascii=False) + "\n")
    write_atomic(EXPLORER_FILE, render_explorer(doc, rows, weekly["weeks"]))
    write_atomic(CSV_FILE, render_csv(rows))
    write_atomic(README_FILE, render_readme(doc, rows, features))
    print(f"rendered {README_FILE.name} and {CSV_FILE.name} for {len(rows)} projects")
    if stopped:
        sys.exit(stopped)


if __name__ == "__main__":
    main()
