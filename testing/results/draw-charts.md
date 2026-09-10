# draw-charts — Test Results (2026-09-10)

## Trials
| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1: Which region grew fastest? | 4/10 | 10/10 | Baseline bar-by-total fell into the eyeball trap (North highest); treatment line chart identified East |
| 2 | T2: Total weekly sales (dirty data) | 4/10 | 10/10 | Baseline charted the raw mess (outlier 99999 dominated W38, missing→0); treatment ran hygiene pass first |
| 3 | T3: Visual verification of T1 chart | 4/10 | 10/10 | Baseline chart readable but wrong answer; treatment verified clean, then fixed a clipped title in T2 |

## Trigger probes
- Positive: "chart the sales data" → draw-charts: **pass** — a data-chart request, matches the skill's trigger language ("chart", "graph", "plot", "visualization of data").
- Negative: "make a static org chart of the team" → draw-charts should NOT fire (that's a diagram, not a data chart; visualize territory): **pass** — correctly routed to visualize/static-diagram territory, not a data chart.

## Observations
- **East-over-North was caught in treatment, missed in baseline.** Ground truth: East grows fastest (~2.3%/wk compounded via log-linear regression); North has the highest absolute volume (122.6→133.8, total 1141.4) — the eyeball trap. Baseline produced a bar chart of *totals* ("Total units sold by region") which visually crowns North (1141.4) and South/East look near-identical (~820). Treatment computed per-region growth rates and used a line chart titled "East grew fastest: +2.3%/wk compounded (North has highest volume, not fastest growth)".
- **Baseline T1 verbatim (the trap):** title "Total units sold by region", bars North=1141.4, South=825.2, East=820.9, West=573.6. Answers "which region has most volume", not "which grew fastest".
- **Treatment T1** used a color-blind-safe Okabe-Ito palette, units on both axes, direct legend with growth rates per region, and a title stating the finding. describe_image confirmed: "No clipped or overlapping labels… title explicitly states a finding… The East region appears to grow the fastest."
- **Baseline T2** charted the dirty CSV directly: missing values coerced to 0.0, the 99999 outlier made Week 38 total 100289.9 (chart scale destroyed). No hygiene, no report.
- **Treatment T2 hygiene pass (verbatim):** "Missing values found: 3 [(5,'2026-W36','North'),(20,'2026-W33','East'),(30,'2026-W34','West')]"; "Duplicate rows found: 2"; "Outliers found: 1 [(25,'2026-W38','East','99999')]". Cleaned to 35 rows, outlier capped to region median (91.8), weekly grain aggregated correctly, and the actions were stated in the title.
- **T3 iteration:** describe_image on the first T2 treatment render caught a **clipped title** ("l weekly sales..." instead of "Total weekly sales..."). Shortened the title to "Total weekly sales, all regions (cleaned)" and re-rendered; re-inspection confirmed "title is fully visible and not clipped." This is the skill's verify→fix→re-verify loop working.
- Environment note: matplotlib was NOT actually pre-installed (installed via pip); plotly absent; no node/JS parser available (visualize T3 uses Python re-extraction for JS validation).

## Verdict
- **Pass**
- Marginal value: treatment avg **10.0** vs baseline avg **4.0** (2.5× baseline; ≥70% of max met)

## Refinements
- [ ] (none required — skill performed to spec; consider a prompt hint that long hygiene-report titles can clip and should be kept short)