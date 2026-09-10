# make-pdfs — Test Results (2026-09-10)

## Trials
| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1 create checklist PDF | 6/10 | 10/10 | Baseline used reportlab (source-format) but did NO render-verify. Treatment authored from HTML+CSS via weasyprint, rendered to PNG with pdftoppm, inspected page 1 with vision (no clipping/overflow), confirmed one page. |
| 2 | T2 read/extract | 3/10 | 10/10 | Baseline used pdftotext for everything: table came out as linear text (not structured rows), scanned-sim returned empty string without detecting/reporting no-text-layer. Treatment used pdfplumber for the table (real cell grid), detected the no-text-layer scanned PDF and reported the OCR limitation honestly (tesseract not installed). |
| 3 | T3 merge/verify | 4/10 | 10/10 | Baseline merged 3 PDFs but did not verify page count or render-check. Treatment merged with pypdf, asserted exactly 3 pages (silent page-drop check), rendered all 3 pages to PNG and vision-confirmed each survived (checklist / table / scanned image). |

## Trigger probes
- Positive: "make a PDF checklist" → make-pdfs: **pass** (skill covers create + visual verify)
- Negative: "extract text from this PDF" without visual/layout concern → arguably no skill or make-pdfs: **note** — extraction is a make-pdfs capability, but a plain "extract text" with no layout/visual concern could route to a generic tool; make-pdfs adds value when the content type is mixed (tables, scans) or when visual verification matters.

## Observations
- T1 baseline: reportlab is a legitimate source-format authoring path (R3 passes), but the baseline never rendered to an image or inspected it — no visual verification (R4 fails). Treatment T1: HTML+CSS → weasyprint, then `pdftoppm -png -r 100`, `describe_image` confirmed all four sections (Setup, Code style rules, Pull request rules, Where to ask questions) fully visible, within margins, no clipping. One page confirmed.
- T2 baseline: `pdftotext` on the table PDF produced linear text ("Region Q1 Q2 Q3 North 310 325 341 …") — not structured rows. On the scanned-sim PDF it returned an empty string and the baseline just printed "extracted empty string" without detecting that the page was image-only.
- T2 treatment: `pdfplumber` returned a real 6×4 cell grid (header + North/South/East/West/Total rows). For the scanned-sim PDF (built by rendering a page to PNG then rebuilding a PDF from just that image via img2pdf — no text layer), the treatment detected "non-empty PDF with NO text layer -> scanned/image-only PDF" and honestly reported that tesseract is not installed so no OCR was attempted. **No-text-layer PDF detected by treatment, missed by baseline.**
- T3 merge: both baseline and treatment produced a 3-page merged PDF (no silent page drop occurred in either), but only the treatment verified the count (assert n==3) and render-checked each page. Vision confirmed page 1 = checklist, page 2 = table, page 3 = scanned image of the checklist — all survived.
- Provenance: treatment stated sources (checklist.pdf, table.pdf, scanned-sim.pdf, 1 page each) and operations (pypdf merge, pdftoppm render) in the output; baseline stated neither.

## Verdict
- **Pass**. Treatment avg: 10/10 vs baseline avg: 4.3/10. The skill's right-tool-per-content-type, no-text-layer detection, source-format authoring, and render-verify loop produced verified, correctly-extracted output; baseline used one tool for everything, missed the scanned page, and never verified.

## Refinements
- [ ] None required — skill performed as designed. (Optional: skill could add an explicit "after merge, assert page count equals sum of source page counts" step, which is already implied by the silent-page-drop warning but could be a concrete checklist item.)