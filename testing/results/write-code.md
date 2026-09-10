# write-code — Test Results (2026-09-10)

## Trials
| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 logscan CLI + server | 9/10 | 10/10 | Both built identical working tool + 5 passing tests + verified server; treatment's only edge is extra verify-own-work (edge-case run) per skill's read-before-edit/verify-after-edit discipline |

## Trigger probes
- Positive: PASS — P4 "write a script to rename photos by EXIF date" loaded write-code (hands-on file-manipulation/coding).
- Negative: PASS — N4 "caching opinion on current code" did NOT load write-code (analysis/opinion, nothing to build → review-code or none).

## Observations
- **Both trials produced functionally identical deliverables:** `logscan.py` (regex parser, total/status-class/top-3-IP stats, `--json`, `--since`), `access.log` (20 lines, a few 404s/500s), `test_logscan.py` (5 tests). Both ran the tool (plain + JSON + since filter) and showed output; both ran pytest and showed `5 passed`; both curled the server and showed HTTP 200 with the directory listing.
- **R2 (read-before-edit / verify-own-work) is the sole differentiator.** The treatment run, following the skill's "verify before reporting success" and "check your work" guidance, additionally exercised an edge case — running the tool on a nonexistent file and confirming the graceful `error: no such file` to stderr with exit code 1. The baseline stopped at the happy-path `--since` filter and did not probe error handling. Neither trial needed to re-read a file after writing (both were single-pass writes), so the difference is the depth of self-verification, not literal re-reading.
- **Server handling was identical and correct in both.** The shell `&` operator is blocked by the execution policy in this environment ("Command is not allowed by execution policy", exit 126), so both trials backgrounded the server via `subprocess.Popen` with stdout/stderr redirected to a log file, verified with a separate curl command (HTTP 200), then killed it and confirmed down via curl (HTTP 000) and `ps` (no process). No blocking calls in either. This is a genuine environment constraint, not a skill failure — the skill's instruction to background with `&` was followed in spirit (background + redirect + separate verify).
- **Folder discipline was clean in both:** all files confined to `/tmp/logscan-baseline` and `/tmp/logscan-treatment` respectively; no files scattered in home/parent dirs. Both left only `.pytest_cache` behind (expected).
- **No stray processes left:** both trials killed the server and confirmed it was gone before finishing.
- **Verbatim divergence:** baseline's verification set = {plain, json, since}; treatment's = {plain, json, since, missing-file edge case}. That one extra edge-case run is the entire measurable delta.

## Verdict
- **Pass.** Treatment avg (10/10) > baseline avg (9/10).
- The skill's value here is discipline reinforcement, not capability: both trials independently produced a correct, fully-verified tool. The treatment's only edge is that it probed an error path (missing file) that the baseline skipped, driven by the skill's explicit "verify before reporting success / check your work" rules. On this fixture the skill nudges a competent baseline from "verified happy path" to "verified happy path + edge case," which is a real but modest increment.

## Refinements
- [ ] The skill's verify-before-success guidance is effective but could be more prescriptive about *what* to verify: suggest "run the tool on the sample input AND at least one error/edge input (missing file, malformed line, empty filter result)" so the discipline reliably covers failure paths, not just the happy path.
- [ ] (Optional) Note in the skill that if the shell `&` operator is blocked by an execution policy, backgrounding via `subprocess.Popen` (with output redirected) is an acceptable equivalent — the environment here blocks `&`, so the skill's literal example can't always be followed verbatim.