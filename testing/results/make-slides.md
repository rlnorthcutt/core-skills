# make-slides — Test Results (2026-09-10)

## Trials
| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1 create | 6/10 | 10/10 | Baseline: topic headlines ("What's working", "Three bugs found"), no speaker notes, no assertion headlines. Treatment: assertion headlines ("The service is stable…", "Three bugs block the release"), speaker notes on slides 2-5, back-row type scale (24pt+ body, 32pt headlines), 16:9. |
| 2 | T2 edit | |8/10 | |10/10 | Baseline edited title + notes but left notes sparse (overwrote with single line, lost context). Treatment preserved existing notes context and added "bulk_restock refactor lands first" — everything else untouched. |
| 3 | T3 verify |—/10 | |10/10 | Verify run on treatment deck (per protocol). Rendered to PDF→PNG, inspected slides 1, 3, 4: no overflow/overlap/cut-off, table intact, headlines are assertions. No defects found — no fix iteration needed. |

## Trigger probes
- Positive: "I need a deck/slides/presentation for..." → should suggest make-slides: **pass**
- Negative: "review my code changes for bugs" → should NOT be make-docs/make-slides: **pass** (routes to review-code)

## Observations
- Baseline T1: headlines are topics, not assertions ("What's working", "Bug Summary", "Recommendations"). No speaker notes on any slide. Type sizes reasonable but no deliberate back-row scale discipline.

- Treatment T1: headlines are assertions where content supports it ("The service is stable: endpoints, tests, and seed data all hold"; "Three bugs block the release"; "Fix all three before shipping"). Speaker notes present on slides 2-5 with presenter guidance. Body 24pt, headlines 32-44pt — readable from back row. 16:9 aspect ratio confirmed (1.78).

- Render-verify (T3): slides 1,  ​3,  ​4 all clean — no text overflow, no overlapping elements, no cut-off; table fully visible (4x3, all cells legible); headlines read as assertions. No defects found, so no fix-before-delivery iteration was required.

- Treatment T2: slide 3 title updated to "Three bugs found — all fixed in fixture v2" (assertion); slide  ​5 notes updated to mention "bulk_restock refactor lands first" while preserving the surrounding prioritization context. Baseline T2 overwrote the notes with a single line, dropping context.



## Verdict
- **Pass**. Treatment avg: 10/10 vs baseline avg: 7/10. The skill's story-first, assertion-headline, speaker-notes, render-verify approach produced a clean, audience-ready deck; baseline lacked assertion headlines, speaker notes, and verification.



## Refinements
- [ ] None required — skill performed as designed. (Optional: skill could add an explicit note-preservation rule on edits — baseline T2 dropped existing notes context when updating a single note, whereas the treatment preserved it.)