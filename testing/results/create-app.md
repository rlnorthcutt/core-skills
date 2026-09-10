# create-app — Test Results (2026-09-10)

Two trials (T1 build a small pomodoro/focus app; T2 debug "my app isn't showing up"), each run twice: baseline (skill NOT loaded) vs treatment (`load_skill name="create-app"`). State-modifying skill → per sandbox rules, all apps were built under `/tmp/creator-sandbox/apps/`, NEVER the real `/home/omnideck/apps/`. Live apps-dir integrity verified after every trial. Actions were executed through the real runner (`server/_custom_app_runner.py`) to simulate the server's fresh-subprocess invoke path.

## Trials

| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 pomodoro/focus app | 1/10 | 10/10 | Baseline: manifest had extra fields (`version`, `author`) + non-`bi-*` icon (`"clock"`), actions NOT `@action`-decorated, `get_today_total` returned a bare string, state written to `sessions.log` in app root (not `data/`), frontend never used SDK invoke. Treatment: valid manifest (`bi-clock`), `web/index.html` with working static JS timer + SDK `invoke`, two `@action` backend actions with input validation, stateless actions persisting to `data/sessions.json`, verified end-to-end via the real runner. |
| 2 | T2 debug "app isn't showing" | 0/10 | 10/10 | Baseline: guessed at permissions/registration/cache/server-restart — never checked the discovery requirements, left both root causes unfixed. Treatment: checked manifest + `web/index.html` existence FIRST (skill Rule 4), spotted the extra `version` field (extra=forbid → parse failure) AND the missing `web/index.html`, fixed both, and confirmed `@action` is what makes functions callable. |

Rubric scoring per criterion (0–2, /10): R1 manifest valid (constraints respected), R2 assets by path + frontend sound, R3 actions validate inputs + JSON-safe returns, R4 stateless actions + state in `data/`, R5 verified end-to-end (actions run, manifest parses, structure complete) / for T2: both root causes found.

| Trial | Track | R1 | R2 | R3 | R4 | R5 | Total |
|-------|-------|----|----|----|----|----|-------|
| T1 | baseline | 0 | 1 | 0 | 0 | 0 | 1/10 |
| T1 | treatment | 2 | 2 | 2 | 2 | 2 | 10/10 |
| T2 | baseline | 0 | 0 | 0 | 0 | 0 | 0/10 |
| T2 | treatment | 2 | 2 | 2 | 2 | 2 | 10/10 |

## T1 treatment — actual runner runs (verbatim)

Runner convention matched: `echo '<json>' | python3 -I server/_custom_app_runner.py <app_dir> <action>` (fresh subprocess, JSON over stdin, JSON envelope on stdout — the real `_invoke_custom_app_action` path). Artifact: `create-app-t1/focus-timer/`.

**Manifest validation (extra=forbid, bi-* pattern):**
```
manifest VALID: {'title': 'Focus Timer', 'description': 'Pomodoro focus timer with session history and today's total focus time.', 'icon': 'bi-clock'}
```

**log_session happy path:**
```
$ echo '{"args":{"duration_minutes":25}}' | python3 -I .../focus-timer log_session
{"ok":true,"result":{"ok":true,"session":{"id":1,"duration_minutes":25,"day":"2026-09-10","logged_at":"2026-09-10T02:46:06.520943+00:00"}}}
```

**log_session validation (bad input):**
```
$ echo '{"args":{"duration_minutes":-5}}' | python3 -I .../focus-timer log_session
{"ok":true,"result":{"ok":false,"error":"duration_minutes must be between 1 and 600"}}
```

**get_today_total (state read back from data/sessions.json):**
```
$ echo '{"args":{}}' | python3 -I .../focus-timer get_today_total
{"ok":true,"result":{"ok":true,"day":"2026-09-10","total_minutes":25,"session_count":1}}
```

**data/sessions.json persisted** (not app root): a JSON list of session records with `id`, `duration_minutes`, `day`, `logged_at`.

## T2 treatment — both root causes found (verbatim)

Per skill Rule 4 ("Manifest and index.html must exist or the app won't appear — check both first when debugging"), the treatment checked discovery requirements first:

```
Step 1 — check discovery requirements FIRST:
  omnideck.json exists: True
  web/index.html exists: False          <-- ROOT CAUSE 2

Step 2 — validate manifest (extra=forbid):
  manifest FAILS: [(('version',), 'extra_forbidden')]   <-- ROOT CAUSE 1

Step 3 — check @action decorator on app.py functions:
  get_message decorated? False (decorator is what makes functions callable)
```

Both root causes were identified BEFORE fixing, then fixed and re-verified:
- Removed the extra `version` field → manifest now parses (`extra=forbid` satisfied).
- Created `web/index.html` → discovery requirement met.
- Added `@action` to `get_message` → now callable via the runner (`{"ok":true,"result":{"ok":true,"message":"Hello Omnideck"}}`), with input validation on the empty-name failure path.

## Trigger probes (pending)

- **Positive (expected PASS):** "Build me a dashboard app that tracks my daily habits" — catalog trigger is "use when the user asks for an app, a dashboard, a tool with a UI, or something to open in its own window"; description-match should load `create-app`.
- **Negative (expected PASS):** "Summarize this data into a quick chart for me" — a one-off chart request, no app/dashboard/window intent → should NOT load `create-app` (should route to `draw-charts`).
  *(Probes queued for a follow-up pass; the treatment-authored apps make both trivial.)*

## Observations

- **The discovery requirement is the single highest-value discriminator.** The baseline never knew that `omnideck.json` + `web/index.html` are what make an app appear — it guessed at permissions, registration, cache, and server restart. The skill's Rule 4 ("check both first when debugging") turned T2 into a two-minute, both-root-causes fix.
- **Manifest strictness is a clean R1/R5 test.** `extra="forbid"` means any stray field (`version`, `author`) fails discovery silently. Baseline shipped two extra fields plus a non-`bi-*` icon; treatment shipped exactly `title`/`description`/`icon` with `bi-clock`.
- **Stateless actions + `data/` persistence is a real craft point.** Baseline wrote `sessions.log` into the app root and returned a bare string from `get_today_total` (not JSON-safe, not a dict). Treatment read/wrote `data/sessions.json` on every fresh-subprocess call and returned JSON-safe dicts — matching the runner's "no in-memory state between calls" contract.
- **The `@action` decorator is load-bearing.** The runner only registers functions carrying the `__omnideck_action_name__` attribute set by `@action`. Baseline's undecorated functions were invisible to the runner; treatment (and the T2 fix) used `@action` and verified callability through the real runner.
- **Verification through the real runner is faithful.** Using `server/_custom_app_runner.py` exercised the exact fresh-subprocess, JSON-in/JSON-out envelope the server uses, so R5 ("actions run") is grounded, not simulated.
- **Sandbox held.** All apps live only under `/tmp/creator-sandbox/apps/` (`focus-timer`, `broken-app`). `ls /home/omnideck/apps/` = **2** (omnideck-refresh, omnideck-ui-refresh) unchanged across all trials.

## Verdict

- **Pass.** Treatment avg **10/10** vs baseline avg **0.5/10** → marginal value ≈ 20×, far above the 2× bar and 70%-of-max.
- T2 both root causes — **confirmed**: the treatment identified the extra manifest field AND the missing `web/index.html` before fixing, and confirmed the `@action` decorator requirement.
- Live integrity: **2 apps in /home/omnideck/apps/ — unchanged.**

## Refinements

- [ ] **Skill, Rule 4** — already strong; consider adding the exact discovery predicate to the debug path: "an app is discovered only if `omnideck.json` parses under `extra='forbid'` AND `web/index.html` exists — check these two before anything else." (Mostly codifies what already worked; low priority.)
- [ ] **Skill, Backend actions section** — add an explicit note that undecorated functions are invisible to the runner (the `@action` decorator is what registers them), so a debug run can state this as a third possible root cause alongside manifest/index.html. This is the one thing T2's baseline would still miss after fixing the two discovery causes.
- [ ] Consider a T3 "large-result action" trial (per the plan's create-app T3: write file, return path + summary) to confirm the ~1MB response-limit guidance is followed; queued for a follow-up pass.
