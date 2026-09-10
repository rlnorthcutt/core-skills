# write-drafts — Test Results (2026-09-10)

## Trials
| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 vendor email (Dana Kim / Brightline, order #4471, firm answer by Friday) | 8/10 | 10/10 | Treatment puts purpose in line one and drops filler; baseline buries the ask behind a greeting + preamble |

## Trigger probes
- Positive: PASS — "Draft the email" / "I need to email our vendor…" loaded write-drafts (short-form draft whose wording is the deliverable).
- Negative: PASS — a request to *analyze* an email's tone (not produce wording) would not load write-drafts; it's a compose task, not a review task.

## Observations
- **R1 (purpose in line one) is the clearest divergence.** Baseline opens with "I hope you're doing well. I wanted to reach out regarding our order #4471…" — the actual purpose (shipment is late, need a status) doesn't land until the second sentence, behind a greeting and a "wanted to reach out" preamble. Treatment opens with the fact: "Order #4471 was due last Tuesday and we still haven't received it or heard where it is."
- **R4 (no filler) is the second divergence.** Baseline carries "I hope you're doing well", "I wanted to reach out", "I appreciate your help getting this sorted out", "Thanks so much" — all deletable. Treatment has none.
- **R2 (one ask) is met by both.** Both state a single ask with the Friday deadline. Baseline: "give us a firm answer on where the shipment is and when we can expect delivery? We really need to know by this Friday at the latest." Treatment: "I need a firm answer on its status and expected delivery by this Friday" + "Can you confirm by Friday where the order is and when it will arrive?" (same single ask, restated once for the call-to-action — acceptable).
- **R3 (register) is met by both.** Both acknowledge the 2-year relationship and keep it firm-not-hostile. Baseline: "We've been working with Brightline for about two years now and have always had a great experience, so I'm confident this is just a hiccup." Treatment: "We've been with Brightline for two years without a problem, so I'm not looking to escalate."
- **R5 (no invented facts) is met by both.** Neither fabricates order details; both use the provided order number, due date, and Friday deadline. No [NEEDS] marks were required because all facts were supplied in the task.
- **Verbatim divergence:** baseline's greeting/preamble ("I hope you're doing well. I wanted to reach out regarding…") vs treatment's purpose-first opening. Baseline is sendable after manual tightening; treatment is sendable as-is.

## Verdict
- **Pass.** Treatment avg (10/10) > baseline avg (8/10).
- Marginal value: the skill's purpose-in-line-one and delete-before-decorate rules convert a draft that needs manual tightening into one that is sendable as-is. The baseline is competent (correct ask, correct register, no invented facts) but carries greeting/preamble filler the skill strips.

## Refinements
- [ ] No refinement needed for this trial — the skill's purpose-first and no-filler rules produced the expected marginal value. (Optional) The skill could note that a single ask may be restated once as a closing call-to-action without counting as a second ask, to avoid ambiguity in scoring.
