# plan-learning — Trigger Probes

## Positive probe
**Prompt:** "I have 4 hours a week for 8 weeks — help me build a study plan to learn Spanish."
**Expected:** loads `plan-learning`.
**Result:** PASS — description trigger ("Use when the user wants to learn something, build a study plan, or needs a learning schedule") matches directly.

## Negative probe
**Prompt:** "Can you summarize the key points of this paper for me?"
**Expected:** does NOT load `plan-learning` (should load `research`, or just answer).
**Result:** PASS — a summarization request, not a learning-plan request. `plan-learning` correctly not loaded.

## Notes
- `plan-learning` grants `planning` + `memory` + `webfetch` — appropriate for building a plan, persisting it, and verifying real resources.
- Trigger description is clear and distinct from `research` (which is for investigating a question, not scheduling a study plan).