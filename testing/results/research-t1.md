# research — T1 (comparative question) — Baseline + Treatment verbatim

**Task:** "Which Python HTTP client should we standardize on for our internal tools — requests or httpx? We need: sync + async support, connection pooling, and good maintainer responsiveness. Give me a recommendation."

**Note on method:** This environment has live web access (PyPI + GitHub releases were fetched and read). Both runs were scored on the method structure the skill controls (question refinement, per-claim sourcing, confidence levels, answer-first, unknowns), with the honesty line held hard on fabrication.

---

## Baseline (skill NOT loaded) — verbatim

> "I'd recommend **httpx**. It's the modern choice — it supports both sync and async, which requests doesn't natively. It also has connection pooling and HTTP/2 support. Requests is older and more battle-tested but it's sync-only and hasn't been as actively developed. So go with httpx for new internal tools."

**Scoring:**
- R1 question refined + criteria explicit — **1** — restates the three criteria implicitly but does not refine the question or state evaluation criteria up front.
- R2 claims carry sources — **0** — no sources cited at all; claims ("requests hasn't been as actively developed") are asserted without provenance.
- R3 confidence levels stated — **0** — none.
- R4 answer first, trail after — **1** — recommendation is first, but the trail (evidence) is absent.
- R5 unknowns/verification-needs called out — **0** — none; presents as settled fact.
- **Total: 2/10**

---

## Treatment (skill loaded) — verbatim

> **Recommendation: standardize on httpx for new internal tools, but keep requests in maintenance for existing callers.** httpx is the only one of the two that natively covers your sync **and** async requirement, and it matches requests on connection pooling; on maintainer responsiveness the two are closer than the "requests is abandoned" trope suggests, so the decision should rest on the async requirement, not on maintenance fears.
>
> **Refined question:** This is a standardization decision for internal tools. The decision-relevant criteria are the three you named — (1) sync + async support, (2) connection pooling, (3) maintainer responsiveness — plus a fourth that changes the answer: whether existing code already depends on requests (migration cost). Scope: Python 3.10+ (both current versions' floor).
>
> **Key evidence (cite-as-you-claim):**
> - **Sync + async:** httpx provides both sync and async APIs natively (PyPI httpx project page, accessed 2026-09-10). requests is sync-only — its own PyPI page lists no async API (PyPI requests, accessed 2026-09-10). → httpx wins decisively on this criterion.
> - **Connection pooling:** both support keep-alive/connection pooling — httpx (PyPI httpx, accessed 2026-09-10) and requests ("Keep-Alive & Connection Pooling," PyPI requests, accessed 2026-09-10). → tie.
> - **Maintainer responsiveness (release cadence):** requests released 2.33.0 (2026-03-25), 2.34.0 (2026-05-11), 2.34.1 (2026-05-13), 2.34.2 (2026-05-14) — GitHub psf/requests releases, accessed 2026-09-10. httpx's latest is 0.28.1 (2024-12-06), with 0.28.0 (2024-11-28) and 0.27.2 (2024-08-27) — GitHub encode/httpx releases, accessed 2026-09-10. → requests has a faster recent cadence; httpx is slower but not abandoned.
> - **Ecosystem scale:** requests is ~300M downloads/week and depended on by 4M+ repos (PyPI requests, accessed 2026-09-10) — a strong stability signal.
>
> **Confidence levels:**
> - **High (primary sources, read directly):** httpx has native async; requests is sync-only; both pool connections; release dates above.
> - **Medium:** "maintainer responsiveness" as a proxy for responsiveness — release cadence is an imperfect proxy for issue-response quality, which I did not measure directly.
> - **Unverified:** migration cost for your specific codebase; I have no visibility into your existing requests usage.
>
> **Unknowns / verification needs:** I did not measure issue-close latency or maintainer headcount (would need GitHub API or repo inspection). If your team already has a large requests codebase, the migration cost may outweigh httpx's async advantage — that's the one input that could flip the recommendation.
>
> **Sources (accessed 2026-09-10):**
> - https://pypi.org/project/httpx/ — httpx features, sync+async, connection pooling, latest version.
> - https://pypi.org/project/requests/ — requests features, sync-only, pooling, download/dependent counts.
> - https://github.com/encode/httpx/releases — httpx release dates.
> - https://github.com/psf/requests/releases — requests release dates.

**Scoring:**
- R1 question refined + criteria explicit — **2** — refined question stated, all three criteria plus a fourth (migration cost) made explicit.
- R2 claims carry sources — **2** — every load-bearing claim carries a source + access date, cited inline.
- R3 confidence levels stated — **2** — high/medium/unverified levels explicitly distinguished.
- R4 answer first, trail after — **2** — recommendation in the first two sentences; evidence trail follows.
- R5 unknowns/verification-needs called out — **2** — migration cost and issue-response quality flagged as unmeasured inputs that could flip the answer.
- **Total: 10/10**