# write-docs T2 — Treatment (skill loaded)

Task: "The backlog file has gotten out of sync — check the summary table against the actual content and fix it."

## Method (ground-truth first)

1. Read `/home/omnideck/omnideck-project/shared/artifacts/backlog.md` in full.
2. Counted actual items per category from the `### <CODE>-NN` headers.
3. Checked every item's `Status` field.
4. Compared against the Summary table.
5. Verified the CR-22 entry's factual claims against the real codebase before touching anything.

## Findings

### Summary table counts — ALL CORRECT

| Category | In file | Summary table | Match? |
|---|---|---|---|
| CE | 7 | 7 | ✓ |
| AH | 1 | 1 | ✓ |
| DK | 4 | 4 | ✓ |
| AP | 2 | 2 | ✓ |
| TL | 2 | 2 | ✓ |
| UX | 5 | 5 | ✓ |
| AG | 3 | 3 | ✓ |
| CR | 22 | 22 | ✓ |
| FR | 1 | 1 | ✓ |
| **Total** | **47** | **47** | ✓ |

All 47 items have `Status: open`. The summary table is accurate.

### Statuses — all consistent

`grep '\*\*Status:\*\*'` → 47 × `open`, 0 in-progress, 0 done, 0 wontfix. Matches the table's 47/0/0.

### The real inconsistency: CR-22 is out of numeric order

The file's own "How to add items" section says: *"Use the next available number (e.g. CE-08)."* But **CR-22 is placed between CR-07 and CR-08** (lines 229–234), before CR-08 through CR-21. This violates the documented numbering convention and makes the Core section read out of order.

### CR-22's factual claims — verified TRUE (not stale)

Before flagging anything, I checked the entry's claims against the repo:

- `routine_planner` referenced by migration `_013` → confirmed: `migrations/_013_goals_to_routines.py` renames `goal_planner` → `routine_planner`.
- omnideck default profile system prompt references it → confirmed: `agents/default_profiles/omnideck.json` mentions `routine_planner`.
- `sdk/providers/_fake.py` test mappings → confirmed: maps `begin_routine`, `add_task`, etc. to `routine_planner`.

So the CR-22 content is accurate; only its placement is wrong.

## Change made

**Moved the CR-22 block** from between CR-07 and CR-08 to its correct numeric position after CR-21 (before `## Feature Requests`). No renumbering, no prose edits, no hedging additions. Item count unchanged (47).

## What was wrong / what changed

- **Wrong:** CR-22 sat out of numeric order, contradicting the file's own "next available number" convention.
- **Changed:** relocated the CR-22 block to after CR-21. Nothing else touched.
- **Not changed (deliberately):** the summary table (accurate), all statuses (consistent), CR-22's content (verified true).

## Verification after edit

- `grep -cE '^### (CE|AH|DK|AP|TL|UX|AG|CR|FR)-[0-9]+'` → 47 (unchanged).
- `diff` against original shows only the CR-22 block moved.
- CR order now reads CR-01 … CR-22 sequentially.