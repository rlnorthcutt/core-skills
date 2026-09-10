# Trigger Probes — Batch 1 (2026-09-09)
Skills probed: review-code, review-security, simplify-code, write-code

| Probe | Request (short) | Probed skill | Loaded? | Correct? | Notes |
|---|---|---|---|---|---|
| P1 | check payment flow before PR | review-code | yes — review-code | pass | "double-check before PR, worried I broke something" = correctness review of a change; prompt matches exactly |
| P2 | security pass on upload endpoint | review-security | yes — review-security | pass | "security pass on the diff" + file-upload endpoint (input handling/external data) = security review; prompt matches |
| P3 | clean up copy-paste code | simplify-code | yes — simplify-code | pass | "works but ugly, lots of copy-paste, clean it up" = cleanup, explicitly not bug-hunting; prompt matches |
| P4 | rename photos by EXIF date | write-code | yes — write-code | pass | "write me a script that renames photos" = hands-on file-manipulation/coding; prompt matches |
| N1 | add --verbose flag (NOT review) | review-code | no | pass | New feature work (add flag + prettier output). Right load: write-code. review-code clearly wrong — no diff/change to review. |
| N2 | off-by-one bug hunt (NOT security) | review-security | no | pass | Bug hunt in known code (sum skips last row). Right load: review-code (correctness bug hunt) or write-code (debug/fix). review-security clearly wrong — no auth/input/secrets/external-data angle. |
| N3 | export crash bug (NOT simplify) | simplify-code | no | pass | Bug fix ("track it down and fix it"), not cleanup. Right load: write-code (hands-on fix) or review-code (diagnose). simplify-code clearly wrong — it's explicitly not bug-hunting. |
| N4 | caching opinion (NOT write-code) | write-code | no | pass | Analysis/opinion ("look at how current code does requests and give your opinion"), no hands-on building. Right load: review-code (arguably) or none. write-code clearly wrong — nothing to build/edit/run. |

## Observations
- **Boundary between review-code and simplify-code is the cleanest.** The catalog descriptions make the split explicit: review-code = "bugs, edge cases, regressions"; simplify-code = "Not bug-hunting — use review-code for that." P3 ("clean it up") and N3 ("track down and fix the bug") both landed correctly with no ambiguity.
- **review-code vs write-code is the fuzziest boundary.** N2 (bug hunt) and N3 (bug fix) both sit between "review the change" (review-code) and "hands-on fix" (write-code). The catalog's write-code description ("Write, edit, run, and debug code") overlaps with review-code's "review a diff/PR/changed code." A request that says "find why it's off by one" could plausibly trigger either. This is the near-miss worth watching.
- **review-security is well-scoped by its trigger phrase.** P2 loaded correctly because the request literally said "security pass" and the endpoint (file uploads) is a trust boundary. N2 correctly did NOT load it because there was no security angle — the catalog's "auth, input handling, secrets, external data" trigger list made the negative decision easy.
- **write-code's "hands-on" trigger is clear for P4 and N4.** P4 ("write me a script") is unambiguous hands-on. N4 ("give your opinion") is unambiguous analysis. The catalog's "Load for any hands-on coding or file-manipulation task" cleanly separates these.
- **No catalog-description gaps surfaced.** Every decision was reachable from the descriptions alone. The only soft spot is the review-code/write-code overlap on bug-hunt-vs-fix requests, which is inherent to the tasks rather than a description defect.

## Summary
- 8/8 correct
