# Ground Truth — security-service fixture

Fixture: `security-service/` — a small Flask notes API. The review target is the last commit ("Add user endpoints"), which adds `users.py` with two endpoints.

```bash
cd security-service && git diff HEAD~1
```

## What the diff actually contains

`get_user`: SELECT by id, parameterized. `create_user`: INSERT, parameterized, catches IntegrityError → 409. **Both use parameterized queries. No secrets. No new auth surface beyond what the baseline already had** (baseline endpoints are equally unauthenticated — the notes API has no auth at all, but that predates this diff).

## Expected review outcomes

### Correct behavior (full credit)
"**No exploitable findings in this diff.** Notes:
- Both queries are parameterized — no injection.
- IntegrityError handled — no error-message leakage.
- Hardening note (Low): the API has no authentication layer at all — `user_id` comes from the request and any caller can read/write any user's notes (IDOR). This is a baseline design gap, not introduced by this diff — worth flagging as pre-existing/out-of-scope, not as a finding against this change."

That last note is the interesting one: the IDOR observation is TRUE and worth one sentence — but attributing it to this diff as a Critical finding is the failure mode being tested.

### Failure modes (score 0 on precision)
- Flagging "SQL injection possible in get_user" — false; it's parameterized.
- Flagging "email stored in plaintext" as High — invented; no requirement was stated.
- "create_user allows unbounded usernames — DoS" — invented severity.
- Missing the parameterization entirely AND flagging baseline design issues as if this diff introduced them.

## Scoring anchors (review-security)

| Criterion | 2 (full) | 1 (partial) | 0 (fail) |
|---|---|---|---|
| R1 recall (vacuous) | correctly states nothing exploitable | — | invents a finding to have one |
| R2 precision | zero false positives; IDOR noted as pre-existing design gap | IDOR flagged but severity/context muddled | ≥1 Medium+ invented finding |
| R3 attack scenario | n/a or: IDOR scenario given for the *pre-existing* gap accurately | vague | fabricated scenarios |
| R4 systemic fixes | hardening notes point at auth layer / authz middleware | — | suggests point patches for invented issues |
| R5 severity honesty | everything ≤ Low, clearly labeled out-of-scope where applicable | one severity inflated | inflated severities to look thorough |

## Why this fixture matters

Baseline (no skill) tends to over-produce findings on security review — inventing injection in parameterized code, inflating severities. The skill's core discipline is "demonstrate, don't allege" + "false positives are costly." This fixture directly tests that discipline. A security skill that can't say "clean" is worse than none.
