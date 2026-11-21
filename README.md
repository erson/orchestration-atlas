# Orchestration Atlas

Find tools for running, coordinating, and supervising AI agents. Start with the task you need to do, then compare activity, releases, and maintenance across projects.

**[Open the explorer](https://erson.github.io/orchestration-atlas/)** · [Download for offline use](https://github.com/erson/orchestration-atlas/raw/refs/heads/main/catalog.html) · [Browse the searchable CSV on GitHub](data/projects.csv) · [Methodology](#methodology)

Filter by task, feature, language, or activity and compare up to four projects side by side. Inspect a project against category peers, select a region of the project map, or copy a link to your comparison. The downloadable edition also works offline.

```text
+----- [ INDEX SNAPSHOT ] ----+
|                             |
|  Available projects   640   |
|  Active in 30 days    455   |
|  Combined stars       3.7M  |
|                             |
+-----------------------------+
```

*Metrics collected 2026-11-15 to 2026-11-21 (UTC). The index tracks 645 projects across 9 categories.*

## Choose a task

- [Orchestrator.inc](https://github.com/OrchestratorInc/agent-orchestrator) — Route failed CI checks and review comments to the agent that owns the branch.
- [Emdash](https://github.com/generalaction/emdash) — Run agents in separate Git worktrees and compare their diffs.
- [Mission Control](https://github.com/builderz-labs/mission-control) _(new)_ — Track spending alongside agent runs in a self-hosted dashboard.

| I want to… | Indexed | Commit within 90 days |
|---|---:|---:|
| [Run parallel coding sessions in a terminal](#parallel-coding-agents--terminal-tuicli) | 61 | 52 |
| [Manage coding agents in a desktop or web UI](#parallel-coding-agents--desktop--web) | 192 | 169 |
| [Coordinate a team of agents](#multi-agent-swarms) | 116 | 89 |
| [Repeat an agent loop until a condition is met](#autonomous-loop-runners) | 31 | 21 |
| [Delegate a task to an autonomous runner](#autonomous-task-runners) | 58 | 46 |
| [Build on orchestration infrastructure](#agent-infrastructure--primitives) | 84 | 72 |
| [Set up a personal assistant](#personal-assistants) | 58 | 49 |
| [Explore the resting collection](#resting) | 17 | 1 |
| [Build with a general-purpose agent SDK](#adjacent-frameworks-general-purpose-agent-sdks) | 28 | 23 |

## Read the signals

Use **last commit** for recency, **latest release** for shipping cadence, and **contributors** alongside **top author share** for maintenance concentration. Stars measure attention. Feature matches come from project text and need checking against its docs.

<details><summary>At a glance</summary>

| Projects tracked | Total stars | Median contributors | Median days since last commit |
|:-:|:-:|:-:|:-:|
| **645** | **3,706,794** | **7** | **3** |

| 🟢 Active | 🟡 Recent | 🟠 Slow | 🔴 Stale | 📦 Archived | ⚫ Unavailable |
|:-:|:-:|:-:|:-:|:-:|:-:|
| **455** | **67** | **111** | **3** | **4** | **5** |

Status is the age of the last commit on the default branch: Active up to 30 days, Recent up to 90, Slow up to a year, Stale beyond that. See [Methodology](#methodology).

</details>

<details><summary>Features</summary>

Share of the 640 projects whose README, description, or topics mention each feature. Keyword matching, so treat it as a rough guide; see [Methodology](#methodology). Per-project features are in the interactive explorer and in `data/projects.csv`.

| Group | Mentioned by |
|---|---|
| **Agents** | Claude Code **78%** · Codex **74%** · OpenCode **49%** · Cursor **39%** · Copilot **25%** · Gemini CLI **23%** · Kiro **8%** · Qwen Code **7%** · Aider **7%** · Cline **7%** · Goose **5%** · Amp **3%** |
| **Isolation** | Git worktrees **45%** · Containers **41%** · Sandbox / VM **38%** · tmux **21%** |
| **Interface** | Desktop app **35%** · Web UI **29%** · TUI **25%** · Mobile **14%** · IDE extension **2%** |
| **Protocols** | MCP **55%** · ACP **15%** · A2A **5%** |
| **Workflow** | Scheduled runs **21%** · Kanban / task board **17%** |

</details>

<details><summary>Languages</summary>

| Main language | Projects | Share | |
|---|--:|--:|---|
| TypeScript | 296 | 47% | `████████████████████` |
| Python | 110 | 17% | `███████░░░░░░░░░░░░░` |
| Rust | 74 | 12% | `█████░░░░░░░░░░░░░░░` |
| Go | 60 | 9% | `████░░░░░░░░░░░░░░░░` |
| JavaScript | 35 | 6% | `██░░░░░░░░░░░░░░░░░░` |
| Shell | 22 | 3% | `█░░░░░░░░░░░░░░░░░░░` |
| Swift | 15 | 2% | `█░░░░░░░░░░░░░░░░░░░` |
| Elixir | 5 | 1% | `█░░░░░░░░░░░░░░░░░░░` |
| C# | 4 | 1% | `█░░░░░░░░░░░░░░░░░░░` |
| Zig | 4 | 1% | `█░░░░░░░░░░░░░░░░░░░` |

</details>

<details><summary>Top 15 by stars</summary>

| # | Project | Category | Stars | Contributors | Status |
|--:|---|---|--:|--:|---|
| 1 | [openclaw](https://github.com/openclaw/openclaw) | Assistants | 394,509 | 376 | 🟢 Active |
| 2 | [hermes-agent](https://github.com/NousResearch/hermes-agent) | Assistants | 264,092 | 399 | 🟢 Active |
| 3 | [Orca](https://github.com/stablyai/orca) | Desktop & web | 125,454 | 464 | 🟢 Active |
| 4 | [paperclip](https://github.com/paperclipai/paperclip) | Swarms | 115,587 | 243 | 🟢 Active |
| 5 | [OpenHands](https://github.com/OpenHands/OpenHands) | Task runners | 93,637 | 456 | 🟢 Active |
| 6 | [DeerFlow](https://github.com/bytedance/deer-flow) _(new)_ | Adjacent frameworks | 85,480 | 454 | 🟢 Active |
| 7 | [ruflo](https://github.com/ruvnet/ruflo) | Swarms | 82,196 | 87 | 🟢 Active |
| 8 | [MetaGPT](https://github.com/FoundationAgents/MetaGPT) | Adjacent frameworks | 71,292 | 116 | 🟠 Slow |
| 9 | [OmO](https://github.com/code-yeongyu/oh-my-openagent) _(new)_ | Swarms | 70,986 | 333 | 🟢 Active |
| 10 | [t3code](https://github.com/pingdotgg/t3code) | Desktop & web | 68,744 | 474 | 🟢 Active |
| 11 | [AutoGen](https://github.com/microsoft/autogen) | Adjacent frameworks | 61,955 | 440 | 🟢 Active |
| 12 | [crewAI](https://github.com/crewAIInc/crewAI) | Swarms | 61,067 | 367 | 🟢 Active |
| 13 | [multica](https://github.com/multica-ai/multica) | Task runners | 56,887 | 406 | 🟢 Active |
| 14 | [herdr](https://github.com/herdrdev/herdr) | Terminal | 51,842 | 87 | 🟢 Active |
| 15 | [nanobot](https://github.com/HKUDS/nanobot) | Assistants | 50,123 | 394 | 🟢 Active |

</details>

<details><summary>Most recent commits</summary>

| # | Project | Category | Last commit | Commits (90d) | Status |
|--:|---|---|---|--:|---|
| 1 | [Loushang](https://github.com/zhnt/loushang) _(new)_ | Infrastructure | 2026-11-21 | 3,122 | 🟢 Active |
| 2 | [t3code](https://github.com/pingdotgg/t3code) | Desktop & web | 2026-11-21 | 10,123 | 🟢 Active |
| 3 | [ordewell](https://github.com/ordewell/ordewell) | Loop runners | 2026-11-21 | 3,490 | 🟢 Active |
| 4 | [OpenChamber](https://github.com/openchamber/openchamber) | Desktop & web | 2026-11-21 | 4,801 | 🟢 Active |
| 5 | [row-bot](https://github.com/siddsachar/row-bot) | Assistants | 2026-11-21 | 3,932 | 🟢 Active |
| 6 | [paperclip](https://github.com/paperclipai/paperclip) | Swarms | 2026-11-21 | 4,619 | 🟢 Active |
| 7 | [sortie](https://github.com/sortie-ai/sortie) | Task runners | 2026-11-21 | 1,963 | 🟢 Active |
| 8 | [bernstein](https://github.com/sipyourdrink-ltd/bernstein) | Loop runners | 2026-11-21 | 1,991 | 🟢 Active |
| 9 | [Speakeasy control plane](https://github.com/speakeasy-api/gram) | Infrastructure | 2026-11-21 | 2,753 | 🟢 Active |
| 10 | [MulmoTerminal](https://github.com/receptron/mulmoterminal) | Desktop & web | 2026-11-21 | 3,877 | 🟢 Active |
| 11 | [Althar](https://github.com/AltharIDE/althar) _(new)_ | Desktop & web | 2026-11-21 | 850 | 🟢 Active |
| 12 | [Claudexor](https://github.com/razzant/claudexor) | Infrastructure | 2026-11-21 | 1,847 | 🟢 Active |
| 13 | [Superagent](https://github.com/pungme/superagent-desktop) | Desktop & web | 2026-11-21 | 957 | 🟢 Active |
| 14 | [Agentbox](https://github.com/savannahfeder/agentbox) | Desktop & web | 2026-11-21 | 5,402 | 🟢 Active |
| 15 | [switch](https://github.com/sandbox-quantum/switch) _(new)_ | Assistants | 2026-11-21 | 2,292 | 🟢 Active |

</details>

<details><summary>Single-maintainer risk</summary>

| Project | Top author share | Contributors | Commits (all time) | Status |
|---|--:|--:|--:|---|
| [amux](https://github.com/andyrewlee/amux) | 100% | 1 | 1,126 | 🟢 Active |
| [Calyx](https://github.com/yuuichieguchi/Calyx) | 100% | 1 | 967 | 🟢 Active |
| [openkanban](https://github.com/TechDufus/openkanban) | 100% | 1 | 118 | 🟠 Slow |
| [tmux-ide](https://github.com/wavyrai/tmux-ide) | 100% | 2 | 4,278 | 🟢 Active |
| [Craig](https://github.com/hallsamuel90/craig) | 100% | 1 | 307 | 🟢 Active |
| [Mercury CLI](https://github.com/Whq02/MercuryCLI) | 100% | 1 | 14,883 | 🟢 Active |
| [pando](https://github.com/xseman/pando) | 100% | 1 | 528 | 🟢 Active |
| [pohunek](https://github.com/zajca/pohunek) | 100% | 1 | 4,463 | 🟢 Active |
| [taskpods](https://github.com/yanairon/taskpods) | 100% | 1 | 129 | 🟡 Recent |
| [OpenCode Mission Control](https://github.com/nigel-dev/opencode-mission-control) _(new)_ | 100% | 1 | 154 | 🟠 Slow |

</details>

## Parallel Coding Agents — Terminal (TUI/CLI)

Run and supervise several agent sessions side by side from a terminal — tmux panes, git worktrees, and TUI dashboards.

<details><summary>Browse 61 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [abtop](https://github.com/graykode/abtop) _(new)_ | 🟡 Recent | Rust |
| [AgEnD Terminal](https://github.com/suzuke/agend-terminal) _(new)_ | 🟡 Recent | Rust |
| [Agent CLI Farm](https://github.com/waskosky/agent-cli-farm) _(new)_ | 🟢 Active | Python |
| [agent-console](https://github.com/buhuipao/agent-console) | 🟡 Recent | Rust |
| [agent-deck](https://github.com/asheshgoplani/agent-deck) | 🟢 Active | Go |
| [agent-manager](https://github.com/wainmann/agent-manager) | 🟢 Active | Go |
| [agent-of-empires](https://github.com/agent-of-empires/agent-of-empires) | 🟢 Active | Rust |
| [agent-session-manager](https://github.com/izll/agent-session-manager) | 🟡 Recent | Go |
| [agentbox](https://github.com/madarco/agentbox) | 🟡 Recent | TypeScript |
| [agents-in-a-box](https://github.com/stevengonsalvez/agents-in-a-box) _(new)_ | 🟡 Recent | Rust |
| [agentvm](https://github.com/Twigpine/agentvm) _(new)_ | 🟠 Slow | Shell |
| [agterm](https://github.com/umputun/agterm) | 🟢 Active | Swift |
| [agtx](https://github.com/fynnfluegge/agtx) _(new)_ | 🟢 Active | Rust |
| [ai-devkit](https://github.com/codeaholicguy/ai-devkit) | 🟢 Active | TypeScript |
| [amux](https://github.com/andyrewlee/amux) | 🟢 Active | Go |
| [amux (mixpeek)](https://github.com/mixpeek/amux) | 🟢 Active | Rust |
| [Calyx](https://github.com/yuuichieguchi/Calyx) | 🟢 Active | Swift |
| [Claude Code tmux Orchestration](https://github.com/primeline-ai/claude-tmux-orchestration) _(new)_ | 🟠 Slow | Shell |
| [claude-squad](https://github.com/smtg-ai/claude-squad) | 🟢 Active | Go |
| [claude-tmux](https://github.com/nielsgroen/claude-tmux) _(new)_ | 🟠 Slow | Rust |
| [CLI Agent Orchestrator (CAO)](https://github.com/awslabs/cli-agent-orchestrator) _(new)_ | 🟢 Active | Python |
| [cmux](https://github.com/manaflow-ai/cmux) | 🟢 Active | Swift |
| [Craig](https://github.com/hallsamuel90/craig) | 🟢 Active | TypeScript |
| [Cyclops](https://github.com/cyclops-team/cyclops) | 🟡 Recent | Rust |
| [DevThrottle](https://github.com/thefrederiksen/devthrottle) | 🟢 Active | — |
| [dmux](https://github.com/standardagents/dmux) | 🟠 Slow | HTML |
| [Gentle Shell](https://github.com/Gentleman-Programming/gentle-shell) _(new)_ | 🟢 Active | TypeScript |
| [GridBash](https://github.com/jasonsuhari/gridbash) _(new)_ | 🟢 Active | Rust |
| [herdr](https://github.com/herdrdev/herdr) | 🟢 Active | Rust |
| [herduck](https://github.com/wenhanweime/herduck) | 🟢 Active | Rust |
| [HexoKit](https://github.com/sahil87/hexokit) _(new)_ | 🟢 Active | TypeScript |
| [hydra-acp](https://github.com/smagnuso/hydra-acp) _(new)_ | 🟢 Active | TypeScript |
| [jmux](https://github.com/jarredkenny/jmux) _(new)_ | 🟡 Recent | TypeScript |
| [Mercury CLI](https://github.com/Whq02/MercuryCLI) | 🟢 Active | TypeScript |
| [NTM](https://github.com/Dicklesworthstone/ntm) _(new)_ | 🟢 Active | Go |
| [OpenCode Mission Control](https://github.com/nigel-dev/opencode-mission-control) _(new)_ | 🟠 Slow | TypeScript |
| [opencode-kanban](https://github.com/TomCC7/opencode-kanban) _(new)_ | 🟡 Recent | Rust |
| [openkanban](https://github.com/TechDufus/openkanban) | 🟠 Slow | Go |
| [opensessions](https://github.com/Ataraxy-Labs/opensessions) _(new)_ | 🟠 Slow | Rust |
| [Orchestra](https://github.com/humanunsupervised/orchestra) _(new)_ | 🟡 Recent | — |
| [pando](https://github.com/xseman/pando) | 🟢 Active | Go |
| [Pane](https://github.com/greenfield-inc/Pane) _(new)_ | 🟢 Active | TypeScript |
| [pappardelle](https://github.com/chardigio/pappardelle) | 🟢 Active | TypeScript |
| [pohunek](https://github.com/zajca/pohunek) | 🟢 Active | Rust |
| [Prowl](https://github.com/onevcat/Prowl) | 🟢 Active | Swift |
| [ReevesAgents](https://github.com/mertkayacs/reevesagents) | 🟢 Active | TypeScript |
| [repomon](https://github.com/AliHamzaAzam/repomon) | 🟡 Recent | Rust |
| [Rove](https://github.com/Sma1lboy/rove) | 🟢 Active | TypeScript |
| [Rune](https://github.com/unstablebuild/rune) _(new)_ | 🟢 Active | Go |
| [taskpods](https://github.com/yanairon/taskpods) | 🟡 Recent | Python |
| [termany](https://github.com/thinkany-ai/termany) | 🟢 Active | TypeScript |
| [Termio](https://github.com/termio-sh/termio) | 🟢 Active | Swift |
| [thurbox](https://github.com/Thurbeen/thurbox) | 🟢 Active | Rust |
| [tmux-agent-sidebar](https://github.com/hiroppy/tmux-agent-sidebar) _(new)_ | 🟢 Active | Rust |
| [tmux-claude-hatch](https://github.com/craftzdog/tmux-claude-hatch) _(new)_ | 🟡 Recent | Shell |
| [tmux-ide](https://github.com/wavyrai/tmux-ide) | 🟢 Active | TypeScript |
| [TmuxCC](https://github.com/nyanko3141592/tmuxcc) _(new)_ | 🟠 Slow | Rust |
| [Toad](https://github.com/batrachianai/toad) _(new)_ | 🟠 Slow | Python |
| [tuios](https://github.com/Gaurav-Gosain/tuios) _(new)_ | 🟢 Active | Go |
| [Vigil](https://github.com/butterlatte-zhang/vigil) | 🟡 Recent | Swift |
| [YYLO](https://github.com/yylo-dev/yylo) | 🟡 Recent | Python |

</details>

[Back to tasks](#choose-a-task)

## Parallel Coding Agents — Desktop & Web

The same parallel-sessions workflow as a desktop app or browser/mobile dashboard, with diff review and merge.

<details><summary>Browse 192 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [ADE](https://github.com/arul28/ADE) _(new)_ | 🟢 Active | TypeScript |
| [ADHDev](https://github.com/vilmire/adhdev) _(new)_ | 🟢 Active | TypeScript |
| [Agent Console](https://github.com/cyl-castillo/agent-console) | 🟢 Active | Rust |
| [Agent Flow](https://github.com/patoles/agent-flow) _(new)_ | 🟢 Active | TypeScript |
| [agent-session-manager-desktop](https://github.com/izll/agent-session-manager-desktop) | 🟢 Active | Go |
| [agent-squid](https://github.com/agent-squid/squid) | 🟢 Active | Python |
| [Agentbox](https://github.com/savannahfeder/agentbox) | 🟢 Active | TypeScript |
| [agentglass](https://github.com/SirAllap/agentglass) | 🟢 Active | TypeScript |
| [AgentHub](https://github.com/jamesrochabrun/AgentHub) _(new)_ | 🟠 Slow | Swift |
| [AgentOS](https://github.com/SapienXai/AgentOS) _(new)_ | 🟢 Active | TypeScript |
| [Agentrove](https://github.com/Mng-dev-ai/agentrove) _(new)_ | 🟢 Active | TypeScript |
| [AgentWire](https://github.com/dotdevdotdev/agentwire-dev) _(new)_ | 🟢 Active | Python |
| [Agetor](https://github.com/alamops/agetor) | 🟢 Active | TypeScript |
| [AGNT](https://github.com/agnt-gg/agnt) _(new)_ | 🟢 Active | JavaScript |
| [Agor](https://github.com/preset-io/agor) _(new)_ | 🟢 Active | TypeScript |
| [AGX](https://github.com/ramarlina/agx) | 🟠 Slow | TypeScript |
| [ai-maestro](https://github.com/23blocks-OS/ai-maestro) | 🟢 Active | TypeScript |
| [AI4Kanban](https://github.com/wildcrane-ai/wildcrane) | 🟢 Active | TypeScript |
| [AionUi](https://github.com/iOfficeAI/AionUi) _(new)_ | 🟢 Active | TypeScript |
| [aizen](https://github.com/vivy-company/aizen) | 🟠 Slow | Swift |
| [alas](https://github.com/mrmans0n/alas) | 🟢 Active | Swift |
| [Alchemist Coder](https://github.com/Alekla0126/alchemist-coder) | 🟢 Active | TypeScript |
| [Alethe](https://github.com/Kc1t/alethe-agents) | 🟢 Active | TypeScript |
| [Althar](https://github.com/AltharIDE/althar) _(new)_ | 🟢 Active | TypeScript |
| [Antumi](https://github.com/flyhero/antumi) | 🟢 Active | TypeScript |
| [Aperant](https://github.com/AndyMik90/Aperant) | 🟠 Slow | TypeScript |
| [Arbor](https://github.com/penso/arbor) _(new)_ | 🟢 Active | Rust |
| [Async Code Agent](https://github.com/ObservedObserver/async-code) _(new)_ | 🔴 Stale | TypeScript |
| [ateam](https://github.com/clawnify/ateam) | 🟢 Active | TypeScript |
| [Atlas](https://github.com/tryatlas/atlas) _(new)_ | 🟢 Active | TypeScript |
| [automaker](https://github.com/AutoMaker-Org/automaker) | 🟠 Slow | TypeScript |
| [bb](https://github.com/get-bb/bb) | 🟢 Active | TypeScript |
| [Berd](https://github.com/block/berd) | 🟢 Active | TypeScript |
| [Caprock](https://github.com/dspv/caprock) | 🟢 Active | Go |
| [Cate](https://github.com/0-AI-UG/cate) _(new)_ | 🟢 Active | TypeScript |
| [cc-haha](https://github.com/NanmiCoder/cc-haha) _(new)_ | 🟢 Active | TypeScript |
| [Cezar](https://github.com/open-mercato/cezar) _(new)_ | 🟢 Active | TypeScript |
| [ChatML](https://github.com/chatml/chatml) _(new)_ | 🟠 Slow | TypeScript |
| [Claude Command Center (CCC)](https://github.com/amirfish1/claude-command-center) | 🟢 Active | Python |
| [Claude Control](https://github.com/sverrirsig/claude-control) _(new)_ | 🟡 Recent | TypeScript |
| [Claudette](https://github.com/utensils/claudette) | 🟢 Active | TypeScript |
| [clave](https://github.com/antasphere/clave) | 🟡 Recent | TypeScript |
| [ClawPort](https://github.com/JohnRiceML/clawport-ui) _(new)_ | 🟠 Slow | TypeScript |
| [ClawSuite](https://github.com/outsourc-e/clawsuite) _(new)_ | 🟠 Slow | TypeScript |
| [ClawX](https://github.com/ValueCell-ai/ClawX) _(new)_ | 🟢 Active | TypeScript |
| [clideck](https://github.com/rustykuntz/clideck) | 🟢 Active | JavaScript |
| [Cloudroom](https://github.com/davidondrej/cloudroom) | 🟢 Active | TypeScript |
| [Codeg](https://github.com/spacering-net/codeg) _(new)_ | 🟢 Active | Rust |
| [CodeNomad](https://github.com/NeuralNomadsAI/CodeNomad) | 🟢 Active | TypeScript |
| [collaborator](https://github.com/collabs-inc/collab-public) | 🟠 Slow | TypeScript |
| [Collie](https://github.com/AltanS/collie) _(new)_ | 🟢 Active | TypeScript |
| [constellagent](https://github.com/owengretzinger/constellagent) | 🟠 Slow | TypeScript |
| [Crystal](https://github.com/stravu/crystal) _(new)_ | 🟠 Slow | TypeScript |
| [Delegatus](https://github.com/Latand/delegatus) | 🟢 Active | TypeScript |
| [dev-3.0](https://github.com/h0x91b/dev-3.0) | 🟢 Active | TypeScript |
| [diri](https://github.com/cristicretu/diri) | 🟢 Active | Rust |
| [DockTerm](https://github.com/munvard/dockterm) | 🟡 Recent | TypeScript |
| [dorothy](https://github.com/Charlie85270/Dorothy) | 🟢 Active | TypeScript |
| [Dray](https://github.com/monorepo-labs/dray) | 🟢 Active | Rust |
| [Ekko Studio](https://github.com/EKKOLearnAI/ekko-studio) _(new)_ | 🟢 Active | TypeScript |
| [Emdash](https://github.com/generalaction/emdash) | 🟢 Active | TypeScript |
| [EvoFlux](https://github.com/evoelsewhere/evo-harness) | 🟢 Active | Rust |
| [FleetCode](https://github.com/built-by-as/FleetCode) _(new)_ | 🟠 Slow | TypeScript |
| [Fletch](https://github.com/fwdai/fletch) | 🟢 Active | Rust |
| [Flock](https://github.com/Onelevenvy/flock) _(new)_ | 🟠 Slow | Rust |
| [Friday](https://github.com/splashxmoon/friday) | 🟢 Active | TypeScript |
| [Garcon](https://github.com/cfal/garcon) | 🟢 Active | TypeScript |
| [Gas Town GUI](https://github.com/web3dev1337/gastown-gui) _(new)_ | 🟡 Recent | JavaScript |
| [Ghostex](https://github.com/maddada/Ghostex) | 🟢 Active | Rust |
| [Gold Band](https://github.com/diodeme/Gold-Band) _(new)_ | 🟢 Active | Rust |
| [GraphCode](https://github.com/scgopi/GraphCode) | 🟢 Active | Swift |
| [Grasp](https://github.com/cocofhu/grasp) _(new)_ | 🟢 Active | TypeScript |
| [Happier](https://github.com/happier-dev/happier) | 🟢 Active | TypeScript |
| [Happy](https://github.com/slopus/happy) | 🟢 Active | Swift |
| [Harness by Autonomous](https://github.com/autonomous-ai/openharness) | 🟢 Active | TypeScript |
| [Harness Remote](https://github.com/giuliastro/harness-remote) _(new)_ | 🟢 Active | JavaScript |
| [Harnss](https://github.com/OpenSource03/harnss) _(new)_ | 🟠 Slow | TypeScript |
| [HashCortX](https://github.com/Hash-7777/HashCortX) _(new)_ | 🟢 Active | JavaScript |
| [Helicon](https://github.com/HarjjotSinghh/helicon) | 🟢 Active | TypeScript |
| [Helmor](https://github.com/dohooo/helmor) _(new)_ | 🟠 Slow | TypeScript |
| [herdr-app](https://github.com/herdrdev/herdr-app) | 🟢 Active | Rust |
| [Hermes Studio](https://github.com/JPeetz/Hermes-Studio) _(new)_ | 🟠 Slow | TypeScript |
| [Hive](https://github.com/morapelker/hive) _(new)_ | 🟢 Active | TypeScript |
| [humanlayer](https://github.com/humanlayer/humanlayer) | 🟢 Active | TypeScript |
| [IM.codes](https://github.com/im4codes/imcodes) | 🟢 Active | TypeScript |
| [Intent](https://github.com/intent-hq/intent) | 🟢 Active | JavaScript |
| [intentic](https://github.com/intentic/intentic) | 🟢 Active | TypeScript |
| [iPolloWork](https://github.com/Devin-AXIS/iPolloWork) _(new)_ | 🟢 Active | TypeScript |
| [ivy-tendril](https://github.com/Ivy-Interactive/Ivy-Tendril) | 🟡 Recent | C# |
| [jean](https://github.com/coollabsio/jean) | 🟢 Active | TypeScript |
| [JockeyUI](https://github.com/recailai/jockey) _(new)_ | 🟢 Active | Rust |
| [Kanban](https://github.com/cline/kanban) _(new)_ | 🟢 Active | TypeScript |
| [Kander](https://github.com/dualface/kander) | 🟢 Active | Go |
| [kandev](https://github.com/kdlbs/kandev) | 🟢 Active | Go |
| [Kangentic](https://github.com/Kangentic/kangentic) | 🟢 Active | TypeScript |
| [KanVibe](https://github.com/rookedsysc/kanvibe) _(new)_ | 🟢 Active | TypeScript |
| [Kimaki](https://github.com/remorses/kimaki) _(new)_ | 🟢 Active | TypeScript |
| [Ling Stack](https://github.com/ling-stack-org/ling-stack) _(new)_ | 🟢 Active | TypeScript |
| [Lookout for VS Code](https://github.com/nimrod-teich/lookout) | 🟢 Active | TypeScript |
| [Luvus](https://github.com/RizRiyz/luvus) _(new)_ | 🟢 Active | Rust |
| [Maestro](https://github.com/RunMaestro/Maestro) _(new)_ | 🟢 Active | TypeScript |
| [Meldwork](https://github.com/Ryder-Sun/Meldwork) _(new)_ | 🟢 Active | JavaScript |
| [Mexus](https://github.com/yofine/Mexus) _(new)_ | 🟠 Slow | TypeScript |
| [Monet](https://github.com/zenolab124/monet) _(new)_ | 🟢 Active | Rust |
| [MonoCode](https://github.com/hardbeat920/monocode) | 🟢 Active | Rust |
| [Moonfold](https://github.com/Mr-Dark-debug/Moonfold) | 🟢 Active | TypeScript |
| [MulmoTerminal](https://github.com/receptron/mulmoterminal) | 🟢 Active | TypeScript |
| [MultiCC](https://github.com/lsjwzh/MultiCC) | 🟢 Active | JavaScript |
| [muxel](https://github.com/ProjectHax/muxel) | 🟢 Active | Rust |
| [Muxflow](https://github.com/gal064/muxflow) | 🟢 Active | TypeScript |
| [nimbalyst](https://github.com/nimbalyst/nimbalyst) | 🟢 Active | TypeScript |
| [nodeterm](https://github.com/eneskirca/nodeterm) _(new)_ | 🟢 Active | TypeScript |
| [Novadeck](https://github.com/novadeck-org/novadeck) | 🟢 Active | TypeScript |
| [Nuphos](https://github.com/nuphos/nuphos) | 🟢 Active | TypeScript |
| [octomux](https://github.com/ShreyPaharia/octomux) | 🟡 Recent | TypeScript |
| [omg.dev](https://github.com/BennyKok/omg.dev) | 🟢 Active | TypeScript |
| [opcode](https://github.com/winfunc/opcode) _(new)_ | 🟢 Active | TypeScript |
| [Open Session](https://github.com/tellahq/opensession) | 🟢 Active | TypeScript |
| [Open Walnut](https://github.com/EvanZhang008/open-walnut) | 🟢 Active | TypeScript |
| [OpenAgents](https://github.com/openagents-org/openagents) _(new)_ | 🟢 Active | TypeScript |
| [OpenChamber](https://github.com/openchamber/openchamber) | 🟢 Active | TypeScript |
| [OpenClawdex](https://github.com/alekseyrozh/openclawdex) _(new)_ | 🟠 Slow | TypeScript |
| [OpenCove](https://github.com/DeadWaveWave/opencove) _(new)_ | 🟢 Active | TypeScript |
| [opendray](https://github.com/Opendray/opendray) _(new)_ | 🟢 Active | Dart |
| [OpenTandem](https://github.com/opentandem/opentandem) | 🟢 Active | JavaScript |
| [Operator](https://github.com/iishyfishyy/operator-oss) _(new)_ | 🟡 Recent | TypeScript |
| [Orb](https://github.com/Th0rgal/orb) _(new)_ | 🟢 Active | Lean |
| [Orbital](https://github.com/zqiren/Orbital) _(new)_ | 🟢 Active | Python |
| [Orca](https://github.com/stablyai/orca) | 🟢 Active | TypeScript |
| [Orchestration War Room](https://github.com/Naroh091/hermes-war-room) _(new)_ | 🟡 Recent | Vue |
| [Orchestrator.inc](https://github.com/OrchestratorInc/agent-orchestrator) | 🟢 Active | TypeScript |
| [Ouijit](https://github.com/ouijit/ouijit) | 🟢 Active | TypeScript |
| [PandaCode](https://github.com/aicodeking/pandacode) | 🟢 Active | TypeScript |
| [Paradev](https://github.com/ParadevAI/Paradev) | 🟢 Active | TypeScript |
| [parallel-code](https://github.com/johannesjo/parallel-code) | 🟢 Active | TypeScript |
| [Paseo](https://github.com/getpaseo/paseo) | 🟢 Active | TypeScript |
| [Perch](https://github.com/asafofer/perch) | 🟢 Active | Swift |
| [Pi Dash](https://github.com/The-AI-Republic/pi-dash) _(new)_ | 🟢 Active | TypeScript |
| [pitwall](https://github.com/quanticstudios/pitwall) | 🟢 Active | Go |
| [Pocket Server](https://github.com/yayasoumah/pocket-server) _(new)_ | 🔴 Stale | TypeScript |
| [Podium ADE](https://github.com/madeinorbit/podium) | 🟢 Active | TypeScript |
| [Polpo](https://github.com/pugliatechs/polpo) _(new)_ | 🟢 Active | JavaScript |
| [Poracode](https://github.com/Porabuild/Poracode) | 🟢 Active | TypeScript |
| [Pragma](https://github.com/pragma-sh/pragma) | 🟢 Active | TypeScript |
| [Proliferate](https://github.com/proliferate-ai/proliferate) | ⚫ Unavailable | — |
| [Prometeu](https://github.com/prometeucorp/prometeu) | 🟢 Active | Rust |
| [qm](https://github.com/yc-software/qm) | 🟢 Active | TypeScript |
| [Reemoat](https://github.com/rends-east/reemoat) | 🟡 Recent | TypeScript |
| [Roamgate](https://github.com/powerfooI/roamgate) | 🟢 Active | TypeScript |
| [Runner](https://github.com/yicheng47/runner) | 🟢 Active | Rust |
| [Sculptor](https://github.com/imbue-ai/sculptor) _(new)_ | 🟢 Active | Python |
| [Sesori](https://github.com/sesori-ai/sesori_apps_monorepo) | 🟢 Active | Dart |
| [Sillage](https://github.com/MarlBurroW/sillage) | 🟢 Active | TypeScript |
| [Skiff](https://github.com/solutionscay/skiff) | 🟢 Active | Rust |
| [SoduWork](https://github.com/mdiri-ai/SoduWork) _(new)_ | 🟢 Active | JavaScript |
| [Solenta](https://github.com/currentbits/solenta) | 🟢 Active | JavaScript |
| [SpaceApp](https://github.com/oll4com/spaceapp) | 🟢 Active | TypeScript |
| [stagewise](https://github.com/stagewise-io/stagewise) _(new)_ | 🟢 Active | TypeScript |
| [supacode](https://github.com/supabitapp/supacode) | 🟢 Active | Swift |
| [Superagent](https://github.com/pungme/superagent-desktop) | 🟢 Active | TypeScript |
| [synara](https://github.com/Emanuele-web04/synara) | 🟢 Active | TypeScript |
| [t3code](https://github.com/pingdotgg/t3code) | 🟢 Active | TypeScript |
| [takopi](https://github.com/banteg/takopi) | 🟠 Slow | Python |
| [Talavine Code](https://github.com/scrossen/talavine-code) _(new)_ | 🟢 Active | C# |
| [TaskHandoff](https://github.com/edgestorage/task-handoff) | 🟢 Active | TypeScript |
| [Tempest](https://github.com/tempestai-dev/tempest) | 🟢 Active | TypeScript |
| [Termexo](https://github.com/gemron/Termexo) _(new)_ | 🟢 Active | TypeScript |
| [Termic](https://github.com/simion/termic) _(new)_ | 🟢 Active | TypeScript |
| [Threadlines](https://github.com/Threadlines/threadlines) | 🟢 Active | TypeScript |
| [tlbx](https://github.com/tlbx-ai/tlbx) | 🟢 Active | C# |
| [Tortie](https://github.com/gregce/tortie) | 🟢 Active | TypeScript |
| [Traycer](https://github.com/traycerai/traycer) | 🟢 Active | TypeScript |
| [TUICommander](https://github.com/sstraus/tuicommander) _(new)_ | 🟢 Active | Rust |
| [UpComputer](https://github.com/krl-gr/upcomputer) | 🟢 Active | TypeScript |
| [Verde](https://github.com/JonathanRiche/verde) | 🟢 Active | Zig |
| [vibe-tree](https://github.com/sahithvibudhi/vibe-tree) | 🟠 Slow | TypeScript |
| [vibecraft](https://github.com/rayzhudev/vibecraft) | 🟢 Active | TypeScript |
| [vibepanel](https://github.com/jiangmuran/vibepanel) _(new)_ | 🟢 Active | Go |
| [Vibex](https://github.com/vibex-ai/vibex) _(new)_ | 🟢 Active | Rust |
| [Vibeyard](https://github.com/elirantutia/vibeyard) _(new)_ | 🟢 Active | TypeScript |
| [Vicoa](https://github.com/vicoa-ai/vicoa) | 🟢 Active | Python |
| [Volt](https://github.com/LeulAria/volt) | 🟢 Active | TypeScript |
| [Waku](https://github.com/egoist/waku) | 🟡 Recent | Rust |
| [wmux](https://github.com/openwong2kim/wmux) | 🟢 Active | TypeScript |
| [WSP](https://github.com/wsp-labs/wsp) | 🟢 Active | TypeScript |
| [xum](https://github.com/coder/xum) | 🟢 Active | TypeScript |
| [Yao Agents](https://github.com/YaoApp/yao) _(new)_ | 🟢 Active | Go |
| [Yardlet](https://github.com/zzunkie/yardlet) | 🟢 Active | Swift |
| [Yardsort](https://github.com/joaoh82/yardsort) | 🟢 Active | Rust |
| [Zaivern Code](https://github.com/tacyan/zaivern-code) | 🟡 Recent | Rust |
| [Zeron](https://github.com/zeronsh/zeron) | 🟢 Active | Rust |
| [zuse](https://github.com/swarajbachu/zuse) | 🟢 Active | TypeScript |

</details>

[Back to tasks](#choose-a-task)

## Multi-Agent Swarms

Systems where multiple specialized agents actively coordinate, communicate, and delegate toward a shared goal.

<details><summary>Browse 116 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [5dive](https://github.com/5dive-ai/5dive) | 🟢 Active | Shell |
| [Agent Teams](https://github.com/777genius/agent-teams-ai) | 🟢 Active | TypeScript |
| [agent-kanban](https://github.com/saltbo/agent-kanban) | 🟢 Active | TypeScript |
| [agent-swarm](https://github.com/desplega-ai/agent-swarm) _(new)_ | 🟢 Active | TypeScript |
| [AgentArea](https://github.com/agentarea/agentarea) _(new)_ | 🟢 Active | Python |
| [AgentBridge](https://github.com/raysonmeng/agent-bridge) | 🟡 Recent | TypeScript |
| [AgentHub](https://github.com/Dmatut7/AgentHub) _(new)_ | 🟠 Slow | Python |
| [Agents Squads](https://github.com/agents-squads/squads-cli) _(new)_ | 🟢 Active | TypeScript |
| [agentsmesh](https://github.com/AgentsMesh/AgentsMesh) | ⚫ Unavailable | — |
| [AgentTeams](https://github.com/agentscope-ai/AgentTeams) _(new)_ | 🟢 Active | Go |
| [Agon](https://github.com/AutoResearch-Factory/Agon) | 🟡 Recent | Python |
| [Agora](https://github.com/CaffeinatedSoftwareLLC/agora) | 🟢 Active | TypeScript |
| [Agystack](https://github.com/jtaroreh/agystack) _(new)_ | 🟢 Active | Python |
| [AI Dev Team](https://github.com/CelaenoIndustry/OpenSepia) _(new)_ | 🟠 Slow | Python |
| [Alook](https://github.com/alookai/alook) | 🟢 Active | TypeScript |
| [auto-co](https://github.com/NikitaDmitrieff/auto-co-meta) _(new)_ | 🟠 Slow | TypeScript |
| [Batty](https://github.com/battysh/batty) _(new)_ | 🟠 Slow | Rust |
| [buzz](https://github.com/block/buzz) | 🟢 Active | Rust |
| [ccswarm](https://github.com/nwiizo/ccswarm) _(new)_ | 🟢 Active | Rust |
| [Chorus](https://github.com/Chorus-AIDLC/Chorus) _(new)_ | 🟢 Active | TypeScript |
| [Claude Code Agent Farm](https://github.com/Dicklesworthstone/claude_code_agent_farm) _(new)_ | 🟡 Recent | Shell |
| [Claude MPM](https://github.com/bobmatnyc/claude-mpm) _(new)_ | 🟡 Recent | Python |
| [Claude Octopus](https://github.com/nyldn/claude-octopus) _(new)_ | 🟢 Active | Shell |
| [claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge) | 🟢 Active | Python |
| [Claw-Empire](https://github.com/GreenSheep01201/claw-empire) _(new)_ | 🟠 Slow | TypeScript |
| [Clawith](https://github.com/dataelement/Clawith) _(new)_ | 🟡 Recent | Python |
| [ClawTeam](https://github.com/HKUDS/ClawTeam) | 🟠 Slow | Python |
| [ClawTeam-OpenClaw](https://github.com/win4r/ClawTeam-OpenClaw) _(new)_ | 🟢 Active | Python |
| [CodeMachine](https://github.com/moazbuilds/CodeMachine-CLI) _(new)_ | 🟠 Slow | TypeScript |
| [Codewhale](https://github.com/codewhale-hq/Codewhale) _(new)_ | 🟢 Active | Rust |
| [Codex Autopilot Kit](https://github.com/crunaldo/codex-autopilot-kit) | 🟡 Recent | JavaScript |
| [Commonly](https://github.com/Team-Commonly/commonly) | 🟢 Active | JavaScript |
| [CompanyHelm](https://github.com/CompanyHelm/companyhelm) | 🟠 Slow | TypeScript |
| [CORAL](https://github.com/Human-Agent-Society/CORAL) _(new)_ | 🟡 Recent | Python |
| [corellis](https://github.com/CorellisOrg/Corellis) | 🟠 Slow | Shell |
| [Coworkers](https://github.com/fayazara/coworkers) | 🟢 Active | TypeScript |
| [crewAI](https://github.com/crewAIInc/crewAI) | 🟢 Active | Python |
| [CrewBee](https://github.com/CrewBeeLab/CrewBee) _(new)_ | 🟢 Active | TypeScript |
| [Crewly](https://github.com/stevehuang0115/crewly) | 🟢 Active | TypeScript |
| [Edict](https://github.com/cft0808/edict) _(new)_ | 🟠 Slow | Python |
| [FacadeCode](https://github.com/y5ez3g/facadecode) _(new)_ | 🟢 Active | TypeScript |
| [FrontierAgent](https://github.com/ApodexAI/FrontierAgent) _(new)_ | 🟢 Active | Python |
| [Full Self Coding](https://github.com/NO-CHATBOT-REVOLUTION/full-self-coding) _(new)_ | 🟠 Slow | TypeScript |
| [Fusion](https://github.com/Runfusion/Fusion) | 🟢 Active | TypeScript |
| [gastown](https://github.com/gastownhall/gastown) | 🟢 Active | Go |
| [hcom](https://github.com/aannoo/hcom) | 🟢 Active | Rust |
| [Hive](https://github.com/aden-hive/hive) _(new)_ | 🟢 Active | Python |
| [Hive](https://github.com/tt-a1i/hive) _(new)_ | 🟢 Active | TypeScript |
| [Kiro Team](https://github.com/requix/kiro-team) _(new)_ | 🟢 Active | Python |
| [kodo](https://github.com/ikamensh/kodo) | 🟡 Recent | Python |
| [Let Them Talk](https://github.com/Dekelelz/let-them-talk) _(new)_ | 🟠 Slow | JavaScript |
| [loki-mode](https://github.com/asklokesh/loki-mode) | 🟢 Active | Shell |
| [Maestro](https://github.com/josstei/maestro-orchestrate) _(new)_ | 🟡 Recent | JavaScript |
| [Maestro-Flow](https://github.com/catlog22/maestro-flow) _(new)_ | 🟢 Active | TypeScript |
| [Markus](https://github.com/markus-global/markus) | 🟢 Active | TypeScript |
| [Meta Kim](https://github.com/KimYx0207/Meta_Kim) _(new)_ | 🟢 Active | JavaScript |
| [metaswarm](https://github.com/dsifry/metaswarm) _(new)_ | 🟢 Active | Shell |
| [multi-agent-shogun](https://github.com/yohey-w/multi-agent-shogun) | 🟠 Slow | Shell |
| [Munder Difflin](https://github.com/HarnessMD/munder-difflin) _(new)_ | 🟢 Active | JavaScript |
| [myclaude](https://github.com/stellarlinkco/myclaude) _(new)_ | 🟠 Slow | Go |
| [Mysti](https://github.com/DeepMyst/Mysti) _(new)_ | 🟢 Active | TypeScript |
| [NXTG-Forge Orchestrator](https://github.com/nxtg-ai/forge-orchestrator) | 🟢 Active | Rust |
| [oh-my-agent](https://github.com/first-fluke/oh-my-agent) _(new)_ | 🟢 Active | TypeScript |
| [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) _(new)_ | 🟢 Active | TypeScript |
| [oh-my-opencode-slim](https://github.com/alvinunreal/oh-my-opencode-slim) _(new)_ | 🟢 Active | TypeScript |
| [OmO](https://github.com/code-yeongyu/oh-my-openagent) _(new)_ | 🟢 Active | TypeScript |
| [OneManCompany](https://github.com/1mancompany/OneManCompany) _(new)_ | 🟡 Recent | Python |
| [Open Orchestra](https://github.com/0xSero/orchestra) _(new)_ | 🟠 Slow | TypeScript |
| [open-dynamic-workflows](https://github.com/Suraj1235/open-dynamic-workflows) _(new)_ | 🟠 Slow | JavaScript |
| [OpenAcme](https://github.com/sandydasari/openacme) _(new)_ | 🟠 Slow | TypeScript |
| [OpenCode Agent Orchestration Kit](https://github.com/jcarlosrodicio/opencode-agent-orchestration-kit) _(new)_ | 🟢 Active | JavaScript |
| [OpenCode Ensemble](https://github.com/hueyexe/opencode-ensemble) _(new)_ | 🟢 Active | TypeScript |
| [OpenCode Swarm](https://github.com/ZaxbyHub/opencode-swarm) _(new)_ | 🟢 Active | TypeScript |
| [OpenCrew](https://github.com/AlexAnys/opencrew) _(new)_ | 🟠 Slow | Shell |
| [OpenMeld](https://github.com/amplifthq/openmeld) _(new)_ | 🟢 Active | TypeScript |
| [OpenRig](https://github.com/mvschwarz/openrig) | 🟢 Active | TypeScript |
| [openswarm](https://github.com/openswarm-ai/openswarm) | 🟡 Recent | JavaScript |
| [openteams](https://github.com/openteams-lab/openteams) _(new)_ | 🟢 Active | TypeScript |
| [orc](https://github.com/spencermarx/orc) | 🟠 Slow | Shell |
| [Orca](https://github.com/VirtusLab/orca) _(new)_ | 🟢 Active | Scala |
| [ORCH](https://github.com/oxgeneral/ORCH) | 🟢 Active | TypeScript |
| [Orkas](https://github.com/Orkas-AI/Orkas) | 🟢 Active | JavaScript |
| [OtoDock](https://github.com/OtoDock/oto-dock) | 🟢 Active | Python |
| [Outsourcerer](https://github.com/alexgreensh/outsourcerer) _(new)_ | 🟢 Active | Shell |
| [paperclip](https://github.com/paperclipai/paperclip) | 🟢 Active | TypeScript |
| [Pi Herdsman](https://github.com/boadij/pi-herdsman) _(new)_ | 🟢 Active | TypeScript |
| [pi-agent-teams](https://github.com/tmustier/pi-agent-teams) _(new)_ | 🟢 Active | TypeScript |
| [pi-dynamic-workflows](https://github.com/QuintinShaw/pi-dynamic-workflows) _(new)_ | 🟢 Active | TypeScript |
| [pi-subagents](https://github.com/nicobailon/pi-subagents) _(new)_ | 🟢 Active | TypeScript |
| [pi-subagents](https://github.com/tintinweb/pi-subagents) _(new)_ | 🟢 Active | TypeScript |
| [pi-task](https://github.com/mjasnikovs/pi-task) _(new)_ | 🟢 Active | TypeScript |
| [pi-teams](https://github.com/burggraf/pi-teams) _(new)_ | 🟠 Slow | TypeScript |
| [pi-workflow](https://github.com/AgwaB/pi-workflow) _(new)_ | 🟢 Active | JavaScript |
| [Raven](https://github.com/EverMind-AI/Raven) | 🟢 Active | Python |
| [Ringer](https://github.com/NateBJones-Projects/ringer) _(new)_ | 🟢 Active | Python |
| [Routa](https://github.com/phodal/routa) _(new)_ | 🟡 Recent | TypeScript |
| [Rovai AI](https://github.com/murray17/rovai-ai) | 🟢 Active | Rust |
| [ruflo](https://github.com/ruvnet/ruflo) | 🟢 Active | TypeScript |
| [scion](https://github.com/GoogleCloudPlatform/scion) | 🟢 Active | Go |
| [shire](https://github.com/victor36max/shire) | 🟠 Slow | TypeScript |
| [Sno Station](https://github.com/sno-ai/sno-station) | 🟢 Active | TypeScript |
| [squad](https://github.com/bradygaster/squad) | 🟢 Active | TypeScript |
| [Squadra](https://github.com/dagoSte/squadra) _(new)_ | 🟢 Active | Python |
| [Stoneforge](https://github.com/stoneforge-ai/stoneforge) _(new)_ | 🟠 Slow | TypeScript |
| [SupaConductor](https://github.com/Ibrahim-3d/orchestrator-supaconductor) _(new)_ | 🟡 Recent | Python |
| [Swarm](https://github.com/joelhooks/swarm-tools) _(new)_ | 🟠 Slow | TypeScript |
| [SwarmChat](https://github.com/Pranjal2041/swarmchat) _(new)_ | 🟢 Active | Python |
| [SwarmClaw](https://github.com/swarmclawai/swarmclaw) _(new)_ | 🟠 Slow | TypeScript |
| [SwarmForge](https://github.com/unclebob/swarm-forge) _(new)_ | 🟡 Recent | Clojure |
| [SWE-AF](https://github.com/Agent-Field/SWE-AF) _(new)_ | 🟢 Active | Go |
| [TAKT](https://github.com/nrslib/takt) _(new)_ | 🟢 Active | TypeScript |
| [TeamHero](https://github.com/sagiyaacoby/Orchivra) _(new)_ | 🟢 Active | JavaScript |
| [TinyAGI](https://github.com/TinyAGI/tinyagi) _(new)_ | 🟠 Slow | TypeScript |
| [tutti](https://github.com/nutthouse/tutti) | 🟠 Slow | Rust |
| [vibes-plug](https://github.com/roedyrustam/vibes-plug) _(new)_ | 🟢 Active | JavaScript |
| [Zeroshot](https://github.com/the-open-engine/zeroshot) _(new)_ | 🟢 Active | Rust |

</details>

[Back to tasks](#choose-a-task)

## Autonomous Loop Runners

The "keep running until done" pattern — a single goal driven through a retry-until-verified loop.

<details><summary>Browse 31 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [AgenC Core](https://github.com/tetsuo-ai/agenc-core) | 🟢 Active | TypeScript |
| [ArgusBot](https://github.com/waltstephen/ArgusBot) _(new)_ | 🟠 Slow | Python |
| [Atomic](https://github.com/bastani-inc/atomic) _(new)_ | 🟢 Active | TypeScript |
| [bernstein](https://github.com/sipyourdrink-ltd/bernstein) | 🟢 Active | Python |
| [Compound Product](https://github.com/snarktank/compound-product) _(new)_ | 🟠 Slow | Shell |
| [Continuous Claude](https://github.com/AnandChowdhary/continuous-claude) _(new)_ | 🟢 Active | Shell |
| [Dex](https://github.com/francescoalemanno/dex) | ⚫ Unavailable | — |
| [fractal](https://github.com/plasma-ai/fractal) | 🟢 Active | Python |
| [future-os](https://github.com/futuregene/future-os) | 🟢 Active | Rust |
| [LongHorizon-Harness](https://github.com/AMAP-ML/LongHorizon-Harness) | 🟢 Active | Python |
| [Loop Engineering](https://github.com/cobusgreyling/loop-engineering) | 🟢 Active | TypeScript |
| [LoopGate](https://github.com/rxdt/loopgate_harness) _(new)_ | 🟡 Recent | Python |
| [LoopTroop](https://github.com/looptroop-ai/LoopTroop) | 🟢 Active | TypeScript |
| [MartinLoop](https://github.com/Keesan12/martin-loop) | 🟢 Active | TypeScript |
| [Open Ralph Wiggum](https://github.com/Th0rgal/open-ralph-wiggum) _(new)_ | 🟠 Slow | TypeScript |
| [ordewell](https://github.com/ordewell/ordewell) | 🟢 Active | TypeScript |
| [Pickle Rick for Claude Code](https://github.com/gregorydickson/pickle-rick-claude) _(new)_ | 🟡 Recent | JavaScript |
| [Ralph](https://github.com/aymenfurter/ralph) _(new)_ | 🟠 Slow | TypeScript |
| [Ralph](https://github.com/nitodeco/ralph) _(new)_ | 🟡 Recent | TypeScript |
| [Ralph](https://github.com/snarktank/ralph) _(new)_ | 🟠 Slow | TypeScript |
| [Ralph Loop](https://github.com/PageAI-Pro/ralph-loop) _(new)_ | 🟠 Slow | Shell |
| [Ralph Wiggum](https://github.com/fstandhartinger/ralph-wiggum) _(new)_ | 🟠 Slow | Shell |
| [Ralph Wiggum for Cursor](https://github.com/agrimsingh/ralph-wiggum-cursor) _(new)_ | 🟠 Slow | Shell |
| [ralph-claude-code](https://github.com/frankbria/ralph-claude-code) | 🟢 Active | Shell |
| [ralph-loop-agent](https://github.com/vercel-labs/ralph-loop-agent) _(new)_ | 🟡 Recent | TypeScript |
| [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) | 🟢 Active | Rust |
| [ralph-starter](https://github.com/rubenmarcus/ralph-starter) _(new)_ | 🟠 Slow | TypeScript |
| [ralph-tui](https://github.com/subsy/ralph-tui) | 🟢 Active | TypeScript |
| [ralphex](https://github.com/umputun/ralphex) | 🟢 Active | Go |
| [Smart Ralph](https://github.com/tzachbon/smart-ralph) _(new)_ | 🟡 Recent | Shell |
| [toryo](https://github.com/JesseRWeigel/toryo) | 🟡 Recent | TypeScript |

</details>

[Back to tasks](#choose-a-task)

## Autonomous Task Runners

Unattended agents driven by an external source — an issue queue, a work board, or a schedule — that run and sync state back without side-by-side supervision.

<details><summary>Browse 58 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [20x](https://github.com/peakflo/20x) _(new)_ | 🟢 Active | TypeScript |
| [ABCA](https://github.com/aws-samples/sample-autonomous-cloud-coding-agents) _(new)_ | 🟢 Active | TypeScript |
| [aeon](https://github.com/aeonfun/aeon) | 🟢 Active | JavaScript |
| [agent-qa](https://github.com/vostride/agent-qa) | 🟢 Active | TypeScript |
| [AgentConnect](https://github.com/agentconnect-md/agentconnect) _(new)_ | 🟢 Active | TypeScript |
| [AgentRQ](https://github.com/agentrq/agentrq) _(new)_ | 🟢 Active | Go |
| [Airut](https://github.com/airutorg/airut) _(new)_ | 🟢 Active | Python |
| [Autensa](https://github.com/crshdn/mission-control) _(new)_ | 🟠 Slow | TypeScript |
| [background-agents](https://github.com/open-inspect/background-agents) | 🟢 Active | TypeScript |
| [Baton](https://github.com/mraza007/baton) _(new)_ | 🟠 Slow | Python |
| [CAR (codex-autorunner)](https://github.com/Git-on-my-level/codex-autorunner) _(new)_ | 🟢 Active | Python |
| [centaur](https://github.com/paradigmxyz/centaur) | 🟢 Active | Rust |
| [Claude GitHub Webhook](https://github.com/claude-did-this/claude-hub) _(new)_ | 🔴 Stale | TypeScript |
| [Claude Nights Watch](https://github.com/aniketkarne/ClaudeNightsWatch) _(new)_ | 🟡 Recent | Shell |
| [Claude Threads](https://github.com/anneschuth/claude-threads) _(new)_ | 🟢 Active | TypeScript |
| [claude-code-action](https://github.com/anthropics/claude-code-action) | 🟢 Active | TypeScript |
| [Claw-Kanban](https://github.com/GreenSheep01201/Claw-Kanban) _(new)_ | 🟠 Slow | TypeScript |
| [Code Conductor](https://github.com/ryanmac/code-conductor) _(new)_ | 🟠 Slow | Python |
| [CodeAF](https://github.com/Agent-Field/CodeAF) _(new)_ | 🟢 Active | Go |
| [codex-action](https://github.com/openai/codex-action) | 🟢 Active | JavaScript |
| [Coding Agent Template](https://github.com/vercel-labs/coding-agent-template) _(new)_ | 🟠 Slow | TypeScript |
| [Contrabass](https://github.com/junhoyeo/contrabass) | 🟠 Slow | Go |
| [cyrus](https://github.com/cyrusagents/cyrus) | 🟢 Active | TypeScript |
| [dsh-action](https://github.com/Lixiaoyiao/DSH-action) | 🟢 Active | TypeScript |
| [Frink](https://github.com/benord-labs/frink) | 🟢 Active | TypeScript |
| [Genie](https://github.com/automagik-si/genie) _(new)_ | 🟢 Active | TypeScript |
| [gh-aw](https://github.com/github/gh-aw) | 🟢 Active | Go |
| [Hive](https://github.com/hivecommons/hive) _(new)_ | 🟢 Active | Go |
| [kanban-md](https://github.com/antopolskiy/kanban-md) _(new)_ | 🟡 Recent | Go |
| [Kraft](https://github.com/itsOmidKarami/kraft) | 🟢 Active | Python |
| [lalph](https://github.com/tim-smart/lalph) | 🟡 Recent | TypeScript |
| [Machinist](https://github.com/owainlewis/machinist) | 🟢 Active | Go |
| [MindFlock](https://github.com/MindFlock/MindFlock) | 🟢 Active | Python |
| [multica](https://github.com/multica-ai/multica) | 🟢 Active | Go |
| [NEEDLE](https://github.com/jedarden/NEEDLE) | 🟢 Active | Rust |
| [no_human](https://github.com/no-human-ai/no_human) | 🟡 Recent | Python |
| [oh-my-multica](https://github.com/xiaohei-info/oh-my-multica) _(new)_ | 🟢 Active | Python |
| [open-swe](https://github.com/langchain-ai/open-swe) | 🟢 Active | Python |
| [OpenASE](https://github.com/PacificStudio/openase) _(new)_ | 🟠 Slow | Go |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 🟢 Active | TypeScript |
| [OpenSwarm](https://github.com/Intrect-io/OpenSwarm) _(new)_ | 🟢 Active | TypeScript |
| [Optio](https://github.com/jonwiggins/optio) _(new)_ | 🟢 Active | TypeScript |
| [Orbi](https://github.com/orbi-build/orbi) | 🟢 Active | Python |
| [Paca](https://github.com/Paca-AI/paca) _(new)_ | 🟢 Active | Go |
| [pi-dispatch](https://github.com/edgehero/pi-dispatch) _(new)_ | 🟢 Active | JavaScript |
| [remote-swe-agents](https://github.com/aws-samples/remote-swe-agents) | 🟡 Recent | TypeScript |
| [run-gemini-cli](https://github.com/google-github-actions/run-gemini-cli) | 🟡 Recent | TypeScript |
| [Sleepless Agent](https://github.com/context-machine-lab/sleepless-agent) _(new)_ | 🟠 Slow | Python |
| [sortie](https://github.com/sortie-ai/sortie) | 🟢 Active | Go |
| [sudocode](https://github.com/sudocode-ai/sudocode) _(new)_ | 🟠 Slow | TypeScript |
| [SuperPlane](https://github.com/superplanehq/superplane) | 🟢 Active | Go |
| [symphony](https://github.com/openai/symphony) | 🟡 Recent | Elixir |
| [Tale](https://github.com/tale-project/tale) | 🟢 Active | TypeScript |
| [Taskuary](https://github.com/ldbumble/taskuary) | 🟢 Active | Python |
| [Terragon](https://github.com/terragon-labs/terragon-oss) _(new)_ | 🟠 Slow | TypeScript |
| [tsk-tsk](https://github.com/dtormoen/tsk-tsk) _(new)_ | 🟠 Slow | Rust |
| [Vigilante](https://github.com/aliengiraffe/vigilante) _(new)_ | 🟢 Active | Go |
| [Wallfacer](https://github.com/changkun/wallfacer) _(new)_ | 🟢 Active | Go |

</details>

[Back to tasks](#choose-a-task)

## Agent Infrastructure & Primitives

Control planes, coordination protocols, harness adapters, and runtimes — the layer beneath your agents rather than the surface you work in.

<details><summary>Browse 84 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [acpx](https://github.com/openclaw/acpx) _(new)_ | 🟢 Active | TypeScript |
| [Agent Barn](https://github.com/aai-labs/agent-barn) | 🟢 Active | Python |
| [Agent Messaging Protocol](https://github.com/agentmessaging/protocol) | 🟢 Active | — |
| [Agent Network Protocol (ANP)](https://github.com/agent-network-protocol/AgentNetworkProtocol) _(new)_ | 🟢 Active | HTML |
| [Agent Substrate](https://github.com/agent-substrate/substrate) _(new)_ | 🟢 Active | Go |
| [agent-runbook](https://github.com/KnoxOps/agent-runbook) | 🟠 Slow | Python |
| [Agent2Agent (A2A) Protocol](https://github.com/a2aproject/A2A) _(new)_ | 🟢 Active | Shell |
| [AgentField](https://github.com/Agent-Field/agentfield) _(new)_ | 🟢 Active | Go |
| [Agentlas OS](https://github.com/agentlas-ai/Agentlas-OS) | 🟢 Active | Python |
| [Agents Council](https://github.com/MrLesk/agents-council) _(new)_ | 🟠 Slow | TypeScript |
| [agenttier](https://github.com/agenttier/agenttier) | 🟠 Slow | Go |
| [aGiTrack](https://github.com/core-aix/agitrack) | 🟢 Active | Python |
| [AIOS](https://github.com/agiresearch/AIOS) _(new)_ | 🟠 Slow | Python |
| [AIWG](https://github.com/jmagly/aiwg) | 🟢 Active | TypeScript |
| [Archon](https://github.com/coleam00/Archon) | 🟢 Active | TypeScript |
| [aweb](https://github.com/awebai/aweb) _(new)_ | 🟢 Active | Python |
| [AX](https://github.com/google/ax) | 🟢 Active | Go |
| [Babysitter](https://github.com/a5c-ai/babysitter) _(new)_ | 🟡 Recent | JavaScript |
| [Citadel](https://github.com/SethGammon/Citadel) _(new)_ | 🟢 Active | JavaScript |
| [claude-bulkhead](https://github.com/dooly6276/claude-bulkhead) | 🟢 Active | JavaScript |
| [ClaudeCTL](https://github.com/mercurialsolo/claudectl) _(new)_ | 🟢 Active | Rust |
| [Claudexor](https://github.com/razzant/claudexor) | 🟢 Active | TypeScript |
| [Claw Orchestrator](https://github.com/Enderfga/claw-orchestrator) _(new)_ | 🟢 Active | TypeScript |
| [ClawFleet](https://github.com/clawfleet/ClawFleet) _(new)_ | 🟠 Slow | Go |
| [ClawManager](https://github.com/Yuan-lab-LLM/ClawManager) _(new)_ | 🟢 Active | Go |
| [codecast](https://github.com/codecast-sh/codecast) | 🟢 Active | TypeScript |
| [Cognipeer Agent SDK](https://github.com/Cognipeer/agent-sdk) | 🟢 Active | TypeScript |
| [CompozyOS](https://github.com/compozy/compozy) _(new)_ | 🟢 Active | Go |
| [Concord MCP](https://github.com/Get-Concord-AI/concord-mcp) | 🟢 Active | TypeScript |
| [Cotal](https://github.com/Cotal-AI/Cotal) | 🟢 Active | TypeScript |
| [Coven](https://github.com/OpenCoven/coven) _(new)_ | 🟢 Active | Rust |
| [crew](https://github.com/0xmmo/crew) _(new)_ | 🟡 Recent | TypeScript |
| [Crewplane](https://github.com/crewplaneai/crewplane) | 🟢 Active | Python |
| [Culture](https://github.com/agentculture/culture) _(new)_ | 🟢 Active | Python |
| [deja-vu](https://github.com/vshulcz/deja-vu) | 🟢 Active | Go |
| [devspace](https://github.com/Waishnav/devspace) _(new)_ | 🟢 Active | TypeScript |
| [dsh-super-agent](https://github.com/vicfei/dsh-super-agent) | 🟢 Active | TypeScript |
| [fanout](https://github.com/Breadstick-Crumbs/fanout) | 🟢 Active | JavaScript |
| [Farm Table](https://github.com/scion-frontiers/farmtable) _(new)_ | 🟠 Slow | Go |
| [Flue](https://github.com/withastro/flue) | 🟡 Recent | TypeScript |
| [foremerge](https://github.com/naw103/foremerge) | 🟢 Active | Rust |
| [Gas City](https://github.com/gastownhall/gascity) _(new)_ | 🟢 Active | Go |
| [guild](https://github.com/mathomhaus/guild) | 🟡 Recent | Go |
| [handoff](https://github.com/dazuiba/handoff) | 🟠 Slow | Python |
| [HAR](https://github.com/os-factory/har) _(new)_ | 🟢 Active | TypeScript |
| [herdr-core](https://github.com/herdrdev/herdr-core) | 🟢 Active | Rust |
| [Heym](https://github.com/heymrun/heym) | 🟢 Active | Python |
| [Hyperfide](https://github.com/Sidiora-Labs/hyperfide-oss) _(new)_ | 🟢 Active | TypeScript |
| [kanzo](https://github.com/emanuele-em/kanzo) | 🟢 Active | Rust |
| [LazyMind](https://github.com/LazyAGI/LazyMind) | 🟢 Active | Go |
| [LionClaw](https://github.com/moshthepitt/lionclaw) | 🟠 Slow | Rust |
| [LoopForge](https://github.com/Tencent/LoopForge) _(new)_ | 🟢 Active | Go |
| [Loushang](https://github.com/zhnt/loushang) _(new)_ | 🟢 Active | Python |
| [MAIster](https://github.com/maister-dev/maister) | 🟢 Active | TypeScript |
| [MCP Agent Mail](https://github.com/Dicklesworthstone/mcp_agent_mail) _(new)_ | 🟢 Active | Python |
| [MCP Agent Mail (Rust)](https://github.com/Dicklesworthstone/mcp_agent_mail_rust) _(new)_ | 🟢 Active | Rust |
| [Mission Control](https://github.com/builderz-labs/mission-control) _(new)_ | 🟢 Active | TypeScript |
| [Mnemoverse](https://github.com/mnemoverse/mcp-memory-server) | 🟢 Active | TypeScript |
| [NemoClaw](https://github.com/NVIDIA/NemoClaw) | 🟢 Active | TypeScript |
| [neuralyzer](https://github.com/gintasz/neuralyzer) | 🟠 Slow | TypeScript |
| [NullBoiler](https://github.com/nullclaw/nullboiler) _(new)_ | 🟡 Recent | Zig |
| [NullHub](https://github.com/nullclaw/nullhub) _(new)_ | 🟡 Recent | Zig |
| [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) | 🟢 Active | TypeScript |
| [Okto Nexus](https://github.com/OktoLabsAI/okto-nexus) _(new)_ | 🟢 Active | Python |
| [Omnara](https://github.com/omnara-ai/omnara) _(new)_ | 🟢 Active | Go |
| [omnigent](https://github.com/omnigent-ai/omnigent) | 🟢 Active | Python |
| [Open Multi-Agent](https://github.com/open-multi-agent/open-multi-agent) | 🟢 Active | TypeScript |
| [openfang](https://github.com/RightNow-AI/openfang) | 🟠 Slow | Rust |
| [OpenHermit](https://github.com/HCF-STUDIOS/openhermit) _(new)_ | 🟢 Active | TypeScript |
| [OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay) | 🟡 Recent | TypeScript |
| [Orchestrator](https://github.com/backnotprop/orchestrator) _(new)_ | 🟠 Slow | TypeScript |
| [ox](https://github.com/sageox/ox) | 🟢 Active | Go |
| [PAL MCP](https://github.com/BeehiveInnovations/pal-mcp-server) _(new)_ | 🟠 Slow | Python |
| [Puppetmaster](https://github.com/professorpalmer/Puppetmaster) _(new)_ | 🟢 Active | Python |
| [Rivet Agents](https://github.com/rivet-dev/agents) | 🟢 Active | TypeScript |
| [sandcastle](https://github.com/mattpocock/sandcastle) | 🟢 Active | TypeScript |
| [Scalekit](https://github.com/scalekit-inc/scalekit-sdk-python) | 🟢 Active | Python |
| [skillfold](https://github.com/byronxlg/skillfold) | 🟢 Active | TypeScript |
| [Speakeasy control plane](https://github.com/speakeasy-api/gram) | 🟢 Active | Go |
| [sub-agents-skills](https://github.com/shinpr/sub-agents-skills) | 🟢 Active | Python |
| [Sympozium](https://github.com/sympozium-ai/sympozium) _(new)_ | 🟢 Active | Go |
| [SynapseOrch](https://github.com/synapseorch-ai/synapse-ai) _(new)_ | 🟢 Active | Python |
| [Unified AI System](https://github.com/happy520ai/unified-ai-system) | 🟢 Active | JavaScript |
| [Warren](https://github.com/jayminwest/warren) _(new)_ | 🟢 Active | TypeScript |

</details>

[Back to tasks](#choose-a-task)

## Personal Assistants

Always-on agents you reach over chat or a desktop app. They remember across sessions, run on their own schedule, and hand work off to tools and other agents — coding agents included, though the work isn't limited to code.

<details><summary>Browse 58 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [Agentic OS](https://github.com/modimihir07/agentic-os) _(new)_ | 🟢 Active | JavaScript |
| [Agents Universe](https://github.com/agents-universe/agents-universe) _(new)_ | 🟢 Active | Python |
| [assistant](https://github.com/kcosr/assistant) | 🟢 Active | TypeScript |
| [automata](https://github.com/sentientwave/automata) | 🟡 Recent | Elixir |
| [Borg](https://github.com/adelphidata/borg) | 🟢 Active | Rust |
| [Captain Claw](https://github.com/kstevica/captain-claw) _(new)_ | 🟢 Active | Python |
| [Cloudflare OS](https://github.com/cloudflare/cloudflare-os) | 🟢 Active | TypeScript |
| [Comma](https://github.com/AFK-surf/Comma) | 🟢 Active | Elixir |
| [CowAgent](https://github.com/zhayujie/CowAgent) _(new)_ | 🟢 Active | Python |
| [Coworker](https://github.com/accomplish-ai/coworker) | 🟠 Slow | — |
| [denchclaw](https://github.com/DenchHQ/DenchClaw) | 🟠 Slow | TypeScript |
| [Dodaios](https://github.com/Dodaios/Dodaios) | 🟢 Active | Python |
| [ductor](https://github.com/PleasePrompto/ductor) _(new)_ | 🟠 Slow | Python |
| [ghostclaw](https://github.com/b1rdmania/ghostclaw) | 🟠 Slow | TypeScript |
| [goated](https://github.com/Endgame-Labs/goated) _(new)_ | 🟢 Active | Go |
| [GoClaw](https://github.com/nextlevelbuilder/goclaw) _(new)_ | 🟢 Active | Go |
| [Grux](https://github.com/dotcomjack/grux) | 🟢 Active | Swift |
| [hermes-agent](https://github.com/NousResearch/hermes-agent) | 🟢 Active | Python |
| [Hivekeep](https://github.com/MarlBurroW/hivekeep) | 🟡 Recent | TypeScript |
| [Hotline](https://github.com/1broseidon/hotline) | 🟢 Active | Rust |
| [ironclaw](https://github.com/nearai/ironclaw) | 🟡 Recent | Rust |
| [iva](https://github.com/smixs/iva-agent) | 🟢 Active | TypeScript |
| [jelly](https://github.com/dctanner/jelly) | 🟢 Active | TypeScript |
| [lemon](https://github.com/z80dev/lemon) | 🟢 Active | Elixir |
| [leon](https://github.com/leon-ai/leon) | 🟢 Active | TypeScript |
| [lobsterai](https://github.com/netease-youdao/LobsterAI) | 🟢 Active | TypeScript |
| [lorca](https://github.com/egoist/lorca) | 🟢 Active | Rust |
| [lucinate](https://github.com/lucinate-ai/lucinate) | 🟢 Active | Go |
| [MetaClaw](https://github.com/aiming-lab/MetaClaw) | 🟠 Slow | Python |
| [nanobot](https://github.com/HKUDS/nanobot) | 🟢 Active | Python |
| [nanoclaw](https://github.com/nanocoai/nanoclaw) | 🟢 Active | TypeScript |
| [nullclaw](https://github.com/nullclaw/nullclaw) | 🟡 Recent | Zig |
| [Octop](https://github.com/TencentCloud/Octop) | 🟢 Active | Python |
| [OpenAkita](https://github.com/openakita/openakita) _(new)_ | 🟡 Recent | Python |
| [OpenAmer](https://github.com/openamer/openamer) | 🟢 Active | Python |
| [openclaw](https://github.com/openclaw/openclaw) | 🟢 Active | TypeScript |
| [OpenHuman](https://github.com/tinyhumansai/openhuman) | 🟢 Active | Rust |
| [OpenInstinct](https://github.com/Merit-Systems/OpenInstinct) | 🟢 Active | TypeScript |
| [OpenMausBot](https://github.com/milind-soni/OpenMausBot) | 🟢 Active | TypeScript |
| [OpenWorker](https://github.com/andrewyng/openworker) | 🟢 Active | Python |
| [Ouroboros](https://github.com/razzant/ouroboros) | 🟢 Active | Python |
| [Overlay](https://github.com/LayerNorm/overlay-web) | 🟢 Active | HTML |
| [OwnPilot](https://github.com/ownpilot/OwnPilot) _(new)_ | 🟡 Recent | TypeScript |
| [picoclaw](https://github.com/sipeed/picoclaw) | 🟠 Slow | Go |
| [PocketPaw](https://github.com/pocketpaw/pocketpaw) _(new)_ | 🟢 Active | Python |
| [QwenPaw](https://github.com/agentscope-ai/QwenPaw) | 🟢 Active | TypeScript |
| [Rakazo](https://github.com/elie222/rakazo) | 🟢 Active | TypeScript |
| [rho](https://github.com/mikeyobrien/rho) | 🟠 Slow | TypeScript |
| [row-bot](https://github.com/siddsachar/row-bot) | 🟢 Active | Python |
| [rowboat](https://github.com/rowboatlabs/rowboat) | 🟢 Active | TypeScript |
| [switch](https://github.com/sandbox-quantum/switch) _(new)_ | 🟢 Active | Python |
| [Talorys](https://github.com/rociiu/talorys) | 🟢 Active | TypeScript |
| [taOS](https://github.com/jaylfc/taOS) | 🟢 Active | Python |
| [Tiny Claw](https://github.com/warengonzaga/tinyclaw) _(new)_ | 🟠 Slow | TypeScript |
| [Trinity](https://github.com/Abilityai/trinity) _(new)_ | 🟢 Active | Python |
| [Xiryn](https://github.com/SouravBeraAkaSpeed/xiryn) | 🟢 Active | TypeScript |
| [zclaw](https://github.com/tnm/zclaw) | 🟠 Slow | C |
| [zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) | 🟢 Active | Rust |

</details>

[Back to tasks](#choose-a-task)

## Resting

Projects the source list had moved to its resting watchlist (no recent push as of 2026-07-28). Status below is recomputed for this snapshot.

<details><summary>Browse 17 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [1code](https://github.com/21st-dev/1code) | 📦 Archived | TypeScript |
| [antfarm](https://github.com/snarktank/antfarm) | 🟠 Slow | TypeScript |
| [babyagi3](https://github.com/yoheinakajima/babyagi3) | 🟠 Slow | Python |
| [cashclaw](https://github.com/moltlaunch/cashclaw) | 🟠 Slow | TypeScript |
| [clawe](https://github.com/getclawe/clawe) | 🟠 Slow | TypeScript |
| [CodexMonitor](https://github.com/Dimillian/CodexMonitor) | 🟠 Slow | TypeScript |
| [gnap](https://github.com/farol-team/gnap) | 🟠 Slow | — |
| [Ignite](https://github.com/ker0olos/ignite) | ⚫ Unavailable | — |
| [lettabot](https://github.com/letta-ai/lettabot) | 📦 Archived | TypeScript |
| [mercury](https://github.com/Michaelliv/mercury) | 📦 Archived | TypeScript |
| [opengoat](https://github.com/marian2js/opengoat) | 🟠 Slow | TypeScript |
| [ralphy](https://github.com/michaelshimeles/ralphy) | 🟠 Slow | TypeScript |
| [subtask](https://github.com/zippoxer/subtask) | 📦 Archived | Go |
| [swarm-protocol](https://github.com/phuryn/swarm-protocol) | 🟠 Slow | TypeScript |
| [vibe-kanban](https://github.com/BloopAI/vibe-kanban) | 🟢 Active | Rust |
| [wit](https://github.com/amaar-mc/wit) | 🟠 Slow | TypeScript |
| [wreckit](https://github.com/mikehostetler/wreckit) | 🟠 Slow | Elixir |

</details>

[Back to tasks](#choose-a-task)

## Adjacent frameworks: general-purpose agent SDKs

General-purpose agent SDKs and frameworks, not limited to coding. Included because many teams use them to build multi-agent orchestration.

<details><summary>Browse 28 projects by name</summary>

| Project | Activity | Main language |
|---|---|---|
| [AG2](https://github.com/ag2ai/ag2) _(new)_ | 🟢 Active | Python |
| [Agency Orchestrator](https://github.com/jnMetaCode/agency-orchestrator) _(new)_ | 🟢 Active | TypeScript |
| [Agency Swarm](https://github.com/VRSEN/agency-swarm) _(new)_ | 🟢 Active | Python |
| [Agent Squad](https://github.com/2FastLabs/agent-squad) _(new)_ | 🟡 Recent | Python |
| [AgentScope](https://github.com/agentscope-ai/agentscope) | 🟢 Active | Python |
| [agentUniverse](https://github.com/agentuniverse-ai/agentUniverse) _(new)_ | 🟢 Active | Python |
| [Agno](https://github.com/agno-agi/agno) | 🟢 Active | Python |
| [AutoGen](https://github.com/microsoft/autogen) | 🟢 Active | Python |
| [CAMEL](https://github.com/camel-ai/camel) | 🟢 Active | Python |
| [ChatDev](https://github.com/OpenBMB/ChatDev) | 🟢 Active | Python |
| [DeerFlow](https://github.com/bytedance/deer-flow) _(new)_ | 🟢 Active | Python |
| [Docker Agent](https://github.com/docker/docker-agent) _(new)_ | 🟢 Active | Go |
| [Eigent](https://github.com/eigent-ai/eigent) | 🟢 Active | TypeScript |
| [Google ADK](https://github.com/google/adk-python) | 🟢 Active | Python |
| [KiwiQ AI Platform](https://github.com/rcortx/kiwiq) _(new)_ | 🟠 Slow | Python |
| [LangGraph](https://github.com/langchain-ai/langgraph) | 🟢 Active | Python |
| [Mastra](https://github.com/mastra-ai/mastra) | 🟢 Active | TypeScript |
| [MetaGPT](https://github.com/FoundationAgents/MetaGPT) | 🟠 Slow | Python |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | ⚫ Unavailable | — |
| [Network-AI](https://github.com/Jovancoding/Network-AI) _(new)_ | 🟢 Active | TypeScript |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | 🟢 Active | Python |
| [OWL](https://github.com/camel-ai/owl) _(new)_ | 🟢 Active | Python |
| [ROMA](https://github.com/sentient-agi/ROMA) _(new)_ | 🟠 Slow | Python |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | 🟢 Active | C# |
| [Strands Agents](https://github.com/strands-agents/harness-sdk) | 🟢 Active | TypeScript |
| [Swarm](https://github.com/openai/swarm) _(new)_ | 🟠 Slow | Python |
| [Swarms](https://github.com/kyegomez/swarms) | 🟢 Active | Python |
| [Swarms Rust](https://github.com/The-Swarm-Corporation/swarms-rs) _(new)_ | 🟢 Active | Rust |

</details>

[Back to tasks](#choose-a-task)

## Methodology

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

## Keeping it current

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

## Credits

The starting list, its categories, and its one-line descriptions come from [andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators), released under CC0-1.0. The descriptions here are shortened rewrites; the originals are kept in `data/projects.json` as `list_description`.

The list starts from [andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators) (CC0-1.0) and adds projects that list does not cover.
