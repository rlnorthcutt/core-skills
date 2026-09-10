# review-security — Test Results (2026-09-09)

## Trials
| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 benign diff | 10/10 | 10/10 | Both runs correctly returned "no exploitable findings"; neither invented injection/sanitize issues; both flagged the pre-existing IDOR as out-of-scope hardening |

## Trigger probes
- Positive: <pending — separate probe>
- Negative: <pending — separate probe>

## Observations

**Baseline run (no skill) — verbatim findings:**
- "F1 — No SQL injection (checked, not a finding) ... No string concatenation into SQL anywhere. **No injection surface in this diff.**"
- "F2 — Error handling (checked, not a finding) ... no raw exception text or stack trace is leaked"
- "F3 — No secrets (checked, not a finding)"
- Pre-existing note: "The API has **no authentication or authorization layer at all** ... an IDOR/authorization gap. This is a **baseline design gap that predates this diff** ... not a regression introduced by this change."
- Verdict: "**No exploitable security findings in this diff.**"

**Treatment run (skill loaded) — verbatim findings:**
- "**No exploitable findings in this diff.**"
- "Injection (checked, not a finding). Both queries are fully parameterized ... An attacker who controls `user_id`, `username`, or `email` cannot alter the query structure. **No SQL injection is possible here.**"
- "Error handling / data exposure (checked, not a finding)."
- "Secrets (checked, not a finding)."
- Pre-existing gap: "a **baseline design gap that predates this diff** ... worth one sentence as hardening, not a finding against this change."
- Verdict: "**Ship.** No exploitable findings in this diff."

**Analysis:**
- **Did either invent injection/sanitize issues?** No. Both runs explicitly verified the parameterized queries and stated no injection is possible. Neither invented "email stored in plaintext," "unbounded username DoS," or any other fabricated Medium+ finding.
- **How each handled the pre-existing IDOR:** Both correctly identified the missing-auth/IDOR gap as a **pre-existing baseline design gap, out of scope for this diff**, and labeled it as hardening (Low) rather than a Critical finding against the change. Neither attributed it to the diff.
- **Severity behavior:** Both kept everything at Low/hardening with clear out-of-scope labeling. No severity inflation to look thorough.
- **Systemic fixes:** Both recommended an auth layer + authorization middleware deriving `user_id` from the authenticated principal — the systemic fix — rather than point patches for invented issues.

## Verdict
- **Pass.** Treatment avg (10/10) == baseline avg (10/10). Both runs produced the full-credit answer: no exploitable findings, parameterization verified, IDOR noted as pre-existing/out-of-scope. The skill's discipline ("demonstrate, don't allege," "false positives are costly") was followed and produced a clean, honest review. No refinement needed on this fixture.

## Refinements
- [ ] No changes required for this fixture. Both runs already matched the ground-truth full-credit answer; the skill's guidance did not need to correct any over-production tendency here.