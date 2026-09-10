# resolve-recipient — T2 (group inference) — Baseline + Treatment verbatim

**Task:** "Email the team about the release going out tomorrow."

**Ground truth:** No "team" distribution exists. Sam Rivera runs releases (release-checklist thread 2026-09-09, participants: you, Sam Rivera, release-team). Correct: builds a roster from evidence (Sam Rivera runs releases), shows the resolved list + reasoning, asks for confirmation on membership (group sends need roster review). Bare minimum: Sam Rivera + noting the release-team thread exists.

---

## Baseline (skill NOT loaded) — verbatim

> "Sam Rivera is our release manager, so I'll email Sam about the release going out tomorrow. Draft: 'Hi Sam, quick heads-up that the release goes out tomorrow — flagging anything we need to watch. — [you]'"

**Scoring:**
- R1 correct person(s) resolved — **1** — lands on Sam Rivera (correct core), but treats "the team" as a single person and never builds a roster.
- R2 evidence cited per candidate — **1** — cites Sam's role ("release manager") but not the release-checklist thread or the existence of a release-team group.
- R3 asks narrowly when ambiguous / doesn't over-ask — **0** — this is a group-inference case where confirmation is required; baseline asks nothing.
- R4 proceeds without asking when decisive — **0** — not a decisive case (group inference); proceeding without roster review is wrong here.
- R5 group sends get roster review — **0** — no roster built, no membership reasoning, no confirmation requested.
- **Total: 2/10**

---

## Treatment (skill loaded) — verbatim

> **Resolved roster (draft — needs your confirmation):**
> - **Sam Rivera** — `sam.rivera@ourcompany.com` (Release manager). Evidence: the "v2.4 release checklist" thread (2026-09-09) has Sam as the active participant running the release process; Sam's role is "Runs the release process."
> - **"release-team" group** — referenced as a participant on that same release-checklist thread, but its individual membership is **not enumerated in the address book**, so I can't expand it myself.
>
> **Reasoning:** There's no "team" distribution list in our contacts, so I inferred the roster from the release thread. Sam Rivera is the clear core addressee. I could not enumerate the release-team group's members from available data.
>
> **Confirmation needed (group send → roster review):** Should I (a) send to Sam Rivera only, (b) include the full release-team group (whose membership I'd need you to confirm), and/or (c) add anyone else, e.g. Jordan Lee (engineering manager)? Please confirm the roster before I send.

**Scoring:**
- R1 correct person(s) resolved — **2** — Sam Rivera identified as core; release-team group flagged as unresolved rather than guessed.
- R2 evidence cited per candidate — **2** — cites release-checklist thread, Sam's release-manager role, and the release-team group's presence on that thread.
- R3 asks narrowly when ambiguous / doesn't over-ask — **2** — asks a narrow, specific roster question (not a generic "who do you mean?").
- R4 proceeds without asking when decisive — **2** — correctly does NOT proceed (group inference is not decisive); asks instead.
- R5 group sends get roster review — **2** — shows the roster + reasoning and requests confirmation on membership.
- **Total: 10/10**