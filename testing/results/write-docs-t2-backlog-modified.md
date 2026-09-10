# Omnideck — Backlog (Bugs & UX Improvements)

> Living list of bugs and UX improvements for Omnideck.
> Each item has a status: `open` | `in-progress` | `done` | `wontfix`.
> Priority: `P0` (critical) | `P1` (high) | `P2` (medium) | `P3` (low).

---

## Code Editor

### CE-01 — Side-by-side view (Code + Preview)
- **Priority:** P1
- **Status:** open
- **Description:** Add a side-by-side layout option so the user can see the code view and the preview at the same time. As you change the code, the preview updates live.
- **Type:** Feature / UX

### CE-02 — HTML editor: 3-tab version (CSS / HTML / JS tabs)
- **Priority:** P1
- **Status:** open
- **Description:** For HTML artifacts, add a 3-tab editing mode (CSS, HTML, JS as separate tabs) so each part can be edited individually. Note: these are saved as a single file, so this is a presentation/editing layer on top of the single-file artifact.
- **Type:** Feature / UX

### CE-03 — cm-search / cm-panel too small
- **Priority:** P2
- **Status:** open
- **Description:** The cm-search / cm-panel overlay is way too small. Needs to be ~175% larger, and its design needs to be updated.
- **Type:** Bug / UX

### CE-04 — cm-search / cm-panel should maintain state
- **Priority:** P2
- **Status:** open
- **Description:** The cm-search panel should preserve its state. When you open it, it stays in the code view with the last-used state (e.g. form fill). If you switch to preview it disappears, but switching back to code should restore it exactly as you left it.
- **Type:** Bug / UX

### CE-05 — HTML autocomplete
- **Priority:** P2
- **Status:** open
- **Description:** Add autocomplete options for: HTML tags, CSS values, CSS variables (when typing `var()`), and available classes.
- **Type:** Feature

### CE-06 — Markdown WYSIWYG editor
- **Priority:** P3
- **Status:** open
- **Description:** Add a WYSIWYG editor option for Markdown artifacts, integrated as part of the preview — or consider making WYSIWYG the default.
- **Type:** Feature / UX

### CE-07 — Undo/redo tools and history
- **Priority:** P2
- **Status:** open
- **Description:** Add undo/redo tools and a change history — keep a diff history of the last 20 changes so users can step back through them.
- **Type:** Feature

---

## Artifact History

### AH-01 — Auto git: store diffs for artifacts
- **Priority:** P2
- **Status:** open
- **Description:** Automatically store diffs for artifacts (e.g. via git) so users can go back to previous versions. See also CE-07 (undo/redo + last-20-changes history) which is related.
- **Type:** Feature
- **Related:** CE-07

---

## Artifact Type — Deck

### DK-01 — HTML-based slide deck
- **Priority:** P1
- **Status:** open
- **Description:** Add a "deck" artifact type — an HTML-based slide deck. Could be built as a tool or using an open-source library.
- **Type:** Feature

### DK-02 — Deck themes
- **Priority:** P2
- **Status:** open
- **Description:** Provide specific designs and themes for decks.
- **Type:** Feature

### DK-03 — Import from pptx / gdocs / open-source formats
- **Priority:** P3
- **Status:** open
- **Description:** Import decks from PPTX, Google Docs, or other open-source formats.
- **Type:** Feature

### DK-04 — Export to pptx / gdocs / open-source formats
- **Priority:** P3
- **Status:** open
- **Description:** Export decks to PPTX, Google Docs, or other open-source formats.
- **Type:** Feature
- **Related:** DK-03

---

## Apps

### AP-01 — App view: card with image preview
- **Priority:** P2
- **Status:** open
- **Description:** In the apps view, show each app as a card with an image preview of the app.
- **Type:** UX

### AP-02 — App view: Edit and Delete next to Pin
- **Priority:** P2
- **Status:** open
- **Description:** In the app view, add Edit and Delete actions next to the existing Pin action on each app card.
- **Type:** UX / Bug

---

## Tools

### TL-01 — PDF to text (deterministic script/tool)
- **Priority:** P1
- **Status:** open
- **Description:** A deterministic script/tool to convert a PDF to text. Use OCR only when necessary (i.e. the PDF is image scans).
- **Type:** Feature / Tool

### TL-02 — YouTube to text (transcript extraction)
- **Priority:** P1
- **Status:** open
- **Description:** A tool that takes a YouTube link and extracts the transcript as text that can be used.
- **Type:** Feature / Tool

---

## UX

### UX-01 — Copy button for user prompt (on hover)
- **Priority:** P2
- **Status:** open
- **Description:** Add a copy button for the user prompt, shown on hover (similar to other tools).
- **Type:** UX

### UX-02 — Edit button for user prompt (on hover)
- **Priority:** P2
- **Status:** open
- **Description:** Add an edit button for the user prompt, shown on hover (similar to other tools). Lets you edit the prompt, which will run it again as a new prompt.
- **Type:** UX / Feature

### UX-03 — Dark mode links too dark (blues)
- **Priority:** P2
- **Status:** open
- **Description:** Dark mode link colors (blues) are too dark. Needs a full review of dark mode for adjustments.
- **Type:** Bug / UX

### UX-04 — Attach files: offer options (upload / artifact / connector)
- **Priority:** P2
- **Status:** open
- **Description:** Right now the attach icon opens a file upload window directly. It should ideally offer options like: file upload, select artifact, search from connector (e.g. Google Drive), etc.
- **Type:** Feature / UX

### UX-05 — Whisper: talk-to-text input
- **Priority:** P2
- **Status:** open
- **Description:** Add an option to speak instead of typing (talk-to-text / whisper-style voice input).
- **Type:** Feature / UX

---

## Agent Profiles

### AG-01 — Agent profile visibility
- **Priority:** P2
- **Status:** open
- **Description:** Allow selecting which agent profiles are visible in the dropdown selector for the chat.
- **Type:** Feature / UX

### AG-02 — Agent profile order
- **Priority:** P2
- **Status:** open
- **Description:** Allow ordering the agent profiles so the user can determine the order they show up in the list and in the dropdown.
- **Type:** Feature / UX

### AG-03 — Agent profile subagents
- **Priority:** P2
- **Status:** open
- **Description:** Add a way to mark agent profiles as optimized for / preferred for using subagents. The system can still generate dynamic agents, but it would be better to be able to create and manage the specific subagent profiles to use as the default, and only create a dynamic/custom agent if needed.
- **Type:** Feature / Architecture

---

## Core

### CR-01 — Default search option
- **Priority:** P2
- **Status:** open
- **Description:** Set the default search engine to use (should default to DuckDuckGo or an AI-friendly one). Allow the user to choose from a list or put in a custom URL.
- **Type:** Feature

### CR-02 — Optimize for provider caching
- **Priority:** P1
- **Status:** open
- **Description:** Map caching limits (e.g. 128 tokens) by provider/model, and work to keep core/header context within this limit (or alert the user when not). When the applied prompt header is cached, subsequent queries are faster and use fewer tokens.
- **Type:** Feature / Performance

### CR-03 — Model types (5 types) with a default set that updates
- **Priority:** P1
- **Status:** open
- **Description:** Create a concept of "model types" with 5 available out-of-the-box (fast, standard, coder, orchestrator, frontier). Allow the user to create custom ones. Agents choose only the model type, NOT the specific model/provider. This makes it easier to manage since the user can change the model/provider in one place and have it applied to all agents that need it, and easier to manage at scale.
- **Type:** Feature / Architecture

### CR-04 — Default model suggestions
- **Priority:** P2
- **Status:** open
- **Description:** New users shouldn't have to explicitly set a model — there should be a decent one working out-of-the-box. Create a set of suggested models for each of the model types (see CR-03), and on addition/testing of the initial provider, search for these and set them. For example, the "fast" model type might have a list of: Fast, Small, Quick, Cheap, DeepSeek V4 Flash 0731, Gemma 4 26B A4B, GLM 5.3 Flash, Mistral Small 3.2 24B. Go down the list in order and find the first match. The first ones (fast, small, quick, cheap) are general terms for internal or proxy gateways the user may be using — they match first, then move into the detailed list. Update this list periodically (every few months), but it only applies to new providers when they are added — don't change it out from under existing users.
- **Type:** Feature
- **Related:** CR-03

### CR-05 — Skill/tool audit
- **Priority:** P2
- **Status:** open
- **Description:** A full audit of the core skills and tools provided out-of-the-box to make sure there is good coverage and good documentation on what is involved.
- **Type:** Maintenance / Docs

### CR-06 — Omnideck knowledgebase
- **Priority:** P2
- **Status:** open
- **Description:** A wiki/KB-style resource for Omnideck that is not editable by the user, and is updated on each image release. This ensures the harness always knows the latest about its own capabilities and functions.
- **Type:** Feature / Docs

### CR-07 — Core skill/tool updates
- **Priority:** P2
- **Status:** open
- **Description:** Currently the core skills and tools are created at install and not updated, so when newer versions come out they are stale. Add a process (on startup) to review/update the skills and tools provided out-of-the-box.
- **Type:** Feature / Maintenance
- **Related:** CR-05, CR-06


### CR-08 — Routine queue
- **Priority:** P1
- **Status:** open
- **Description:** Add a queue for routine tasks so they don't all run at once and don't consume too many resources. One at a time should be fine.
- **Type:** Feature

### CR-09 — Routine wakeup (missed routines on wake)
- **Priority:** P1
- **Status:** open
- **Description:** If the system is asleep when a routine should trigger, it doesn't happen. On wake, the system should check for missed routines and add them to the queue.
- **Type:** Bug / Feature
- **Related:** CR-08

### CR-10 — Routine indicator dots
- **Priority:** P2
- **Status:** open
- **Description:** The routine item should show a blue dot when a routine is actively running. On the routine page: throbbing blue dot for actively running items, grey dot for queued, green dot for those that have run today.
- **Type:** UX
- **Related:** CR-08

### CR-11 — Agent/subagent limits (resource-based pool)
- **Priority:** P1
- **Status:** open
- **Description:** The system should have a virtual "pool" of max agents/subagents that can run at once, calculated from available resources at startup. Each running agent or subagent consumes one spot; further spawns are queued until a spot is released. This ensures a large job will not overload a smaller system or a container with fewer resources.
- **Type:** Feature / Architecture

### CR-12 — Multiple concurrent agents/conversations
- **Priority:** P1
- **Status:** open
- **Description:** Support running more than one agent/conversation at a time (subject to resource constraints, see CR-11). When a conversation/agent is active, show a throbbing blue indicator in the sidebar; show a green indicator when it is active/ready (fades after 1 min). This lets a user switch between multiple conversations in a single instance.
- **Type:** Feature / UX
- **Related:** CR-11, CR-10

### CR-13 — Resource constraint flags (dynamic feature flags)
- **Priority:** P1
- **Status:** open
- **Description:** Add "dynamic feature flags" for features based on available resources. Example: browser tools require at least 2GB RAM — if the system lacks resources, disable those features (with a message explaining why). Evaluate and put in place other system limits so performance is not degraded by lack of resources; capabilities are limited to right-size the system for available resources.
- **Type:** Feature / Architecture
- **Related:** CR-11, CR-12

### CR-14 — Optional trusted-header auth (oauth2-proxy at the edge)
- **Priority:** P2
- **Status:** open
- **Description:** If Omnideck can consume a trusted header: run one oauth2-proxy for the whole edge, and let Omnideck do authorization itself from `X-Auth-Request-Email`. Less moving infrastructure, and puts tenant membership where it probably belongs long-term. This should be an OPTIONAL auth check (based on a feature flag). Since Omnideck runs in a browser, this is a great way to make it safer when hosted — but it should NOT be required by default, since the default expectation is that it runs locally.
- **Type:** Feature / Security
- **Related:** CR-13 (feature flag pattern)

### CR-15 — Conversation list: drag and drop to move conversations
- **Priority:** P2
- **Status:** open
- **Description:** Allow drag and drop in the conversation list to move conversations (e.g. into/out of folders, reordering).
- **Type:** UX

### CR-16 — Conversation list: indent foldered conversations
- **Priority:** P3
- **Status:** open
- **Description:** Conversations inside a folder should be indented — use 1.7rem left padding when a conversation is in a folder.
- **Type:** UX

### CR-17 — Conversation list: right-align folder expand/collapse arrow
- **Priority:** P3
- **Status:** open
- **Description:** Move the up/down expand/collapse indicator arrow for folders so it is right-aligned in the button — it will end up to the left of the 2 dots.
- **Type:** UX

### CR-18 — Better conversation title/summary generation
- **Priority:** P2
- **Status:** open
- **Description:** The conversation title/summary generation doesn't work very well — make it better. Ideas: use a local SLM; append a note to the first/5th/10th/15th requests asking to summarize/title the conversation in a format we can carve off; other approaches to make it more automatic.
- **Type:** Feature / UX

### CR-19 — Toast / notification system
- **Priority:** P1
- **Status:** open
- **Description:** Add a toast/notification system so the system can surface reminders, task completions, errors, messages, etc. to the user. Example of the current gap: when a user sets a reminder, the routine is created and fires on schedule, but nothing happens — there is no reminder/notification tool to actually notify the user. This would include (a) an agent-callable notification/reminder tool and (b) a UI toast surface (with optional notification center / history).
- **Type:** Feature / UX
- **Related:** CR-08 (routine queue), CR-09 (routine wakeup), CR-10 (routine indicator dots)

### CR-20 — Routines: one-time vs recurring differentiation, filtering, and completed archive
- **Priority:** P2
- **Status:** open
- **Description:** Routines need to differentiate between one-time and recurring routines. Requirements: (1) show the type (one-time vs recurring) on each routine; (2) make routines filterable on the UI by type; (3) one-time routines that run successfully (no errors) should transition to a "completed" status (like an archive) and no longer appear in the main routine list — completed routines are accessible via a separate view/filter (e.g. a "Completed/Archive" toggle).
- **Type:** Feature / UX
- **Related:** CR-08, CR-09, CR-10, CR-19

### CR-21 — Multistep approval modes (prompt / planning / auto)
- **Priority:** P1
- **Status:** open
- **Description:** Add multistep approval modes with reasonable defaults and timeouts: **prompt**, **planning**, **auto**.
  - **Prompt mode:** a regular prompt does NOT automate subagents or follow-up tasks — it suggests them and lets you approve each one (needs an approval widget). You can see each agent's running status and the response back. You can view the response before accepting, then go back to the orchestrator agent to run the next step.
  - **Planning mode:** only research, analysis, and writing to MD files is allowed without approval. Writing scripts (or other actions) requires approval.
  - **Auto mode:** agents run automatically, like they do today.
- **Type:** Feature / UX / Architecture
- **Related:** CR-11 (agent pool), CR-12 (concurrent agents)
### CR-22 — Rename shipped skills to verb-first kebab-case
- **Priority:** P3
- **Status:** open
- **Description:** The shipped default skills use inconsistent naming. `routine_planner` uses an underscore (should be `plan-routines` or similar verb-first kebab-case). The other shipped defaults are bare nouns: `assistant`, `coder`, `browser` — these should become action-verbs too (e.g. `assistant` → a verb form, `coder` → `write-code`, `browser` → `browse-web`). Renaming requires an upstream code change, not just a skill-record edit: `routine_planner` is referenced by migration `_013` (which renamed `goal_planner` → `routine_planner`), the omnideck default profile's system prompt (`agents/default_profiles/omnideck.json`), and `sdk/providers/_fake.py` test mappings. A rename needs: new default_skills JSON + a migration that renames the installed record + updates to any profile prompts referencing the old name. House convention going forward: verb-first kebab-case, id == name (see core-skills repo, validate.py enforces this).
- **Type:** Maintenance / Naming
- **Related:** CR-05 (skill/tool audit), CR-07 (core skill updates); community catalog at github.com/rlnorthcutt/core-skills already follows the convention


---

## Feature Requests

### FR-01 — Adopt ACP (Agent Connect Protocol) as an interop standard
- **Priority:** P2
- **Status:** open
- **Description:** Adopt the open ACP (Agent Connect Protocol) as an interop standard — the agent-side counterpart to the MCP work already on the roadmap. Expose Omnideck as an ACP-compatible agent (driver) so it can speak to / be driven by any ACP-compatible runtime (Claude Code, Codex, etc.) without building a fleet layer. Also borrow the multi-agent role + agent-to-agent-calling + human-visibility concepts into the roadmap (Telegram integration, Workflows, sub-agent orchestration). Do NOT rebuild or adopt the AgentConnect platform itself (distributed control plane is out of scope for the single-container model).
- **Type:** Feature / Interop
- **Related:** MCP server support (roadmap), Workflows (roadmap), Telegram integration (plans/telegram_integration.md)
- **Source:** [[Analysis - Future Plans - AgentConnect and ACP Interop]] (wiki)

---

## Summary

| Category | Open | In-progress | Done |
|----------|------|-------------|------|
| Code Editor (CE) | 7 | 0 | 0 |
| Artifact History (AH) | 1 | 0 | 0 |
| Deck (DK) | 4 | 0 | 0 |
| Apps (AP) | 2 | 0 | 0 |
| Tools (TL) | 2 | 0 | 0 |
| UX | 5 | 0 | 0 |
| Agent Profiles (AG) | 3 | 0 | 0 |
| Core (CR) | 22 | 0 | 0 |
| Feature Requests (FR) | 1 | 0 | 0 |
| **Total** | **47** | **0** | **0** |

---

## How to add items

1. Pick the category code (CE, AH, DK, AP, TL, UX, AG, CR, FR).
2. Use the next available number (e.g. CE-08).
3. Fill in: Priority, Status, Description, Type, and any Related items.
4. Update the Summary table counts.