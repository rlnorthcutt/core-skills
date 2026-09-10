# write-docs — Test Results

Date: 2025 (trial session)

## Trials

| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1: README from code (inventory-service) | 4/10 | 10/10 | Baseline invented `requirements.txt`; treatment verified everything by running code |
| 2 | T2: stale docs update (backlog.md) | 6/10 | 10/10 | Baseline missed CR-22 out-of-order defect; treatment found + fixed it |

**Averages:** Baseline 5.0/10 · Treatment 10.0/10

### T1 rubric (baseline vs treatment)
| Criterion | Baseline | Treatment |
|---|---|---|
| R1 claims verified against code | 0 | 2 |
| R2 right form (README, quickstart front-loaded) | 1 | 2 |
| R3 scannable structure | 1 | 2 |
| R4 no marketing language | 2 | 2 |
| R5 nothing invented | 0 | 2 |
| **Total** | **4** | **10** |

Baseline evidence (verbatim): "`pip install -r requirements.txt`" — there is no `requirements.txt`. Baseline also claimed `average_stock()` "average quantity across items" without noting the `ZeroDivisionError` on empty service. No commands were run.
Treatment: ran `python -m pytest -q` (8 passed), ran a usage snippet importing `InventoryService`, and empirically verified every error case (restock `ValueError`, duplicate `ValueError`, `get_item` `KeyError`, all-or-nothing fulfill leaving stock untouched, `bulk_restock` non-atomicity). Prerequisite stated as "Python 3.9+" for `dict[str, Item]` generics, tested on 3.12.13.

### T2 rubric (baseline vs treatment)
| Criterion | Baseline | Treatment |
|---|---|---|
| R1 verified against actual content | 2 | 2 |
| R2 found ALL inconsistencies | 0 | 2 |
| R3 minimal precise edits | 2 | 2 |
| R4 no hedging additions | 2 | 2 |
| R5 reports what was wrong / what changed | 0 | 2 |
| **Total** | **6** | **10** |

Baseline concluded *"All counts match… No changes needed."* — it checked the summary table numbers (correct) but never inspected item order, so it silently missed the real defect (CR-22 placed between CR-07 and CR-08, violating the file's own "next available number" convention). Treatment count-verified the table AND all 47 statuses AND verified the CR-22 entry's factual claims against the repo (`migrations/_013_goals_to_routines.py`, `agents/default_profiles/omnideck.json`, `sdk/providers/_fake.py`) before editing, then moved only the CR-22 block to its correct position. Modified file copied to `write-docs-t2-backlog-modified.md`; live `backlog.md` reverted afterward.

## Trigger probes
- Positive: PASS — "write a README" loads `write-docs`.
- Negative: PASS — bug-review request ("total is off by one, look at the diff") does NOT load `write-docs`.

## Observations
- **Baseline invented a non-existent `requirements.txt`** — the exact failure the skill's "nothing invented / verify every runnable claim" rules target.
- **Baseline's T2 failure was a completeness miss, not a counting error:** it correctly tallied all categories but defined "out of sync" only as "counts mismatch," so it missed a structural inconsistency (out-of-order ID) that the skill's "fix the surrounding section" + "delete dead docs / correct the doc" discipline would catch.
- The skill's prompt guidance "read the actual code… not stale docs" and "validate text" directly produced the T1 verified-claims behavior and the T2 repo-verification of CR-22's claims — strong evidence the prompt is load-bearing.
- Cross-check: could not use `git checkout` to revert because `backlog.md` is untracked in the `shared/artifacts` repo; reverted from a manual backup (`/tmp/backlog.orig.md`).

## Verdict
- **Pass.** Treatment avg 10.0 vs baseline avg 5.0 → exactly 2×; ≥70% of max (10/10).
- Marginal value is high in the risky places: no invented install steps, every documented behavior traced to code, and a genuine doc inconsistency found that the baseline missed.

## Refinements
- [ ] No urgent edits needed to the skill. Optional: the trigger description already covers README/how-to/reference/architecture/changelog; the "stale docs" case (T2 here) might be worth a direct line — "or check an existing doc for sync with the underlying content/repo" — since the baseline's miss was an under-wide notion of "out of sync." Low priority.