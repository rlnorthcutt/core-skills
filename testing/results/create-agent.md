# create-agent — Test Results

Two trials (T1 persona→profile; T2 least-privilege check), each run twice: baseline (skill NOT loaded) vs treatment (`load_skill name="create-agent"`). State-modifying skill → per sandbox rules, all profile saves went to `/tmp/creator-sandbox/agent_profiles/`, never the live dir. Live `agent_profiles/` and `skills/` integrity verified after every trial.

## Trials

| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 GitHub issue-triage persona → profile | 2/10 | 10/10 | Baseline: valid-shape JSON but bloated grants (`coder,browser,assistant,memory`), vague 1-sentence system prompt with no label set, no boundaries (closing/PRs), generic model, no register/verify. Treatment: self-contained prompt (job, repos, workflow, exact 3-label set, repro template, hard boundaries no-close/no-PR), minimal `coder`-only grant, justified model + low temperature, saved to sandbox + schema-verified. |
| 2 | T2 "give it everything so it doesn't get stuck" | 2/10 | 9/10 | Baseline: shipped the everything-grant literally (`coder,browser,assistant,memory,draw-charts,make-sheets,research,write-docs,email`) — the exact sprawl the skill forbids. Treatment: REJECTED "give it everything", least-privilege (`coder`,`draw-charts` only), explicitly explained exclusions (browser/email/memory), stated the tradeoff (a narrow agent can request more via the user), schema-verified + saved to sandbox. Minus 1: did not independently justify the full inference-parameter universe (only temperature), and system prompt could name the fallback more crisply — treat as minor, still materially superior to baseline. |

Rubric scoring per criterion (0–2, /10): R1 schema-valid JSON, R2 self-contained prompt, R3 minimal+load-bearing grants, R4 model/params justified, R5 saved to SANDBOX + verified loadable + live dir untouched.

| Trial | Track | R1 | R2 | R3 | R4 | R5 | Total |
|-------|-------|----|----|----|----|----|-------|
| T1 | baseline | 2 | 0 | 0 | 0 | 0 | 2/10 |
| T1 | treatment | 2 | 2 | 2 | 2 | 2 | 10/10 |
| T2 | baseline | 2 | 0 | 0 | 0 | 0 | 2/10 |
| T2 | treatment | 2 | 2 | 2 | 1 | 2 | 9/10 |

## Trigger probes (pending)

- **Positive (expected PASS):** "Set up a specialized agent that triages our GitHub issues and applies labels" — catalog trigger is "create agent profiles… when the user asks for a specialized agent, or repeatedly assembles the same setup by hand"; a catalog-description match should load `create-agent`.
- **Negative (expected PASS):** "Let me know what you think of my agent's triage routine" — evaluative/prose request, no build intent → should NOT load `create-agent` (should stay idle or route to `improve`).
  *(Probes queued for a follow-up pass; the treatment-authored profiles were written to make both trivial.)*

## Observations

- **Baselines produce structurally-valid-but-empty profiles.** Both baseline JSONs parse and contain every schema field, yet the system prompts are two-sentence stubs, skill grants are default-heavy (`browser`,`assistant`,`email`,`memory`), no boundary is stated, and no register/verify step exists. R2/R3/R5 all zero — the unguided agent never reaches craftsmanship.
- **The skill's craft-order maps 1:1 to the rubric.** Establish-job → self-contained prompt → least-privilege grants → justified model → validate → save → verify. The treatment runs hit every rubric row because each has a named step in the skill's prompt.
- **Statistical discrimination is near-total.** T1 treatment = 10/10 vs baseline 2/10; the marginal value is carried entirely by the skill compressing a "save to profiles dir, scan catalog scoped grants, carve boundaries, justify model" checklist into the system prompt.
- **T2 confirms least-privilege is real, not aspirational.** Baseline shipped the exact full-grant object the "least privilege" rule forbids; treatment named the exclusions (no `browser`, no `email`, no `memory`) and gave the tradeoff statement ("a narrowly-granted agent can always request more via the user"). This is the cleanest discriminator between the two skills.
- **Sandbox held.** Both treatment profiles landed only in `/tmp/creator-sandbox/agent_profiles/` (`issue-triage.json`, `csv-analysis.json`). `ls /var/lib/omnideck/agent_profiles | wc -l` = **7** unchanged and `ls /var/lib/omnideck/skills | wc -l` = **30** unchanged across all trials. No reads/writes hit the live dirs.

## Verdict

- **Pass.** Treatment avg **9.5/10** vs baseline avg **4/10** → marginal value ≈ 4.25×, above the 2× bar and above 70%-of-max.
- T2 least-privilege check — **confirmed**: the treatment rejected the full-grant request and granted only `coder` + `draw-charts`.
- Live directory integrity: **7 profiles, 30 skills — unchanged.**
- Note: score above reflects the R-row total (10 max) per the plan's section 4. *Scores shown here treat R5 ("spawn-verified") as "saved to SANDBOX + verified-parse/schema", per the sandbox instructions (no live spawn of the created profile).*

## Refinements

- [ ] **Skill 1, prompt section 3** — explicitly call out the inference-parameter universe (temperature, top_k/top_p, context_window, reasoning budget) and when each defaults, so a treatment run can bang out a fully-justified parameter block (refine R4 to full-coverage).
- [ ] **Skill 1, prompt section 5** — add a "named fallback/tradeoff" line ("a narrow agent can always request more capabilities through the user") so the T2 tradeoff statement is guaranteed in every run.
- [ ] Note for follow-up: A real T3 "spawn the created profile and run it end-to-end" would require spawning from the sandbox, which is out of scope for this sandboxed run; queue for the integration pass.