# make-docs — Test Results (2026-09-10)

## Trials
| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1 create | 6/10 | 10/10 | Baseline used manual bold formatting (4 manual-bold Normal paragraphs, no Heading styles, no caption). Treatment used Heading 1/2, real styled table with caption, front-loaded purpose. |
| 2 | T2 edit | 6/10 | 10/10 | Baseline appended appendix as manual bold paragraph (no style preservation, outline flattened). Treatment added Heading 2 at correct level after Recommendations, preserved all existing sections untouched. |
| 3 | T3 verify |—/10 | 10/10 | Verify run only on treatment output (per protocol). Render caught heading-hierarchy defect (H1/H2 same size); fixed via style sizing, re-rendered clean. |

## Trigger probes
- Positive: "I need a Word document/report for..." → should suggest make-docs: **pass**
- Negative: "review my code changes for bugs" → should NOT be make-docs/make-slides: **pass** (routes to review-code)

## Observations
- Baseline T1: title and section headers all manual-bold Normal paragraphs — no Heading 1/2 styles, no outline, no caption style on table. Purpose paragraph present but not front-loaded as a conclusion.

- Treatment T1: Heading 1 title + Heading 2 sections, styled table ("Light Grid Accent 1") with Caption-style "Bug Summary", front-loaded purpose paragraph stating conclusion up front. Zero manual-bold Normal paragraphs.

- Render-verify (T3) caught a real defect: Heading 1 and Heading 2 rendered at identical size/weight, so the title was not visually distinguished. Fixed by setting Heading 2 to 16pt and a distinct blue; re-render confirmed clear hierarchy, table intact, no overflow.

- Treatment T2: appendix added as Heading  ​2 after Recommendations, matching sibling level; existing sections untouched (no restyling). Baseline T2 added appendix as manual bold paragraph, flattening the outline.

- Reopen verification (R5): all four docx files open cleanly; treatment files show proper Heading 1/2 structure and 0 manual-bold paragraphs; baseline files show 4-5 manual-bold Normal paragraphs and no heading styles.



## Verdict
- **Pass**. Treatment avg: 10/10 vs baseline avg: 6/10. The skill's outline-first, style-based, render-verify loop produced structurally correct, visually verified documents; baseline relied on manual formatting with no hierarchy or verification.



## Refinements
- [ ] None required — skill performed as designed. (Optional: skill could add an explicit "verify heading visual distinction" checklist item, as the render loop caught the H1/H2 same-size issue that a pure style-application pass would miss.)