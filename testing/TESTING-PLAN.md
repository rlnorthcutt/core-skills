# core-skills — Skill Testing Plan

> How we validate the 23 skills in this catalog: repeated real-task trials,
> scored against defined criteria, producing a report per skill and a
> portfolio-level analysis. Results feed refinement (description/prompt edits)
> and serve as the review record for the team.

---

## 1. Goals

1. **Verify trigger behavior** — does the skill load when it should, and *only* when it should?
2. **Verify output quality** — does following the skill's prompt produce measurably better results than not loading it?
3. **Find refinement targets** — misfires, blind spots, and prompt weaknesses become concrete edits.
4. **Produce a review record** — a durable, citable artifact for the team: what was tested, how, results, decisions.

## 2. Method: A/B trial with rubric scoring

Each skill gets **3 trials** (minimum for signal; 5 for the creator family). Every trial:

1. **Design a realistic task** that matches the skill's documented trigger — drawn from actual usage patterns, not toy examples.
2. **Run twice from the same starting state:**
   - **Baseline:** same task, skill NOT loaded.
   - **Treatment:** same task, skill loaded via `load_skill(name)`.
3. **Score both runs** against the skill's rubric (below), 0–2 per criterion.
4. **Record** scores, observations, and any misfire (loaded when it shouldn't / failed to load when prompted naturally).

The A/B pair is what makes the report honest: it shows the skill's *marginal value*, not just that the agent can do the task.

### Rubric scoring scale (per criterion)

| Score | Meaning |
|---|---|
| 0 | Criterion failed — missing, wrong, or caused harm |
| 1 | Partially met — present but flawed, inconsistent, or shallow |
| 2 | Fully met — correct, complete, no visible defects |

**Rubric totals per trial:** sum of criteria (skill-specific, typically 5 criteria → 0–10). A skill "passes" if treatment averages ≥ 2× baseline AND ≥ 70% of max.

## 3. Trigger tests (in addition to task trials)

For each skill, 2 trigger probes (not scored — pass/fail, recorded):

- **Positive trigger:** phrase a natural user request that should load the skill (from its description's trigger language). Agent has `list_available_skills`. Does it load the right skill?
- **Negative trigger:** phrase a nearby-but-different request. Does it correctly NOT load (e.g. `simplify-code` should not load for a bug report; `review-security` should not load for a style cleanup)?

## 4. Per-skill test specs

Each entry: realistic tasks (T1–T3), rubric criteria (R1–Rn), trigger probes.

---

### review-code
- **T1:** Review a seeded diff containing 3 planted bugs (off-by-one, inverted condition, unhandled None). Compare findings against ground truth.
- **T2:** Review an uncommitted change set in a real repo (omnideck clone): staged edits with 2 subtle regressions (caller not updated, error path swallowed).
- **T3:** Review a PR-style diff with a mix: 1 real bug, 1 style nit, 1 false alarm trap (code that looks wrong but is correct — tests "no speculative findings").
- **Rubric:** R1 correct findings recall (found the planted bugs) · R2 precision (no false positives — trap not flagged) · R3 severity assignment matches impact · R4 findings include file/line + concrete failure scenario · R5 acknowledges what's good; verdict present.
- **Pass signal:** treatment finds all planted bugs; baseline typically misses subtler ones.

### review-security
- **T1:** Seed a small Flask app diff with: SQL string-concat, hardcoded API key, missing authz on an endpoint. Ground truth: all three.
- **T2:** A diff that *touches* trust boundaries but is actually safe (parameterized query, env var secret) — tests false-positive control.
- **T3:** New endpoint added to an existing service — does it check the *surrounding* authz context, not just the diff?
- **Rubric:** R1 finds planted vulnerabilities · R2 precision (safe code not flagged) · R3 attack scenario is concrete (who/what/how) · R4 fix recommendations are systemic (parameterization, middleware), not point patches · R5 severity matches exploitability.
- **Pass signal:** treatment demonstrates the attack path; baseline flags classes without scenarios.

### simplify-code
- **T1:** Seed: duplicated logic (3 near-identical branches), a reinvented stdlib helper, dead flag branch. Expected: all consolidated.
- **T2:** Working code with O(n²) loop + redundant conversions on a hot path — tests efficiency pass without over-optimizing cold code.
- **T3:** Applied-simplification trial: does it actually edit (behavior-preserving) and tests still pass afterward?
- **Rubric:** R1 reuse/simplification findings match seeds · R2 behavior preserved (tests green) · R3 no drive-by changes (no feature creep, no bug-fixing creep) · R4 style-adjacent items flagged, not applied · R5 summary reports what changed and what was left alone.
- **Pass signal:** treatment output is smaller/claerer with tests passing; baseline tends to either miss consolidations or rewrite wholesale.

### write-code
- **T1:** Build a small CLI tool from spec (file parsing + output). Tests: verify-before-success, project folder discipline.
- **T2:** Multi-edit task on an existing file (add feature to a repo clone). Tests: read-before-edit, targeted patch vs rewrite.
- **T3:** Task requiring a backgrounded server + a client check (start server, curl it, report). Tests: long-running process handling.
- **Rubric:** R1 works in/creates proper project folder · R2 reads files before editing; edits are targeted · R3 verifies before claiming success (runs/tests/curls) · R4 long-running processes backgrounded correctly · R5 no stray processes/temp files; reports what was done.
- **Pass signal:** treatment has fewer false "done" claims and no stray processes.

### write-drafts
- **T1:** Email requesting a decision with a deadline from messy context (notes, not prose). Tests: subject-as-message, one ask, purpose first line.
- **T2:** Rewriting a user's drafty 3-paragraph message into a tight version — tests delete-before-decorate, full-text revision delivery.
- **T3:** Bio for a specific platform with constraints (length, third person). Tests: platform conventions, [NEEDS: …] marking for unknowns.
- **Rubric:** R1 purpose in line one · R2 one ask / one message · R3 register matches audience · R4 no filler/performance phrases · R5 unknowns marked, nothing invented.
- **Pass signal:** treatment drafts are sendable-as-is; baseline drafts typically need manual tightening.

### humanize-text
- **T1:** Take a deliberately AI-patterned sample (rule-of-three, em-dash density, "delve", summary performance) — measure tells removed vs. introduced.
- **T2:** A legitimately human-but-rough draft — tests it does NOT overcorrect (meaning preserved, precision kept).
- **T3:** Technical passage with necessary hedges — tests distinction between content-hedges and tell-hedges.
- **Rubric:** R1 pattern categories removed (count vs. seeded list) · R2 no new fake-human tells introduced · R3 meaning preserved exactly · R4 legitimate precision/hedges retained · R5 register matches (formal stays formal).
- **Pass signal:** treatment output scores human on read-aloud; baseline (unedited or generic polish) keeps the tells.

### resolve-recipient
- **T1:** "Send it to Chris" with TWO Chris candidates in contacts (differing evidence strength). Expected: resolves with evidence, asks only if ambiguous.
- **T2:** "Email the team about the release" — group inference from email/calendar history. Expected: roster built + shown, membership reasoned.
- **T3:** Unambiguous case (one exact match, recent thread on same topic). Expected: proceeds WITHOUT asking, still shows the resolution.
- **Rubric:** R1 correct person(s) resolved · R2 evidence cited per candidate · R3 asks narrowly when ambiguous, doesn't interrogate · R4 proceeds without asking when evidence is decisive · R5 group sends get roster review.
- **Pass signal:** treatment never mis-sends; baseline guesses or over-asks. (Use mock contacts data if no live integration.)

### personal-context
- **T1:** Seed memory with a preference + a past rejection ("user rejected pandas approach — broke build"). New request that touches both. Expected: retrieves, applies, doesn't re-propose rejected path.
- **T2:** Elliptical request ("update it", "add the other two") where the referent exists only in seeded memory. Expected: retrieves the right referent; doesn't fabricate.
- **T3:** Fresh conversation, no relevant memory — expected: NO retrieval theater, direct answer.
- **Rubric:** R1 retrieves when prior state matters · R2 applies retrieved context correctly · R3 saves new durable facts (specific, dated) · R4 no fabricated continuity · R5 correctly abstains when memory is irrelevant.
- **Pass signal:** treatment resolves elliptical references baseline can't.

### improve
- **T1:** Session with planted friction (2 corrections by user, 1 repeated instruction, 1 ad-hoc script that should've been a tool). Expected: identifies lessons, proposes right artifact types, right sizes.
- **T2:** Session where the lesson is a memory-write (trivial) — tests smallest-fix rule (proposes memory, not a skill).
- **T3:** Full build trial: go-ahead given — does the created artifact actually work and load?
- **Rubric:** R1 lessons cite actual conversation moments · R2 artifact type/classification correct · R3 smallest-fix principle applied · R4 proposes before building; nothing silent · R5 built artifact verified working.
- **Pass signal:** treatment produces a working artifact matched to the friction; baseline just summarizes.

### create-skill
- **T1:** Turn a described procedure into a skill. Tests: scope interview, record draft, validate, install, verify.
- **T2:** Ambiguous over-broad request ("make a skill for coding") — tests: pushes back, narrows scope rather than shipping sprawl.
- **T3:** Duplicate-detection: request a skill that overlaps an existing one — expected: proposes editing existing, or sharp differentiation.
- **Rubric:** R1 record schema correct (validates) · R2 description states explicit trigger · R3 tool categories minimal + load-bearing · R4 scope discipline (one job; pushes back on sprawl) · R5 installs + verifies loading.
- **Pass signal:** created skill passes validate.py and triggers correctly in a follow-up probe.

### create-agent
- **T1:** Design a profile from a persona description. Tests: minimal skill grants, self-contained system prompt.
- **T2:** Persona with conflicting/implicit needs — tests judgment on model choice + parameter defaults.
- **T3:** Verify trial: spawn the created profile on a task; does it perform without missing context?
- **Rubric:** R1 profile JSON matches AgentProfile schema · R2 system prompt self-contained (fresh agent can act) · R3 skill grants minimal and load-bearing · R4 model/params justified · R5 spawn-verified end-to-end.
- **Pass signal:** spawned agent completes task without needing conversation history.

### create-tool
- **T1:** Build a program-type tool (JSON stdin/stdout) from a described need. Tests: contract compliance, parameter design.
- **T2:** Request that matches an existing tool — tests: extends/composes instead of duplicating.
- **T3:** Failure-path trial: bad input to the tool — clean error, not stack trace; idempotency on rerun.
- **Rubric:** R1 checks existing tools first · R2 JSON-in/JSON-out contract correct · R3 parameters typed, documented, sensibly defaulted · R4 tested happy + failure path before declaring done · R5 registered with useful tags/description.
- **Pass signal:** tool runs via actual runner; second call with same args is safe.

### create-app
- **T1:** Build a small dashboard app (manifest + frontend + 1-2 actions + data persistence). Tests: full layout, SDK invoke, persistence.
- **T2:** "My app isn't showing in the UI" debug — expected: checks manifest + web/index.html existence first.
- **T3:** Large-result action — expected: writes file, returns path + summary (not inline payload).
- **Rubric:** R1 manifest valid (constraints respected) · R2 frontend references assets by path · R3 actions validate inputs, return JSON-safe values · R4 state persists in data/, actions stateless · R5 app appears in UI and full path works (UI → invoke → action → data → UI).
- **Pass signal:** app appears and completes the loop end-to-end.

### write-docs
- **T1:** README for a repo with installable-but-untested instructions — expected: runs the commands, fixes or flags inaccuracies.
- **T2:** API reference from code — expected: parameter tables match actual signatures (no invented params).
- **T3:** Update pass on stale docs — expected: deletes/updates dead content rather than hedging it.
- **Rubric:** R1 claims verified against code (commands run) · R2 right form for the audience · R3 structure scannable (headings, one concept per section) · R4 no marketing language · R5 stale content handled honestly.
- **Pass signal:** treatment docs are executable-as-written; baseline docs typically contain untested commands.

### research
- **T1:** Factual question with a primary source available (e.g. library version support) — expected: finds + reads primary source, cites with date.
- **T2:** Comparison question (2-3 options) — expected: triangulated sources, comparison table, confidence levels.
- **T3:** Deliberately unresolvable/niche question — expected: honestly reports "no reliable sources", doesn't launder guesses.
- **Rubric:** R1 primary-source priority · R2 citation as-you-claim (not lumped) · R3 dates on claims · R4 confidence levels + unknowns stated · R5 answer first, trail after.
- **Pass signal:** treatment output citable by a third party; baseline often single-source confident.

### plan-learning
- **T1:** Learn a stated skill with real time budget (e.g. "I have 4h/week for 8 weeks"). Expected: dependency map, critical path, review-first schedule, card deck.
- **T2:** Over-ambitious budget/goal — expected: cuts scope, defers peripheral nodes, says why.
- **T3:** Prior failed attempt — expected: addresses failure history (usually scheduling), weekly minimum session.
- **Rubric:** R1 goal stated as observable behavior · R2 dependency-ordered plan with critical path · R3 review-first schedule with slack + weekly minimum · R4 cards atomic, traceable to nodes · R5 real resources named (no fabrication).
- **Pass signal:** treatment plan survives the 4h/week reality test; baseline plans assume motivation.

### make-docs
- **T1:** Create a .docx with headings/tables/lists from provided content — tests style-based structure.
- **T2:** Edit an existing docx: add a section at correct heading level without flattening hierarchy.
- **T3:** Render check trial: does it convert to PDF/images and inspect (overflow, broken tables) before delivering?
- **Rubric:** R1 styles used, not manual formatting · R2 outline preserved on edit · R3 front-loaded purpose · R4 render-verified before delivery · R5 content quality (lead with conclusion, no filler).
- **Pass signal:** treatment output opens clean in LibreOffice with correct navigation structure.

### make-sheets
- **T1:** Create workbook from CSV data: types fixed, formulas not baked values, summary sheet separate.
- **T2:** Edit a "broken" spreadsheet (numbers-as-text, mid-column totals) — expected: fixes types first, notes provenance.
- **T3:** Chart trial: chart matches question, reload/round-trip verification before delivery.
- **Rubric:** R1 one variable per column, no merged cells · R2 types correct (dates/numbers) · R3 formulas over baked values · R4 chart matches question with honest encoding · R5 round-trip verified (row counts, computed columns).
- **Pass signal:** treatment workbook re-opens with correct types and computing formulas.

### make-slides
- **T1:** Build a 5-8 slide deck from a topic + data. Tests: story-first, assertion headlines, speaker notes.
- **T2:** Edit an existing deck without restyling (content-only edits preserve template).
- **T3:** Render verification: convert to images, inspect for overflow/overlap before delivery.
- **Rubric:** R1 one idea per slide · R2 headlines are assertions · R3 type scale + restrained palette · R4 speaker notes present · R5 render-verified (no overflow/overlap/broken images).
- **Pass signal:** treatment deck needs no manual layout fixes.

### make-pdfs
- **T1:** Create a styled PDF from HTML source (report with page numbers, tables) — render + visual verify.
- **T2:** Extract from a mixed PDF (text pages + a table page + a scanned page) — expected: right tool per section, detects the scanned page, says so.
- **T3:** Merge + form-fill trial with page-count verification after.
- **Rubric:** R1 right extraction tool per content type · R2 detects scanned/no-text-layer pages · R3 source-format authoring (not hand-editing) · R4 visual verification performed · R5 provenance stated (source, pages, ops).
- **Pass signal:** treatment output verified page-by-page; baseline PDFs typically have a silent defect.

### generate-image
- **T1:** Generate an image to a spec (subject/style/constraints). Tests: camera-brief prompt structure, inspection before delivery.
- **T2:** Icon/logo-set request — expected: correctly routes to code/SVG instead of generation, says why.
- **T3:** Iteration trial: given feedback ("warmer, tighter crop"), tests one-variable-per-iteration discipline.
- **Rubric:** R1 prompt structured (subject→action→setting→style→light) · R2 inspects output with vision before delivering · R3 routes wrong-tool requests to code/vector · R4 iteration changes one variable · R5 final prompt + known flaws reported.
- **Pass signal:** treatment output matches spec on first delivery; baseline needs 3+ manual rounds.

### draw-charts
- **T1:** Data + a question — expected: chart type matches question, title states finding, units labeled.
- **T2:** Dirty data (mixed types, outliers, wrong grain) — expected: hygiene pass before charting, aggregation to question's grain.
- **T3:** Trap: percent-of-total with wrong denominator available — expected: catches it.
- **Rubric:** R1 chart type matches question · R2 encoding honest (zero baseline for bars, color-blind-safe) · R3 data hygiene performed · R4 title states finding · R5 rendered output visually verified.
- **Pass signal:** treatment chart answers the question at a glance; baseline defaults to whatever the library produced.

### visualize
- **T1:** Simulation request (e.g. queue dynamics with parameters) — expected: model stated, sliders, live state, presets.
- **T2:** Static-appropriate request — expected: builds static, explains why (interactivity not earned).
- **T3:** Size/perf trial: dataset too big to inline — expected: aggregates/downsamples, file stays under ~1MB.
- **Rubric:** R1 interactivity earns its keep (or correctly abstains) · R2 model stated before UI · R3 every control has visible effect · R4 one screen, no scroll · R5 file size + performance respected, assets by path.
- **Pass signal:** treatment artifact is genuinely explorable and shares the model; baseline builds a toy animation.

---

## 5. Execution protocol

**Per skill (one session):**
1. Load the skill spec from this file.
2. Prepare fixtures (seeded files, contacts mock, planted bugs) — commit fixtures to `testing/fixtures/` so trials are reproducible.
3. Run 3 A/B trials + 2 trigger probes.
4. Fill `testing/results/<skill-id>.md` (template below).
5. If refinement needed: file it in the results file's "Refinements" section; apply + push as a small commit; note the commit in results.

**Batching:** test in dependency order — creators last (they can fix things mid-trial), content skills first (cheap to iterate). Suggested order: Wave 1 reviews → writing → platform meta (create-*) → office/media.

**Who:** sub-agents can execute trials (spawn with the skill spec + fixtures path). The orchestrator reviews results and applies refinements.

## 6. Result record template

```markdown
# <skill-id> — Test Results (<date>)

## Trials
| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1   | /10           | /10             |       |
| 2 | T2   | /10           | /10             |       |
| 3 | T3   | /10           | /10             |       |

## Trigger probes
- Positive: pass/fail — <what happened>
- Negative: pass/fail — <what happened>

## Observations
- <specific moments, verbatim failures, surprises>

## Verdict
- Pass / Needs refinement / Fail
- Marginal value: treatment avg X vs baseline avg Y

## Refinements
- [ ] <concrete edit: description? prompt section? category grant?>
```

## 7. Portfolio analysis (after batch)

One `testing/REPORT.md` aggregating:
- Pass/refine/fail counts across catalog
- Marginal-value ranking (which skills actually earn their load)
- Cross-cutting weaknesses (e.g. "office skills all fail render-verification")
- Trigger-accuracy table (misfire rates)
- Refinement backlog with priorities
- Recommendation: which skills ship as defaults, which stay install-on-demand

## 8. Fixtures

Reproducible seeds under `testing/fixtures/`:
- `fixtures/bugs/` — seeded diffs for review-code/review-security/simplify-code
- `fixtures/docs/` — docx/spreadsheet/deck inputs
- `fixtures/data/` — CSVs for sheets/charts
- `fixtures/text/` — AI-patterned and human-rough samples
- `fixtures/contacts/` — mock contacts/threads for resolve-recipient

Fixtures carry a `GROUND-TRUTH.md` where applicable (planted bugs, expected findings) so scoring isn't vibes.
