Full content of this skill (~2000 lines) was captured verbatim during export and
written to this directory alongside its two support files:

- `payload.template.html` — the ~2 MiB precompiled Claude Design canvas editor
  payload (never meant to be read/edited directly — only seeded via the helper).
- `seed-canvas.mjs` — the helper script that seeds a fresh copy of the payload
  with design content (`.dc.html` artboards, `canvas.json`, images) and validates it.

See the accompanying `SKILL.full.md` in this same directory for the complete
instructions (workflow, artboard/canvas.json format, `.dc.html` authoring rules,
design craft guidance, known limits, and how to talk to the user about it).
