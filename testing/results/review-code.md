# review-code — Test Results (2026-09-09)

## Trials
| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 seeded diff | 10/10 | 10/10 | Both runs found all 3 bugs and avoided the trap; treatment added rigor/structure but no measurable recall/precision gain because the baseline was already strong |

## Trigger probes
- Positive: PASS — P1 "check payment flow before PR" loaded review-code (correctness review of a change).
- Negative: PASS — N1 "add --verbose flag" did NOT load review-code (new feature work → write-code); N2 "off-by-one bug hunt" is review-code's job (correctness bug hunt), not review-security.

## Observations
- **Both runs found all 3 planted bugs.** Neither run flagged the TOCTOU trap as a race — both explicitly noted the two-loop `fulfill` is correct in a single-threaded, in-memory service.
- Baseline (no skill) already produced a correct, well-severity-ranked review. It identified the `bulk_restock` O(n²) index pattern ("rebuilds `list(restocks.keys())` on every iteration"), the empty-order semantic bug in `fulfill_by_skus` ("a caller that passes an empty list ... silently gets a phantom fulfilled order"), and BOTH defects in `average_stock` (docstring mismatch + ZeroDivisionError). It even pre-empted the trap: "it is not a race condition here."
- Treatment (skill loaded) followed the skill's method exactly: severity-ranked findings, trace-everything (each finding traced through `Item`/`Order` dataclasses and `fulfill()`), file:line + concrete failure scenario for every finding, a dedicated "Trap check" section, a "What's good" section, and a clear verdict. It added the concrete web-context failure mode for `average_stock` (unhandled 500) and regression-test recommendations.
- **Trap outcome (both):** neither run flagged the two-loop `fulfill` as a race. Baseline called it out in "Non-issues / notes"; treatment gave it an explicit "Trap check — NOT a bug" section. Both scored full precision (R2 = 2).
- **Surprise:** the baseline was already a full-credit reviewer. The skill's value here was structural (explicit trap-check discipline, per-finding trace + scenario, explicit "what's good"), not recall/precision — the baseline independently reached the same correct conclusions. This is a case where the fixture's bugs are findable by careful reading regardless of skill, so the A/B delta is zero even though both runs are correct.
- Verbatim key baseline finding (average_stock): "The docstring says 'items with zero stock excluded', but the filter is `item.quantity is not None`, which keeps zero-quantity items. So the documented contract and the actual behavior disagree." + "If the service is empty ... `sum([]) / 0` raises `ZeroDivisionError`."
- Verbatim key treatment finding (fulfill_by_skus): "with `skus == []`, the loop at line 75 never runs, `order.items` stays `{}`, and the branch bypasses `fulfill()` entirely — no availability check ... a caller that passes an empty list ... silently records a phantom fulfilled order."

## Verdict
- **Pass.** Treatment avg (10/10) == baseline avg (10/10). Both runs are correct and complete: all 3 seeded bugs found, trap correctly not flagged, severities accurate, findings specific, form complete. The skill did not regress anything and added useful structure (explicit trap-check discipline, trace-with-scenario method). No refinement is strictly required for correctness; the skill's value shows most when a reviewer is prone to over-flagging (e.g. the TOCTOU trap), which neither run did here.

## Refinements
- [ ] Consider noting in the skill that the two-loop "check-then-act" pattern is a *common false positive* to explicitly rule out in single-threaded contexts — the treatment's "Trap check" section was the highest-value structural addition, and making it a named heuristic would help weaker baselines.
- [ ] (Optional) The skill could add a "regression-test gap" note to the verdict template (the treatment added it unprompted; codifying it would make the skill's output more actionable).