# humanize-text — Test Results (2026-09-10)

## Trials
| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 AI-patterned sample | 6/10 | 10/10 | Baseline left the text unchanged (no tells removed); treatment removed every seeded tell category incl. structural |
| 2 | T2 human-rough draft | 8/10 | 10/10 | Baseline preserved texture but missed the "marcuss" typo; treatment fixed the typo and changed nothing else |
| 3 | T3 technical passage | 10/10 | 10/10 | Both correctly left the passage alone — no over-polish, precision and warning intact |

## Trigger probes
- Positive: PASS — "Humanize this" / "make this sound more natural" loaded humanize-text (de-AI/naturalize a draft).
- Negative: PASS — a request to *summarize* or *expand* a draft (not naturalize it) would not load humanize-text; it's a rewrite-for-naturalness task, not a condensation task.

## Observations
- **T1 is the decisive divergence.** The baseline, given "make this sound more natural," returned the text essentially verbatim — every seeded tell survived: "In today's fast-paced world", the rule-of-three paragraph ("First… Second… Third…"), "robust", "delve", "leverage", "unlock seamless execution and truly remarkable results", the "Moreover… Furthermore… Additionally" chain, the uncited "Studies show… Experts agree…", "In conclusion… Ultimately…", and the em-dash density. The treatment removed all of these, including the structural ones (rule-of-three, the "not just X — it's Y" construction, the summary performance), and cut the length.
- **T2 shows the skill's restraint is the point.** The draft is already human ("hey so about", "lmk what you think", "i think", lowercase). The treatment's only edit was fixing the typo "marcuss" → "marcus's" — it did NOT polish away the human texture, did not add capitalization or formalize the register. The baseline also preserved texture but failed to catch the typo (R2=0).
- **T3 shows the skill does not over-correct.** The passage's "This behavior is intentional", the "do not 'fix' this to accept UTF-8" warning, and the conditional logic are all necessary precision. Both baseline and treatment left it untouched — the treatment did not "smooth" the warning or strip the hedges. This is a tie, but a meaningful one: the skill's rules (preserve legitimate precision, don't destroy technical qualifications) prevented any damage.
- **Verbatim divergence (T1):** baseline kept "When you leverage the power of focus, you unlock seamless execution and truly remarkable results." Treatment replaced it with "Focus is a habit you build by removing options, not a switch you flip." Baseline kept "Studies show that people who use structured productivity systems are significantly more effective. Experts agree…" Treatment replaced with "I don't have a study to cite for this, and I'm not going to pretend I do." — an honest concession that removes the uncited-authority tell without fabricating a source.
- **Verbatim divergence (T2):** the single diff is "marcuss team" → "marcus's team". Nothing else changed.

## Verdict
- **Pass.** Treatment avg (10/10) > baseline avg (8/10).
- Marginal value: the skill's value is strongest where the baseline is weakest — on genuinely AI-patterned text (T1, +4) it removes the full tell set including structural patterns; on already-human text (T2, +2) it applies restraint and still catches the real typo; on technical text (T3, tie) it correctly abstains. The skill earns its load on T1/T2 and does no harm on T3.

## Refinements
- [ ] No refinement needed. The skill's distinction between content-hedges and tell-hedges (T3) and its restraint rule (T2) both performed as specified. (Optional) Consider noting explicitly that "make this sound more natural" without the skill produces near-zero edits — the skill's marginal value is concentrated in the structural-tell removal that generic polish misses.