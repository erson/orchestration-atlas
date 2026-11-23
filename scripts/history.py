"""Retain weekly catalog changes and one compact baseline for the next comparison."""

import json
import re
from datetime import datetime, timedelta

EVENTS = ("added", "resumed", "released")
STATUSES = {"Active", "Recent", "Slow", "Stale", "Archived", "Unavailable", "Not fetched"}
REPO = re.compile(r"[A-Za-z0-9-]+/[A-Za-z0-9._-]+")


def monday(day):
    return day - timedelta(days=day.weekday())


def utc_time(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() != timedelta():
        raise ValueError("history timestamps must be UTC")
    return parsed


def load(path):
    if not path.exists():
        return {"projects": {}, "weeks": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("projects"), dict):
        raise ValueError("history must contain a projects object")
    for repo, status in data["projects"].items():
        if not REPO.fullmatch(repo) or status not in STATUSES:
            raise ValueError(f"invalid history baseline for {repo}")
    weeks = data.get("weeks")
    if not isinstance(weeks, list) or not 1 <= len(weeks) <= 12:
        raise ValueError("history must contain between one and twelve observations")
    last = None
    for week in weeks:
        current = utc_time(week["at"])
        previous = utc_time(week["from"]) if week.get("from") else None
        if last is not None and (previous != last or monday(current.date()) <= monday(last.date())):
            raise ValueError("history observations must cover successive recorded weeks")
        if previous is not None and previous >= current:
            raise ValueError("invalid history comparison dates")
        for key in EVENTS:
            repos = week[key]
            if not isinstance(repos, list) or not all(isinstance(r, str) and REPO.fullmatch(r) for r in repos):
                raise ValueError(f"invalid history entries for {key}")
            if len({r.lower() for r in repos}) != len(repos) or (not previous and repos):
                raise ValueError(f"invalid history comparison for {key}")
        last = current
    return data


def observe(data, rows, timestamp):
    """Capture the first successful full-index observation of a UTC week. Replays leave it unchanged."""
    current = utc_time(timestamp)
    weeks = data["weeks"]
    last = utc_time(weeks[-1]["at"]) if weeks else None
    if last and monday(current.date()) <= monday(last.date()):
        return False
    before = {repo.lower(): status for repo, status in data["projects"].items()}
    week = {"at": current.isoformat(timespec="seconds"), "from": last.isoformat() if last else None,
            "added": [], "resumed": [], "released": []}
    projects = {}
    for row in sorted(rows, key=lambda r: r["repo"].lower()):
        repo, status = row["repo"], row["status"]
        projects[repo] = status
        if last is None:
            continue
        previous = before.get(repo.lower())
        if previous is None:
            week["added"].append(repo)
        if previous in ("Recent", "Slow", "Stale") and status == "Active":
            week["resumed"].append(repo)
    cutoff = monday(current.date()) - timedelta(weeks=11)
    data["weeks"] = [w for w in weeks if monday(utc_time(w["at"]).date()) >= cutoff] + [week]
    data["projects"] = projects
    return True


def reconcile_releases(data, rows):
    """Fill retained periods with releases found after a weekly observation."""
    periods = []
    first_added = {}
    for week in data["weeks"]:
        end = utc_time(week["at"])
        for repo in week["added"]:
            first_added.setdefault(repo.lower(), end)
        if week["from"]:
            periods.append((utc_time(week["from"]), end, week, {r.lower() for r in week["released"]}))
    if not periods:
        return False

    indexed = {repo.lower() for repo in data["projects"]}
    changed = False
    for row in rows:
        repo = row["repo"]
        key = repo.lower()
        published = row.get("latest_release_at")
        if key not in indexed or row.get("error") or not published:
            continue
        date = utc_time(published)
        for start, end, week, recorded in periods:
            if start < date <= end and first_added.get(key, end) <= end and key not in recorded:
                week["released"].append(repo)
                recorded.add(key)
                changed = True

    if changed:
        for _, _, week, _ in periods:
            week["released"].sort(key=str.lower)
    return changed
