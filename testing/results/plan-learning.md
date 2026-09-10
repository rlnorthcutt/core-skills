# plan-learning — Test Results

Date: 2025 (trial session)

## Trials

| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1: Rust CLI, 4h/week, 3 months | 2/10 | 10/10 | Baseline had no dependency map, no cards, no reviews; treatment produced all three artifacts |
| 2 | T2: ML + Rust + Korean, 6h/week, 2 months | 0/10 | 10/10 | Baseline produced three parallel schedules with no arithmetic; treatment did the math and pushed back |

**Averages:** Baseline 1.0/10 · Treatment 10.0/10

### T1 rubric (baseline vs treatment)
| Criterion | Baseline | Treatment |
|---|---|---|
| R1 goal-behavior test (observable mastery per node) | 0 | 2 |
| R2 dependency order + critical path | 0 | 2 |
| R3 review-first schedule with slack + weekly minimum | 0 | 2 |
| R4 cards atomic + traceable | 0 | 2 |
| R5 real resources, no fabrication | 2 | 2 |
| **Total** | **2** | **10** |

Baseline: a week-by-week list with no dependency reasoning, no critical path, no reviews, no cards, no slack. Its only strength was naming real resources (The Rust Book, Rust by Example, Rustlings). Goal was a single line ("Build a working log-parsing CLI tool in Rust") with no observable per-node mastery.
Treatment: goal stated as observable behavior (write + test a working CLI that filters/aggregates a log file, `cargo test` green); dependency map with critical path N1→N11; lifetimes demoted to supporting and async/macros/wasm explicitly cut; 12-week review-first schedule with ~40% slack and a 15-minute weekly minimum; ~60 atomic tagged cards; real resources (The Rust Book, Rustlings, Rust by Example) each mapped to nodes.

### T2 rubric (baseline vs treatment)
| Criterion | Baseline | Treatment |
|---|---|---|
| R1 does the budget arithmetic | 0 | 2 |
| R2 pushes back / forces prioritization | 0 | 2 |
| R3 any plan produced is depth-honest | 0 | 2 |
| R4 dependency order within chosen scope | 0 | 2 |
| R5 schedule survives 6h/week reality | 0 | 2 |
| **Total** | **0** | **10** |

Baseline verbatim: produced "Three-Domain Learning Plan (6h/week, 2 months)" with three parallel 2h/week tracks and *no* arithmetic — exactly the "three token plans" failure the spec predicts. It never computed total hours, never flagged that 16h/domain is not learning, and budgeted no review time.
Treatment verbatim: "**6 h/week × 8 weeks = 48 hours total.** That is the entire budget. Three domains is not viable at any meaningful depth." It refused to produce three schedules, offered two honest options — (A) one domain with the real plan, or (B) a 6-week sampling plan explicitly labeled shallow ("you will have *sampled* all three, not *learned* any") — and demanded a decision. Option B budgets slack (36h + 12h buffer) and references the review-first discipline.

## Trigger probes
- Positive: PASS — "help me build a study plan to learn Spanish" loads `plan-learning`.
- Negative: PASS — "summarize the key points of this paper" does NOT load `plan-learning`.

## Observations
- **T2 is where the skill earns its keep.** The baseline's three-parallel-schedules output is precisely the failure mode the skill's "cut scope, defer peripheral nodes, say why" and "no plan without a card deck" rules exist to prevent. The treatment's refusal to fabricate three plans is the strongest signal.
- **T1 baseline's only correct element was real resources** — evidence that naming real resources is a low bar the model meets even without the skill; the skill's marginal value is in the *structure* (dependency map, critical path, reviews, cards), which the baseline entirely lacked.
- The skill's "goal-behavior test every node" and "reviews outrank new material" rules directly produced the treatment's observable-mastery framing and review-first schedule — the prompt is load-bearing, not decorative.
- No calendar events or files were created beyond the plan documents, per the trial constraint; the plan itself is the artifact.

## Verdict
- **Pass.** Treatment avg 10.0 vs baseline avg 1.0 → far exceeds 2×; ≥70% of max (10/10).
- T2 treatment did the arithmetic (48h) and pushed back (refused three plans, forced a choice) — both confirmed.
- Marginal value is decisive, especially on the over-ambitious case where the baseline produced actively misleading output.

## Refinements
- [ ] No urgent edits. Optional: the skill could add an explicit "do the budget arithmetic and state the total hours up front" line to the Diagnose section — T2's baseline failure was precisely the absence of that arithmetic, and making it an explicit step would harden the prompt. Low priority (treatment already did it correctly).