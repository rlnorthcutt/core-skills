# Security Review — Treatment (skill: review-security)

**Target:** `users.py` — the "Add user endpoints" commit (diff `HEAD~1`).
**Context reviewed:** `app.py` (baseline notes API) + `users.py` (new endpoints).
**Method:** skill discipline — establish trust boundaries, demonstrate-don't-allege,
match severity to exploitability, treat false positives as costly.

## Trust boundary

Data enters at the HTTP layer and crosses into SQLite via `sqlite3` in `users.py`:

- `GET /users/<int:user_id>` — `user_id` from the URL path.
- `POST /users` — `username` / `email` from the JSON body.

Both are untrusted caller input. Trace each to its sink.

## Findings

### No exploitable findings in this diff.

**Injection (checked, not a finding).** Both queries are fully parameterized:

- `get_user`: `SELECT id, username, email FROM users WHERE id = ?` bound to
  `(user_id,)`. The route converter `<int:user_id>` also coerces the path segment
  to an integer before it reaches the query.
- `create_user`: `INSERT INTO users (username, email) VALUES (?, ?)` bound to
  `(username, email)`.

There is no string interpolation or concatenation of untrusted data into any SQL
statement. An attacker who controls `user_id`, `username`, or `email` cannot
alter the query structure. **No SQL injection is possible here.**

**Error handling / data exposure (checked, not a finding).** `create_user`
catches `sqlite3.IntegrityError` and returns a fixed 409 message; no exception
text or stack trace reaches the client. `get_user` returns a clean 404 on a
missing row. The response payloads expose only `id`, `username`, `email` — no
sensitive fields are stored or returned.

**Secrets (checked, not a finding).** No credentials, tokens, or hardcoded
secrets are introduced by this diff.

## Pre-existing gap (out of scope, hardening only)

The API has **no authentication or authorization layer**. Any caller can supply
an arbitrary `user_id` and read another user's profile (`GET /users/<id>`) or
notes (baseline `GET /notes?user_id=...`) — an IDOR/authorization gap. This is a
**baseline design gap that predates this diff**: the new endpoints are exactly as
exposed as the pre-existing notes endpoints, and this change adds no new
privilege boundary. It is worth one sentence as hardening, not a finding against
this change.

## Recommendations (systemic)

- Add an authentication layer (session/JWT) and an authorization middleware that
  derives `user_id` from the authenticated principal instead of trusting it from
  the request. That single systemic fix addresses the pre-existing IDOR gap
  across both the new and baseline endpoints.
- General hardening only: input-length limits on `POST /users` and rate limiting.
  No demonstrated DoS vector exists in this diff, so nothing here is a finding.

## Verdict

**Ship.** No exploitable findings in this diff. Both queries are parameterized,
error paths are clean, no secrets, and no new attack surface beyond the
baseline's pre-existing (out-of-scope) lack of authentication.