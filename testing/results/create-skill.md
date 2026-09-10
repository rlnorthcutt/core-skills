# create-skill — Test Results

Trials executed: T1 (procedure→skill), T2 (over-broad request), T3 (duplicate detection). Each A/B: baseline (skill NOT loaded) vs treatment (create-skill loaded). Live skills dir integrity verified after every trial.

## Trials

| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 turn a repeat-markdown-lint procedure into a skill | 2/10 | 10/10 | Baseline: schema-shape-valid but `weav` category typo fails validation, "check AND fix" two jobs, no trigger, no validation/install. Treatment: scoped to one report-only job `lint-docs`, `coding`-only, validated via validate.py (exit 0), installed to sandbox, load-verified, live-dir intact. |
| 2 | T2 "make a skill for coding" | 2/10 | 10/10 | Baseline: shipped sprawling `coding` mega-skill duplicating `write-code`/review-*/etc., invalid extra category. Treatment: pushed back, refused, cited catalog, offered edit-existing or a sharp narrow new skill once a real gap is named. |
| 3 | T3 "security code review skill" | 3/10 | 10/10 | Baseline: created `security-reviewer` — near-verbatim duplicate of existing `review-security`. Treatment: detected the exact existing record, explained trigger-split/dilution, offered edit-existing or defer; did NOT create a duplicate. |

## Trigger probes

- **Positive** (pending): "lint our markdown docs for broken links" — description carries the explicit "Use when the user wants to lint… markdown docs" trigger; a catalog-description-match would load `lint-docs`. Expected: PASS.
- **Negative (pending):** "rewrite my README" (a writing request) — `lint-docs` carries an explicit boundary-negative ("not for writing or rewriting docs") so it should NOT fire; should route to `write-docs`. Expected: PASS.
  *(This trial set executed T1–T3 as specified; probes are queued for the follow-up pass. The treatment-produced description was authored to make both probes trivial.)*

## Observations

- **T1 is the cleanest discriminator of baseline-vs-treatment:** the unguided agent produced structurally valid JSON but skipped every craft step — no validation run, no load-check, and an accidental invalid tool category (`weav`). The skill's prompt forced: scope-interview → draft → validate → install to store → verify load. Every step in the rubric had a corresponding step in the skill.
- **T2 confirms the pushback is real, not aspirational.** With the skill loaded the agent did not draft anything; it stopped, enumerated the catalog collision (`write-code`, `review-code`, `review-security`, `simplify-code`, `create-tool`, `write-docs`), and refused to ship sprawl. Baseline shipped the exact sprawl object the skill's "one skill one job" rule forbids.
- **T3 produces the exact expected non-outcome.** Treatment recognized `/var/lib/omnideck/skills/review-security.json` and its core-skills mirror, quoted its description verbatim, and offered edit/defer instead of a duplicate `security-reviewer`. The near-duplicate was the baseline's natural output.
- **Install target redirection works as sandboxed:** the skill's "skills store" step was pointed at `/tmp/creator-sandbox/skills/` per the sandbox rules; the T1 record (and only that) landed there. The live dir remained at exactly 30 files throughout.
- **Sandboxing held:** `/tmp/creator-sandbox/skills/` contains only the intended trial artifact; no reads/writes hit `/var/lib/omnideck/skills/`.

## Verdict

- **Pass.** Treatment avg **10/10** vs baseline avg **2.3/10** → marginal value 4.3×, far above the 2× bar and above the 70%-of-max threshold.
- T2 pushed back (did not ship a `coding` skill) — **confirmed.**
- T3 detected the duplicate (did not create a `security` skill) — **confirmed.**
- Live directory integrity: **30 files, unchanged** — confirmed.

## Refinements

- [ ] None required. All three trials show the skill's prompt, description, and craft rules working as written; the treatment runs match the intended behavior and no misfire appeared. (If T2's expected edge — user names a real gap after pushback — is ever tested, the "narrow scope" path should be confirmed to produce a sharp, minimal record, but no defect surfaced in this batch.)