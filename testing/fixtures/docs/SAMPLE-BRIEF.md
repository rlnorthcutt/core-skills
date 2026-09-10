# Office & Media Batch — Fixture Briefs

Shared input briefs for the final 7 skills. Each trial uses these as the task prompt; expected quality markers listed per skill in TESTING-PLAN.md.

## make-docs (T1 source content)

Content for a "Quarterly Data-Retention Policy" internal doc, deliberately provided as loose notes (not prose):

- Purpose: comply with new data-retention rule; applies to customer analytics DBs
- Retention periods: raw event data 13 months, aggregated rollups 3 years, backups 90 days
- Exception: legal hold suspends deletion; ops team maintains holds list
- Rollout: effective first day of next quarter; eng owns deletion jobs; DPO owns exceptions
- Contact: privacy@ for questions
Expected: outline-first, styles-based, front-loaded purpose, one topic per section, no invented facts.

## make-sheets (T1 data)

Use a small CSV the tester generates inline (10-15 rows, e.g. weekly sales: date, region, units, unit_price) plus one deliberate type problem: dates as text strings for 2 rows, and one mid-table total row pasted in. The task: "clean this up and add a summary by region with a chart." Expected markers in plan: types fixed, totals not baked, summary separate region, chart answers one question.

## make-slides (T1 content)

Topic: "Why we're adopting trunk-based development." Audience: engineering org all-hands. Data to include: branch lifetime avg dropped 40% in pilot team, merge conflicts per week dropped from 12 to 3, 2 teams piloted over 6 weeks. Expected: story-first (3-5 moves), assertion headlines citing the data, speaker notes, ≤25 words/slide body, verified rendering.

## make-pdfs (T1 task)

"Create a one-page onboarding checklist PDF for new repo contributors: setup steps (clone, venv, install deps, run tests), code style rules (line length 100, type hints required), PR rules (small PRs, tests required, one approval), and where to ask questions (#dev channel). Make it printable." Expected: source-format authoring (HTML→PDF), render-verified via pdftoppm, no clipped content, page fits.

## generate-image (T1 spec)

Spec: "An illustration for the engineering blog post about trunk-based development: a single main branch with small short-lived branches merging in, clean modern flat style, blue accent color, suitable for a hero image 1200x630." Expected: structured camera-brief prompt, inspection before delivery, honest report of flaws (text rendering avoided), final prompt reported.

T2 (wrong-tool probe): "Design me a set of 6 UI icons for the app toolbar (save, undo, redo, settings, search, help). Consistent style." Expected: routes to SVG/code instead of generation, with reasoning — or generation attempted with explicit consistency caveat and failed-then-switched honesty.

## draw-charts (T1 question)

Data: the same weekly sales CSV from make-sheets. Question: "Which region grew fastest over the period?" Expected: chart type matches (line or slope, not pie), sorted/annotated for the answer, title states the finding ("Region X grew fastest: +N units"), units labeled, visual verification performed.

## visualize (T1 mechanism)

Mechanism: "Show me how a queue with Poisson arrivals behaves as service rate approaches arrival rate — I want to see utilization vs wait time explode." Expected: model stated (M/M/1), sliders for λ and μ, live state (queue length, wait time), preset scenarios (stable / near-critical / overloaded), single screen, assets by path, file <1MB.

T2 (static probe): "Show me the architecture of the inventory service (models, service, tests, CLI)." Expected: static diagram (SVG/HTML), NOT an interactive build — with one-line reasoning why static is right.
