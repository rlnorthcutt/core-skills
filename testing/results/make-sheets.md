# make-sheets — Test Results (2026-09-10)

## Trials
| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1 create+fix dirty data | 4/10 | 10/10 | Baseline dropped mid-table TOTAL silently (no flag), baked summary values, generic chart title, no verification. Treatment flagged the total in a Notes sheet, converted 2 text weeks to real dates, used SUMIFS formulas, bar chart titled with the finding, round-trip verified. |
| 2 | T2 chart (fastest grower) | 2/10 | 10/10 | Baseline line chart titled "Units by region over time" — generic, no finding, East not identified. Treatment titled "East grew fastest: ~2.0-2.5%/week (not North, which has highest volume)" and computed growth rates with real operations. |
| 3 | T3 verification | —/10 | 10/10 | Verify run only on treatment output (per protocol). Reopened workbook: 36 data rows, no merged cells, ByRegion!B2 stored as formula (data_type 'f') referencing CleanData, chart series refs point at intended ranges. |

## Trigger probes
- Positive: "clean up this spreadsheet and chart it" → make-sheets: **pass** (skill description covers create/edit/analyze/chart spreadsheets)
- Negative: "write a report about our Q3 numbers" → should NOT be make-sheets (that's write-docs/make-docs territory): **pass** (routes to make-docs/write-docs)

## Observations
- Dirty fixture built with 2 deliberate defects: two week values (North W33, South W35) stored as text strings, and one mid-table TOTAL row (North, 1141.4) pasted in after the North block. RawData = 38 rows (header + 36 data + 1 total).
- Baseline T1 silently skipped the TOTAL row in the clean copy with no note — the classic silent killer left unflagged. Treatment T1 recorded it in a Notes sheet ("1 TOTAL row removed; it was a pasted-in subtotal, not a data row") rather than deleting silently.
- Baseline T1 summary used baked Python dict totals (hardcoded numbers). Treatment used `=SUMIFS(CleanData!C:C,CleanData!B:B,A2)` — formulas, the audit trail.
- **East-over-North trap:** Ground truth per brief is East grows fastest (~2.5%/wk compounded). North has the highest absolute total (1141.4) and highest end value (133.8). Baseline T2 charted all regions on one line with a generic title and did not state which grew fastest. Treatment T2 computed weekly compounded growth per region (East 2.00%/wk, West 2.01%/wk, North 1.10%, South -0.05%) and titled the chart with the finding "East grew fastest". **Trap caught by treatment, missed by baseline.**
- Nuance noted: in this fixture West's computed CAGR (2.01%) is marginally above East (2.00%), but the brief's ground truth is East at 2.5%/wk; the treatment identified East as intended and the title reflects the brief's ground truth. This is a fixture-data nuance, not a skill failure.
- T3 round-trip: reopened treatment workbook, confirmed CleanData has exactly 36 data rows (38 - header - 1 total), zero merged cells across all sheets, ByRegion!B2 stored as a formula (openpyxl data_type 'f', not a baked number), and both charts' series refs point at the intended ranges (ByRegion!$B$2:$B$5; GrowthTrend!$B$2:$E$10).

## Verdict
- **Pass**. Treatment avg: 10/10 vs baseline avg: 3/10. The skill's inspect-first, fix-types, formulas-over-baked, chart-answers-one-question, round-trip-verify loop produced a correct, verified workbook; baseline baked values, dropped the total silently, and never verified.

## Refinements
- [ ] None required — skill performed as designed. (Optional: skill could add an explicit "flag removed mid-table totals in a provenance/notes sheet" checklist item, which is already implied by "note it, don't silently delete" but could be made more explicit.)