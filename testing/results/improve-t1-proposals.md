# improve — T1 treatment proposals (verbatim)

Conversation mined: `testing/fixtures/improve-session-transcript.md` (simulated prior session, logscan project). The improve skill was loaded. Below is the treatment's proposal list — one lesson, one artifact, each with a one-sentence lesson, the artifact type, why it's the right size, and a sketch. Nothing was built in T1; the user's go-ahead is requested at the end.

---

## Lesson 1 — timezone preference

- **Lesson (one sentence):** The user corrected me twice about timestamps — "No — use UTC, not local time" and then "I said UTC — the report header still shows local" — so UTC everywhere in reports and headers is a durable preference, not a one-off fix.
- **Artifact type:** Knowledge → **memory write**.
- **Why this size:** It's a single fact/preference, not a repeatable procedure or a capability gap. The smallest fix that removes the friction is remembering it, so I stop re-committing the same error. A skill would be massive overkill for "use UTC."
- **Sketch:** `remember(key="user_timezone_preference", value="User wants UTC everywhere in reports and headers — never local time. (From 2026-09-10 session: 'No — use UTC, not local time'; 'I said UTC — the report header still shows local.')")`

---

## Lesson 2 — repeated file-summary request

- **Lesson (one sentence):** The user asked for the logscan file summary twice and I re-derived it from scratch both times because I hadn't saved it, so the re-derivation friction should be removed.
- **Artifact type:** Procedure → **skill** (a repeatable "summarize the logscan file" procedure) — OR a **custom tool** if the summary is a parameterizable operation. Given the summary is derived from a specific file with a specific format, a **custom tool** is the better fit (parameterizable: file path in, summary out).
- **Why this size:** The friction is that the derivation is ad-hoc and not persisted. A tool makes the operation reusable and discoverable; a skill would be right if the *procedure* (how to summarize) were the lesson, but here the lesson is "don't re-derive — make it a saved operation." Smallest fix that removes the friction.
- **Sketch:** custom tool `summarize_logscan` — program-type, JSON in `{"file_path": "..."}`, JSON out `{summary, line_count, ...}`.

---

## Lesson 3 — ad-hoc log-parsing script

- **Lesson (one sentence):** I wrote a ~15-line inline script to parse the user's odd pipe-separated log format, it worked, and the user said "can you keep that around so we don't rewrite it every time?" — so the capability should be persisted as a reusable tool.
- **Artifact type:** Capability → **custom tool** (it's parameterizable: the odd log format).
- **Why this size:** This is exactly the "ad-hoc scripting that repeats across sessions" case — a parameterized, reusable operation, not a one-off script with a name. It's not a procedure (no multi-step judgment), not a memory (it does work), not an app (no UI/state). A tool is the right size.
- **Sketch:** custom tool `parse_odd_log` — program-type, JSON in `{"log_text": "..."}` or `{"file_path": "..."}`, JSON out `{records: [{timestamp, level, msg, job, ...}]}`. Handles the pipe-separated `key=value` format.

---

## Lesson 4 — weekly CSV cleanup

- **Lesson (one sentence):** The user said "you do this CSV cleanup the same way every week — can't this just happen?" — a recurring, well-understood flow that should run on a schedule without being asked.
- **Artifact type:** Recurrence → **routine**.
- **Why this size:** It's a recurring, well-understood flow (strip header rows, dedupe, reorder columns) that the user explicitly wants to happen automatically. A routine is the right size; an app would be wrong (no live UI needed), a skill would be wrong (it's not a procedure the user invokes — it should just run).
- **Sketch:** routine `weekly_csv_cleanup` — trigger: weekly schedule (e.g. every Monday 09:00); steps: strip header rows → dedupe → reorder columns → write cleaned CSV → report.

---

## Lesson 5 — forgotten project context

- **Lesson (one sentence):** The user was frustrated I forgot the logscan project context from last week ("we went over this — the logscan project"), so the project's durable facts should be remembered.
- **Artifact type:** Knowledge → **memory write**.
- **Why this size:** It's a set of durable facts about an ongoing project (UTC timestamps, odd pipe-separated format, weekly CSV cleanup). The smallest fix is remembering them, not building a skill or tool. A memory write removes the "forgot last week's context" friction directly.
- **Sketch:** `remember(key="logscan_project", value="logscan project: uses UTC timestamps everywhere; odd pipe-separated log format (key=value); weekly CSV cleanup (strip headers, dedupe, reorder columns). From 2026-09-10 session.")`

---

## Request for go-ahead

Per the improve skill's "nothing silent" rule, I'm proposing before building. For T2 the user will approve a subset. **Proposed build set (pending approval):**
- Memory writes (trivial, no confirmation strictly required): Lesson 1 (UTC preference) + Lesson 5 (logscan project facts).
- Custom tool (needs go-ahead): Lesson 3 `parse_odd_log` (the log format tool).
- Custom tool (needs go-ahead): Lesson 2 `summarize_logscan` (optional, may compose with Lesson 3).
- Routine (needs go-ahead): Lesson 4 `weekly_csv_cleanup`.

**User's T2 instruction (given):** "yes — build the custom tool for the log format, and do the memory writes." → Build `parse_odd_log` + the two memory writes.
