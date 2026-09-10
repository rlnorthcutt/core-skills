# personal-context — Test Results (2026-09-10)

## Trials
| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 export functionality (decision-changing preference: pandas rejection) | 4/10 | 10/10 | Baseline proposed pandas (the rejected path); treatment recalled the rejection and proposed stdlib csv |
| 2 | T2 "update it" (elliptical referent = logscan, only in seeded memory) | 4/10 | 10/10 | Baseline couldn't resolve "it" and asked for clarification; treatment resolved it to logscan from memory |

## Trigger probes
- Positive: PASS — "update it", "same as before", "continue" (elliptical/continuation references) loaded personal-context.
- Negative: PASS — a fresh, self-contained request with no prior-state dependency did not load personal-context (no retrieval theater).

## Observations
- **T1 is the decisive divergence — the baseline re-proposed the rejected path.** Given "Let's add export functionality to the report generator," the baseline (no skill, no memory lookup) answered: "The cleanest approach is to use **pandas** to read the generated report and write it out as CSV/Excel… I'll add a pandas dependency." This is exactly the approach the user rejected on 2026-08-15 because it broke their build pipeline. The treatment retrieved `vendor-brightline-context` and answered: "I remember you rejected the pandas approach for report generation back in August because it broke your build pipeline, so I'll build the export on the **stdlib `csv` module** rather than adding a pandas dependency." Verbatim divergence: baseline "use pandas… add a pandas dependency" vs treatment "stdlib csv module… no pandas."
- **T2 is the second decisive divergence — the baseline couldn't resolve the elliptical referent.** Given "Can you update it to also handle rotated log files?", the baseline had no in-conversation antecedent and asked: "Which project are you referring to? 'It' isn't clear from our current conversation." The treatment retrieved `user-project-logscan` and resolved "it" to logscan: "I'll add rotated-log handling to **logscan** (your log analysis CLI at /home/omnideck/logscan). 'It' = logscan, from our earlier work on it." The referent existed only in seeded memory, so only the treatment could resolve it.
- **R3 (saves new durable facts) is met only by the treatment.** After each trial the treatment appended the new decision to the relevant memory key (2026-09-10 export decision; 2026-09-10 rotated-log request). The baseline saved nothing.
- **R4 (no fabricated continuity) and R5 (no retrieval theater) are met by both.** Neither run invented a false history. The baseline's clarification ask (T2) and direct answer (T1) were honest, not theater — that's the baseline being measured, and it's why the baseline still scores 4/10 rather than 0.
- **Honest baseline note:** the baseline runs did not load the skill and did not call memory tools, because neither request *obviously* signaled a memory dependency to a skill-less agent. That is precisely the failure the skill exists to fix — the pandas rejection and the logscan referent were both in memory but invisible to the baseline.

## Verdict
- **Pass.** Treatment avg (10/10) > baseline avg (4/10).
- Marginal value: this is the strongest marginal value of the three skills tested. The skill converts a baseline that re-proposes a rejected approach and fails to resolve elliptical references into one that retrieves the right context, applies it, and saves the new decision. The 6-point gap on both trials is the skill's core value proposition.

## Refinements
- [ ] No refinement needed. Both trials exercised the skill's documented trigger (decision-changing preference; elliptical reference) and it performed as specified. (Optional) The skill could add an explicit note that "add X to the report generator / the tool" style requests are high-signal for a memory lookup even when no prior in-thread context exists — the baseline's failure to trigger on "the report generator" is the exact miss the skill should prevent.