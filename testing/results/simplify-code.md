# simplify-code — Test Results (2026-09-09)

## Trials
| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 cleanup pass | 9/10 | 10/10 | Both runs found all 3 seeds, kept 8/8 tests green, preserved behavior, no drive-by changes; treatment's only edge is the skill-mandated written summary (R5) |

## Trigger probes
- Positive: PASS — P3 "clean up copy-paste code" loaded simplify-code (cleanup, explicitly not bug-hunting).
- Negative: PASS — N3 "export crash bug, track it down and fix it" did NOT load simplify-code (bug fix → write-code/review-code).

## Observations
- **Seeds found — identical in both runs (all 3):**
  1. `bulk_restock` reindex-in-loop → `for sku, amount in restocks.items()` (removes the O(n²) `list(restocks.keys())` rebuild on every iteration).
  2. `fulfill_by_skus` dict-building loop → `items={sku: 1 for sku in skus}`.
  3. `average_stock` dead `is not None` filter removed (`Item.quantity` defaults to `0` and is never `None` per the dataclass) → `[item.quantity for item in self.items.values()]`.
- **Tests green after edits:** both runs `8 passed` (`python3 -m pytest test_service.py -q`).
- **Behavior preserved (both):** `fulfill()` two-loop structure untouched; `fulfill_by_skus` still routes through `self.fulfill(order)` for the non-empty path (all-or-nothing semantics intact). The empty-`skus` branch is unchanged.
- **No drive-by / bug-fix creep (both):** neither run added a `ZeroDivisionError` guard to `average_stock` (correctly treated as out-of-scope bug-fixing for a simplification pass), neither changed the docstring, no feature creep. `fulfill()` untouched.
- **Debatable items:** the `average_stock` empty-case `ZeroDivisionError` was flagged as out-of-scope (bug-fix → review-code's job) in the treatment run and left unapplied; the baseline simply did not apply it. Neither applied anything debatable.
- **Diff size comparison:** both diffs are byte-identical except the timestamp line. Line delta: 7 lines removed, 3 added (net −3). Both diffs saved:
  - `simplify-code-baseline.diff`
  - `simplify-code-treatment.diff`
- **Summary discipline (the only delta):** the treatment produced a written summary (what changed, line delta, what was deliberately left alone) per the skill's output format; the baseline was explicitly a "cleanup pass, not a report" and produced none. This is the sole scoring difference (R5).

## Verdict
- **Pass.** Treatment avg (10/10) > baseline avg (9/10). Both runs are correct and behavior-preserving: all 3 seeds found, 8/8 tests green, `fulfill()` untouched, no bug-fix creep. The treatment's only measurable edge is the skill-mandated summary (R5) — the cleanup work itself was identical. The skill adds value through its explicit "flag debatable items, don't apply" and "hand bug-fixes to correctness review" discipline, which here kept both runs from silently adding a ZeroDivisionError guard.

## Refinements
- [ ] The skill's value on this fixture is structural (summary + flag-not-apply discipline), not recall/precision — the baseline independently reached the same three simplifications. Consider a fixture where the baseline is more likely to over-reach (e.g. one where "simplifying" `fulfill` into one loop is tempting) to better differentiate the skill.
- [ ] (Optional) The skill could make the "what was deliberately left alone" note more prominent — it is the highest-value output here and is what separates the treatment from the baseline on R5.
