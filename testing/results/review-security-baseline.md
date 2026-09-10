# Security Review — Baseline (no skill)

**Target:** `users.py` — the "Add user endpoints" commit (diff `HEAD~1`).
**Context reviewed:** `app.py` (baseline notes API), `users.py` (new endpoints).
**Reviewer mode:** plain security pass, no skill guidance.

## Scope

The diff under review adds two endpoints to the notes API:

- `GET /users/<int:user_id>` — fetch a user profile by id.
- `POST /users` — register a new user.

The baseline `app.py` (notes list/create) is unchanged by this diff and is
reviewed only for context.

## Findings

### F1 — No SQL injection (checked, not a finding)
Both new queries use parameterized statements with `?` placeholders:

- `get_user`: `SELECT id, username, email FROM users WHERE id = ?` with `(user_id,)`.
- `create_user`: `INSERT INTO users (username, email) VALUES (?, ?)` with
  `(username, email)`.

`user_id` is also constrained by the Flask route converter `<int:user_id>`, so it
is already an integer. No string concatenation into SQL anywhere. **No injection
surface in this diff.**

### F2 — Error handling (checked, not a finding)
`create_user` catches `sqlite3.IntegrityError` and returns a generic 409 with a
fixed message — no raw exception text or stack trace is leaked to the client.
`get_user` returns a clean 404 on a missing row. No information disclosure via
error messages.

### F3 — No secrets (checked, not a finding)
No credentials, API keys, tokens, or hardcoded secrets are introduced. User
profiles expose only `id`, `username`, `email` — no password or sensitive fields
are stored or returned.

## Pre-existing / out-of-scope note

The API has **no authentication or authorization layer at all**. Any caller can
supply an arbitrary `user_id` (in `GET /users/<id>` and in the baseline
`GET /notes?user_id=...`) and read another user's profile or notes — an
IDOR/authorization gap. This is a **baseline design gap that predates this
diff**; the new endpoints are no more (and no less) exposed than the existing
notes endpoints. It is worth flagging as hardening, but it is not a regression
introduced by this change.

## Recommendations

- Add an authentication layer (session/JWT) and an authorization check so that
  `user_id` is derived from the authenticated principal rather than trusted from
  the request. This is the systemic fix for the pre-existing IDOR gap.
- Consider rate-limiting / input-length validation on `POST /users` as general
  hardening, but there is no demonstrated DoS vector in this diff.

## Verdict

**No exploitable security findings in this diff.** The new code follows the
baseline's parameterized-query pattern, handles its error cases cleanly, and
introduces no new attack surface. The only notable issue (missing auth / IDOR)
is a pre-existing baseline design gap, not something this change introduces.