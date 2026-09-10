# write-docs — Trigger Probes

## Positive probe
**Prompt:** "Can you write a README for my new project?"
**Expected:** loads `write-docs`.
**Result:** PASS — description trigger language ("Write and maintain technical documentation — READMEs… Use when the user asks for docs, a README") matches directly. Skill loads.

## Negative probe
**Prompt:** "My code has a bug where the total is off by one — can you look at the diff?"
**Expected:** does NOT load `write-docs` (should load `review-code`).
**Result:** PASS — this is a bug-review request, not a docs request. `write-docs` correctly not loaded; `review-code` is the right skill.

## Notes
- `write-docs` grants `coding` + `webfetch` tool categories — appropriate for reading code and verifying commands.
- The skill's description is precise about the trigger (docs/README/guide/documentation updates), which makes the negative probe clean.