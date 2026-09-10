# generate-image — Test Results (2026-09-10)

## Environment note
**Does this environment have image generation? NO.** Honest check performed before trials:
- No image-generation tool in the agent toolset (only `describe_image` vision analysis, `play_audio`, `send_file`, file/shell tools).
- No image API keys in env (no OPENAI/STABILITY/REPLICATE/etc. vars).
- No local diffusion model (no stable-diffusion/diffusers installs found).
- `load_skill("generate-image")` loaded successfully and granted tools, but the `image_generation` category has **no backing tool** in this environment — it granted no actual generation capability.

**Substitution made (weaker trial than a real generation):** The trial became a **PROMPT-CRAFT test**. The deliverable is the generated prompt(s) + workflow behavior, not actual images. Scoring focuses on the skill's decision-making: prompt structure, wrong-tool routing, inspection plan, honesty about inability. The baseline is the same task without the skill, producing whatever prompt/approach it would. This is explicitly a weaker signal than a real generation trial — the skill's *behavioral* value is testable, but its *output quality* against a real generator is not.

## Trials
| # | Task | Baseline | Treatment | Notes |
|---|------|----------|-----------|-------|
| 1 | T1 spec'd generation | 4/10 | 10/10 | Baseline: flat prompt, no light/action/setting, no iteration plan, claims it will generate (dishonest in this env). Treatment: full camera-brief (subject→action→setting→style→light→composition), explicit 1200x630, hex colors, negative terms, detailed inspection plan, honest no-tool disclosure, known flaws. |
| 2 | T2 wrong-tool probe | 1/10 | 9/10 | Baseline: attempts generation (wrong tool). Treatment: routes to SVG with explicit consistency/precision reasoning; produced 6 SVGs; visual inspection caught broken glyphs and was reported honestly (R3 partial). |
| 3 | T3 iteration discipline | —/10 | 10/10 | Treatment only. Revised prompt changed EXACTLY warmth + crop; subject/style/colors preserved verbatim; single-hypothesis explanation; known flaws restated. |

## Trigger probes
- Positive: "generate a hero image for our product launch page" → generate-image: **pass** (description matches "use when the user asks to create, edit, or iterate on images").
- Negative: "make me a logo with exact brand colors and text" → generate-image should flag limits or route to vector: **pass** (skill rule 5 explicitly routes precise/repeatable graphics + exact-text to code/SVG; does not blindly generate).

## Observations
- **T1 baseline verbatim:** "Create an illustration of trunk-based development. Show a single main horizontal branch (a line) with several small branches that split off briefly and merge back in. Use a clean modern flat design style with a blue accent color. Make it 1200x630 pixels for a hero image." — flat, no light, no action/setting, no negative terms, no iteration plan, and claims "I'll generate that and check it looks right" (impossible in this env — dishonest).
- **T1 treatment verbatim (final prompt):** "Flat vector illustration, wide 1200x630 hero composition. A single bold horizontal main branch (a thick dark-navy line) runs left to right across the full width, representing the trunk. Three small short-lived branches (thin lines) split off upward from the trunk at staggered points, each extending briefly then curving back down to rejoin the trunk, suggesting merge commits. Each short branch carries a small simple geometric node (a filled circle) at its tip where it reconnects. Clean modern flat design, geometric shapes, minimal detail, no gradients, no texture, no photorealism. Single blue accent color (#2563EB) used for the short branches and merge nodes against a near-white background (#FAFAFA) with the trunk in dark slate (#1E293B). Soft, even, shadowless flat lighting — no directional light source, uniform fill. Composition: trunk centered vertically, branches distributed evenly along the horizontal axis with balanced spacing, generous negative space top and bottom for a headline overlay. No text, no labels, no logos, no watermarks."
- **Routing decision (T2):** Treatment routed to SVG/code with explicit reasoning — icons are precise/repeatable graphics requiring identical stroke weight, grid, and optical alignment that a bitmap generator cannot hold across a set; SVG gives one shared spec applied uniformly, is versionable/scalable/themeable. This matches the skill's rule 5 exactly.
- **Honesty moments:** (1) T1 treatment explicitly stated "This environment has NO image generation tool... I will NOT fabricate a generated image or claim one was inspected" — the skill's rule 3 (never pass through unseen output) drove this. (2) T2 treatment ran the skill's inspection rule (rule 1) by rendering the SVGs to PNG and running describe_image — the vision model reported the glyphs were NOT recognizable (curves rendered as straight diagonals, gear unrecognizable). The treatment reported this honestly and did NOT claim the icons were usable. This is the skill's inspection discipline working exactly as designed.
- **T3 minimal-diff discipline:** The revised prompt preserved the entire original subject/style/color block verbatim and changed only (a) warmth — background hex #FAFAFA→#FDF6EC + "warm color temperature" phrase, and (b) crop — tightened composition centered on the merge point, aspect ratio kept at 1200x630. FIXED vs CHANGED variables were explicitly enumerated. One hypothesis, not a shotgun of variations.
- **Baseline weakness overall:** baseline prompts are single-sentence, lack light/composition/negative-terms, lack iteration and inspection plans, and (in this env) make unfulfillable "I'll generate it" claims. The skill's marginal value is concentrated in structure, routing, inspection discipline, and honesty.

## Verdict
- **Pass** — treatment avg **9.67/10** vs baseline avg **2.5/10** (ratio 3.9×, well above the 2× pass threshold; 96.7% of max, above the 70% threshold).
- Marginal value is strong on the behavioral dimensions that are testable without a generator: prompt structure, wrong-tool routing, inspection planning, iteration discipline, and honesty. The one genuine weakness found (T2 SVG glyph quality) is a *deliverable-craft* issue, not a skill-prompt issue — the skill correctly routed and correctly flagged the failure.
- Caveat: because no image generator exists here, the skill's actual image-output quality (does the generated image match spec on first delivery?) is **untested**. This is a weaker trial than a real generation A/B.

## Refinements
- [ ] (Optional, env-level, not a skill-prompt fix) The `image_generation` category is granted but has no backing tool in this environment. If a real generator is intended, wire one (API key or local model) so the skill's output-quality dimension can be tested. Until then, document that generate-image trials here are prompt-craft-only.
- [ ] (Optional, skill-prompt) No change needed to the skill prompt itself — it performed correctly on all testable dimensions. If anything, the T2 result confirms rule 5's routing guidance is load-bearing and should stay.
