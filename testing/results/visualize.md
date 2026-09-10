# visualize — Test Results (2026-09-10)

## Trials
| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1: M/M/1 queue sim | 3/10 | 10/10 | Baseline = toy animation (no model, no utilization/avg-wait, no presets, no seed); treatment = full M/M/1 with model, live counters, 3 presets, deterministic seed |
| 2 | T2: inventory service architecture | 4/10 | 10/10 | Baseline built a generic static diagram with NO reasoning; treatment chose static deliberately and stated why |
| 3 | T3: contract check on T1 HTML | 4/10 | 10/10 | Baseline had no presets/model; treatment passed all contract checks (size, no-fetch, root IDs, wiring) |

## Trigger probes
- Positive: "build an interactive sim of a queue" → visualize: **pass** — matches the skill's trigger ("interactive", "sim", "what happens if…").
- Negative: "what does this code do" (explanation, no visual needed) → visualize should NOT fire: **pass** — an explanation request, no visual artifact warranted.

## Observations
- **T2 static choice was the key differentiator.** The task "show me the architecture of the inventory service" is a *structure* question. Treatment opened with an explicit reasoning line: "**Why static:** this question asks *what the system looks like* (structure: modules, data flow, test surface), not *what it does under changing parameters*. There is no mechanism to explore, so interactivity would add friction without insight." Baseline produced a generic 3-box SVG with no reasoning about the choice — it happened to be static but did not demonstrate the judgment the skill demands (interactivity correctly abstained *with reasoning*).
- **T1 model-before-UI.** Treatment states the model at the top: "**Model:** M/M/1 queue — Poisson arrivals at rate λ and exponential service at rate μ. Utilization ρ = λ/μ. As ρ → 1, average wait W = 1/(μ−λ) explodes." Baseline had no model statement at all.
- **T1 presets.** Treatment wired three buttons that set values programmatically: `setRates(0.7, 1.0)` (stable ρ=0.7), `setRates(0.95, 1.0)` (near-critical ρ=0.95), `setRates(1.1, 1.0)` (overloaded ρ=1.1). Baseline had **no presets** (grep: "no presets").
- **T1 live state.** Treatment shows utilization ρ, theoretical Lq, theoretical W, and simulated W (Little's law) as live counters, plus a queue-length-over-time canvas with the theoretical mean overlaid as a red dashed line. Baseline only drew a raw queue trace with no counters.
- **T1 deterministic seed.** Treatment includes a seed input wired to a mulberry32 PRNG ("Deterministic option — same seed reproduces the same run"). Baseline used raw `Math.random()`.
- **T3 contract check (treatment) — all PASS:**
  - Size: 8219 bytes < 1MB ✓
  - No fetch/XHR/WebSocket: none found ✓
  - Zero external deps (inline JS only, no CDN) ✓
  - Unique root IDs: `app`, `lam`, `mu`, `presetStable/Near/Over`, `seed`, `rhoVal`, `lqVal`, `wVal`, `wSimVal`, `queueChart` — all unique ✓
  - `getElementById` used 13×; sliders + presets wired via `addEventListener` ✓
  - Presets set values programmatically via `setRates` ✓
- **Validation substitution (honest note):** no browser/node available in this environment, so I could not render the HTML in a real browser. Instead I validated structurally: file size, grep for fetch/XHR/WebSocket/CDN, unique-ID audit, listener wiring by code inspection, and JS syntax via Python re-extraction (string/comment-stripped brace/paren/bracket balance — all balanced, PASS). This is a weaker check than a real render; a headless-browser pass is recommended before shipping the skill's verification claim.
- Environment note: matplotlib was not actually pre-installed (installed via pip); plotly absent; no node/JS parser available (hence the Python re-extraction validation).

## Verdict
- **Pass**
- Marginal value: treatment avg **10.0** vs baseline avg **3.67** (2.7× baseline; ≥70% of max met)

## Refinements
- [ ] (none required — skill performed to spec; consider adding a note that structural validation is a fallback when no browser is available, and that a real render is preferred)