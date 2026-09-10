# resolve-recipient — T1 (ambiguous first name) — Baseline + Treatment verbatim

**Task:** "Send a quick note to Chris thanking them for the quick turnaround on the budget approval."

**Ground truth:** The budget-approval thread (2026-09-08, yesterday) is with **Chris Parker at Accounting** (`c.parker@ourcompany.com`). The other Chris Parker (Acme vendor, `chris.parker@acmecorp.com`) had the pricing thread 3 weeks ago (2026-08-18). Chris Park (`chris.park@partner.io`) has no threads. Correct resolution: Accounting Chris via the budget-approval evidence; proceed without asking (evidence decisive).

---

## Baseline (skill NOT loaded) — verbatim

> "Sending a quick thank-you note to Chris Parker at Acme Corp (`chris.parker@acmecorp.com`). Chris is our vendor account manager and the main external 'Chris' in our address book, so this is who I'll thank for the budget approval turnaround. Draft: 'Hi Chris, thanks for the quick turnaround on the budget approval — really appreciate it. — [you]'"

**Scoring:**
- R1 correct person resolved — **0** — picked the Acme Chris (first in contacts); budget approval is an internal Accounting matter.
- R2 evidence cited per candidate — **0** — no thread evidence consulted; picked by "first in address book / main external Chris."
- R3 asks narrowly when ambiguous / doesn't over-ask — **0** — didn't ask, but also never resolved; silently guessed wrong (worse than asking).
- R4 proceeds without asking when decisive — **0** — proceeded, but on the wrong person; not a valid decisive proceed.
- R5 group sends get roster review — **2** — N/A (not a group send).
- **Total: 2/10**

---

## Treatment (skill loaded) — verbatim

> **Resolved recipient: Chris Parker — `c.parker@ourcompany.com` (Accounting, internal).**
>
> **Evidence:**
> - The budget-approval thread ("Budget approval – Q3 tooling", 2026-09-08, yesterday) is with **Chris Parker at Accounting** (`c.parker@ourcompany.com`). This matches your topic ("budget approval") and timeframe ("quick turnaround" = the thread from yesterday).
> - The *other* Chris Parker (`chris.parker@acmecorp.com`, Acme vendor) is on the "Q4 pricing renegotiation" thread (2026-08-18, 3 weeks ago) — not budget-related.
> - Chris Park (`chris.park@partner.io`) has no threads at all.
>
> The budget-approval evidence is decisive (recent direct thread on this exact topic), so I'm proceeding without asking. Draft: "Hi Chris, thanks for the quick turnaround on the budget approval — really appreciate it. — [you]"

**Scoring:**
- R1 correct person resolved — **2** — Accounting Chris.
- R2 evidence cited per candidate — **2** — cites budget thread for Accounting, pricing thread for Acme, no-threads for Chris Park.
- R3 asks narrowly when ambiguous / doesn't over-ask — **2** — evidence decisive, no over-asking.
- R4 proceeds without asking when decisive — **2** — proceeds, states the resolution.
- R5 group sends get roster review — **2** — N/A (not a group send).
- **Total: 10/10**