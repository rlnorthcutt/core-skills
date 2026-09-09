# Tools Inventory — 2026-09-02

What Claude Code (`claude-code 2.1.236`) can actually call in this session,
split by how it becomes available. Companion to `README.md` /
`builtin-skills/` (skills are packaged *instructions*; tools are the actual
functions a skill or I can invoke).

## Always-loaded tools

Defined in the system prompt from the start of every turn — no discovery
step needed.

| Tool | What it does |
|---|---|
| **Bash** | Run shell commands — scripts, installs, tests, etc. Permission-gated sandbox. |
| **Read** | Read files (text, images, PDFs, Jupyter notebooks) |
| **Write** | Create/overwrite a file |
| **Edit** | Targeted find-and-replace edits to an existing file |
| **Agent** | Spawn a subagent — a "fork" of the current session (shares context, background) or a fresh specialized agent (Explore, Plan, code-reviewer, etc.) |
| **Workflow** | Run a scripted, deterministic multi-agent pipeline (fan-out/fan-in, verification passes) — opt-in, heavier orchestration |
| **ListAgents** | List other agents/sessions reachable via SendMessage |
| **AskUserQuestion** | Present the user a multiple-choice clarifying question |
| **ReportFindings** | Structured output format for code-review-style findings |
| **ScheduleWakeup** | Schedule when to resume (backs `/loop`'s dynamic pacing) |
| **Skill** | Invoke a packaged skill |
| **ToolSearch** | Load the full schema for a deferred tool by name/keyword — the mechanism that makes the tools below callable |
| **Artifact** | Publish an HTML or Markdown page as a shareable, live-rendered page (optionally with runtime capabilities — shared state, live/connected data, file downloads, self-updating) |
| **ShareOnboardingGuide** | Upload an ONBOARDING.md for teammates |

## Deferred tools (loaded on demand via ToolSearch)

Named in a system-reminder but schema-less until searched for — a fresh
`ToolSearch` call resolves the full definition before first use.

- **WebFetch** — fetch a specific URL and read/summarize it
- **WebSearch** — search the web
- **NotebookEdit** — edit Jupyter notebook cells
- **CronCreate / CronList / CronDelete** — manage scheduled cloud agents (recurring routines)
- **RemoteTrigger** — fire a remote/cloud session
- **SendMessage** — message another agent/session
- **TaskOutput / TaskStop** — inspect or kill a background task
- **Monitor** — stream live events from a background process
- **EnterPlanMode / ExitPlanMode** — the planning-mode workflow
- **EnterWorktree / ExitWorktree** — git worktree isolation for background/parallel edits
- **PushNotification** — push a mobile notification
- **DesignSync** — sync with the Claude Design canvas tool
- **EndConversation** — end the session (reserved for abuse cases)
- **ListMcpResourcesTool / ReadMcpResourceTool / ReadMcpResourceDirTool** — generic browsing of MCP-exposed resources

## Connected external services (MCP)

**Already authenticated** — full tool sets visible right now:
- **Slack** — read channels/threads/canvases/users, send/schedule messages, reactions, search
- **Google Calendar** — list/search/create/update/delete events, suggest times
- **Google Drive** — search, read, create, copy, share, trash files

**Installed but not connected** — only an `authenticate`/`complete_authentication`
handshake is visible; would need an OAuth round-trip before real tools appear:
**Ahrefs, ClickUp, G2, HubSpot, Zoom, n8n, Salesforce (read-only)**.

## Mapping common asks to what actually runs

| Ask | What handles it |
|---|---|
| Generate an HTML page / live demo | **Artifact** tool — publishes a hosted, shareable page, not a plain file |
| Generate a PPTX / DOCX / PDF | **No dedicated tool.** Done via **Bash + Write**, shelling out to whatever's installed on this machine (`python-docx`/`python-pptx`/`pypdf`, `pandoc`, LaTeX, etc.). Different from claude.ai's chat UI or the Claude API's Managed Agents sandbox, which ship those libraries pre-installed in a hosted container — Claude Code only has what your actual filesystem has. |
| Web browsing (read a page / search) | **WebFetch** / **WebSearch** — read-only, no clicking or screenshots |
| Interactive browsing (click, type, screenshot a live page) | The **claude-in-chrome** skill + its `mcp__claude-in-chrome__*` tools, driving the user's real Chrome via an extension — **not connected in this session** |
| Run terminal commands | **Bash**, permission-gated |
| One-time scripts | No separate "code execution" tool — **Write** the script, run it with **Bash** |
