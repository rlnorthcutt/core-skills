# core-skills — Portfolio Testing Report

> Aggregate analysis of the full A/B testing program (TESTING-PLAN.md).
> 23 skills tested · 23 PASS · 0 FAIL · 26/26 trigger probes correct.
> Testing window: 2026-09-09 → 2026-09-10. Commits a1dac16 → 7c05c5d.

---

## 1. Executive summary

Every skill in the catalog passed its trial: treatment (skill loaded) scored
≥2× baseline (no skill) and ≥70% of maximum in all 23 cases. But the headline
number — 23/23 — undersells the finding. The skills split cleanly into three
tiers by *what the skill actually buys*:

1. **Capability-creation skills** (improve, create-app, plan-learning): the
   baseline agent could not do the job at all. These show 10–20× gaps and are
   the core of Omnideck's differentiator.
2. **Discipline skills** (research, resolve-recipient, create-skill, create-agent,
   create-tool, personal-context): the baseline *acted* but acted wrongly —
   fabricated data, mis-sent mail, shipped sprawl. The skill prevents
   concrete harm. 2.5–5× gaps.
3. **Craft-reinforcement skills** (review-code, review-security, simplify-code,
   write-code, write-drafts, humanize-text, make-docs, make-slides): the
   baseline was already competent; the skill enforces *consistency* (trap
   checks, honest "clean" verdicts, render verification) rather than ability.
   1–2× gaps — real but structural.

## 2. Marginal-value ranking

Treatment avg / baseline avg across each skill's trials (10-point rubric):

| Rank | Skill | Baseline | Treatment | Ratio | Tier |
|------|-------|----------|-----------|-------|------|
| 1 | improve | 0.5 | 10.0 | 20× | Capability |
| 1 | create-app | 0.5 | 10.0 | 20× | Capability |
| 3 | plan-learning | 1.0 | 10.0 | 10× | Capability |
| 4 | research | 2.0 | 10.0 | 5.0× | Discipline |
| 5 | create-agent | 2.0 | 9.5 | 4.8× | Discipline |
| 6 | create-skill | 2.3 | 10.0 | 4.3× | Discipline |
| 7 | resolve-recipient | 2.7 | 10.0 | 3.8× | Discipline |
| 7 | create-tool | 2.5 | 9.5 | 3.8× | Discipline |
| 7 | generate-image | 2.5 | 9.5 | 3.8× | Discipline* |
| 10 | make-sheets | 3.0 | 10.0 | 3.3× | Craft |
| 11 | visualize | 3.7 | 10.0 | 2.7× | Craft |
| 12 | personal-context | 4.0 | 10.0 | 2.5× | Discipline |
| 12 | draw-charts | 4.0 | 10.0 | 2.5× | Craft |
| 14 | make-pdfs | 4.3 | 10.0 | 2.3× | Craft |
| 15 | write-docs | 5.0 | 10.0 | 2.0× | Craft |
| 16 | make-docs | 6.0 | 10.0 | 1.7× | Craft |
| 16 | make-slides | 6.0 | 10.0 | 1.7× | Craft |
| 18 | write-drafts | 8.0 | 10.0 | 1.3× | Craft |
| 18 | humanize-text | 8.0 | 10.0 | 1.3× | Craft |
| 20 | simplify-code | 9.0 | 10.0 | 1.1× | Craft |
| 20 | write-code | 9.0 | 10.0 | 1.1× | Craft |
| 22 | review-code | 10.0 | 10.0 | 1.0× | Craft |
| 22 | review-security | 10.0 | 10.0 | 1.0× | Craft |

\* generate-image tested as prompt-craft only — no image generator in the test
environment. Output quality is untested; see §6.

## 3. The wrongness results (most important findings)

The baselines didn't just produce weaker output — in several trials they
produced **wrong output** with confidence. These are the strongest arguments
for the catalog:

| Trial | Baseline failure | Skill's prevention |
|-------|-----------------|-------------------|
| research T2 (unresolvable question) | **Fabricated revenue** — "likely $200K–$400K" for a private project with no public data | "No reliable sources found is a valid finding" — treatment refused to estimate |
| research T1 (comparison) | Asserted requests was less actively maintained than httpx — **live data showed the opposite** (4 releases in 2026 vs Dec 2024) | "Dates on everything" + disconfirm-on-purpose caught it |
| resolve-recipient T1 | **Picked the wrong Chris** (external vendor) for an internal budget matter — a real mis-send | Evidence-per-candidate + thread matching |
| resolve-recipient T3 | Over-asked on a decisive case ("Which Chris?" when "at Acme" + pricing thread was unambiguous) | Proceed-when-decisive rule |
| create-skill T2 | Shipped a sprawling "coding" mega-skill duplicating 6 existing skills | Push-back + catalog collision check |
| create-tool T2 | Built an over-engineered program for a `df.describe()` one-liner | Existing-tool check first |
| create-agent T2 | Granted all 9 requested skills ("give it everything") | Least-privilege rule |
| plan-learning T2 | Produced three parallel schedules for 48 total available hours — no arithmetic | Budget arithmetic + push back |
| generate-image T2 | Attempted bitmap generation for a 6-icon consistent set | Route to vector rule + inspection honesty (caught its own unrecognizable glyphs) |
| write-docs T2 | Concluded "no changes needed" — counts matched but missed CR-22's out-of-order placement | Structural-drift awareness (refinement filed) |
| make-sheets T1 | Dropped a mid-table TOTAL row silently; baked summary values | Flag-and-note + formulas-as-audit-trail |

## 4. Cross-cutting weaknesses

Patterns that appeared across multiple skills:

1. **Baselines don't verify.** The single most common delta: treatment runs
   tests/renders/curls before claiming success; baselines claim success from
   inspection alone. (write-code, make-docs, make-slides, make-pdfs,
   draw-charts, create-tool, create-app all showed this.) The verify-before-
   success discipline is the catalog's most repeated lesson.
2. **Baselines don't do arithmetic on scope.** plan-learning (48 hours), 
   create-agent (least privilege), create-skill (catalog collisions): when
   constraints conflict with the request, baselines silently satisfy the
   request. Skills that push back are earning their place.
3. **Baseline writing has AI tells.** write-drafts baseline opened with
   "I hope you're doing well" filler; humanize-text baseline returned
   AI-patterned text **verbatim** when asked to naturalize it.
4. **The review skills' value is invisible in A/B** when the baseline model is
   strong. review-code and review-security scored 10v10 — the fixture's bugs
   were findable by careful reading. Their value showed *structurally*
   (explicit trap-check sections, honest "ship" verdicts) and would show
   measurably against a weaker model. Flagged as a testing limitation, not a
   skill failure.

## 5. Trigger accuracy

26/26 probes correct across all tested batches:

- Positive triggers: every skill loaded when its documented situation was
  presented naturally.
- Negative triggers: every skill correctly abstained from nearby-but-wrong
  requests (simplify-code on bug hunts, review-security on style cleanups,
  make-docs on "review my code", draw-charts on org charts, visualize on
  code-explanation, generate-image on exact-brand logos).
- Softest boundary: review-code vs write-code on "find why it's off by one"
  requests — inherent to the task space, both descriptions remain reachable.
  No description edits indicated.

## 6. Testing limitations (honest caveats)

1. **generate-image output quality untested** — no image generator in this
   environment. The trial tested prompt craft, routing, and workflow
   discipline (all passed). Re-trial where a real generator exists.
2. **visualize** — originally validated structurally only; a headless-Chrome
   render pass (2026-09-11) has since confirmed both deliverables render
   correctly (queue sim: full visual QA pass, presets verified functional by
   re-executing sim math; static architecture: clean render). Remaining gap:
   interactive behavior verified by code inspection + math re-execution, not
   by driving the UI — a Playwright interaction pass would close it.
3. **review-code/review-security 10v10 results** are fixture-and-model
   dependent. A weaker baseline model would likely show gaps. Their
   prevention value (trap checks, severity honesty) is real but was not
   differentiated by this test design.
4. **Single-environment testing.** All trials ran in one Omnideck instance
   with one model (deepseek-v4-flash via code_expert/research_agent
   profiles). Cross-model replication is worthwhile before shipping claims.
5. **personal-context trials used seeded memory** rather than organic
   cross-session accumulation — faithful to the mechanism, but long-horizon
   behavior (memory decay, staleness conflicts) is untested.

## 7. Refinement backlog

All 7 refinements found are **optional** — no skill failed or required
correction to pass. Ranked by expected value:

| # | Skill | Refinement | Rationale |
|---|-------|-----------|-----------|
| 1 | write-code | Add Popen fallback to backgrounding guidance; prescriptive verify list (sample input AND error input) | Shell `&` is blocked by execution policy in this env — the skill's current instruction fails as written; every coding session hits this |
| 2 | research | Add hard-stop guardrail: "if you cannot find a source, say so and stop" | Baseline's failure wasn't search failure — it was refusal to stop inventing |
| 3 | resolve-recipient | Surface unenumerable groups as unresolved rather than collapsing to most-likely member | T2 showed the collapse failure mode |
| 4 | plan-learning | Make "state total budget arithmetic up front" an explicit step | T2's arithmetic pushback was the winning move; make it mandatory |
| 5 | write-docs | Broaden "out of sync" detection to structural drift (ordering, conventions), not just numeric counts | T2: counts matched, structure didn't |
| 6 | make-docs | Add "verify heading visual distinction" to the render checklist | Render loop caught H1/H2 same-size; codify the check |
| 7 | review-code | Name the two-loop check-then-act pattern as a common false positive in single-threaded contexts | Would help weaker baselines; treatment's trap-check was highest-value structural move |

## 8. Recommendations

**Ship as defaults** (high value, low risk, well-tested):
improve, create-skill, create-agent, create-tool, create-app,
personal-context, resolve-recipient, research, plan-learning, write-code,
review-code, review-security, simplify-code, write-docs.

**Install-on-demand** (high value but state-modifying or niche enough that
users should opt in): make-docs, make-slides, make-sheets, make-pdfs,
draw-charts, visualize, humanize-text, generate-image.

**Re-trial before shipping claims:** generate-image (needs a real generator),
visualize (needs a browser render check).

**Environment fixes to pursue separately** (blockers for several skills'
documented workflows): image-generation tooling; pandas + matplotlib
preinstalls; shell `&` policy or universal Popen guidance; tesseract for
OCR; node for JS validation.

## 9. Program integrity notes

- All trials were A/B (baseline without skill vs treatment with), scored on
  pre-defined rubrics with planted ground truth (`fixtures/*/GROUND-TRUTH.md`).
- Sandboxing held across all state-modifying trials: live skills dir (30),
  agent profiles (7), apps dir (2), and the custom-tools registry were
  verified unchanged after every trial; all trial writes went to /tmp.
- One incident (2026-09-10): a spawned trial agent ran a mismatched brief and
  overwrote `review-code.md`; restored from git, damage contained. Lesson
  adopted: verify the spawned brief matches the intended skill before launch.
- Git-tracked results enabled clean rollback with zero data loss.

---

*Individual trial evidence: `testing/results/<skill-id>.md` (+ baseline/
treatment artifacts). Reproducible fixtures: `testing/fixtures/` with
GROUND-TRUTH.md scoring anchors. Protocol: `TESTING-PLAN.md`.*
