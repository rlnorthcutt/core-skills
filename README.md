# Omnideck Core Skills

A curated collection of production-quality skills for [Omnideck](https://github.com/rlnorthcutt) —
prompt fragments plus tool-category grants that extend what agents can do.

Skills are stored as **SkillRecord JSON** (the format Omnideck's skill system loads from the
state skills directory). Each skill directory contains:

- `skill.json` — the SkillRecord: `id`, `name`, `description`, `prompt`, `tool_categories`
- `SKILL.md` — human-readable documentation: what it does, when it triggers, port notes (optional)

## Installing

```bash
scripts/install.sh <skill-name>          # install one skill
scripts/install.sh --all                 # install every skill in skills/
scripts/validate.py skills/*/skill.json  # validate records before install
```

Skills install into Omnideck's state skills directory and become available to all agents
immediately via the skill catalog (`list_available_skills` / `load_skill`).

## Tool categories

A skill grants tool *categories*, never individual tools. Available categories:

`coding` · `browser` · `webfetch` · `memory` · `planning` · `image_generation` ·
`music_generation` · `desktop` · `email` · `calendar` · `drive` · `contacts` · `http`

Integration-backed categories (email, calendar, drive, contacts, http) only grant tools
when the backing integration is connected.

## The catalog

Skills are grouped by rollout wave — see each skill's SKILL.md for status.

### Wave 1 — prompt-only, ready now

> `write-code` is the verb-first replacement for the shipped `coder` skill (see backlog CR-22).
| Skill | Purpose |
|---|---|
| `review-code` | Correctness-focused review of code changes: bugs, edge cases, regressions, and severity-ranked findings |
| `review-security` | Security-focused review of code changes: injection, auth flaws, secret leakage, unsafe dependencies |
| `simplify-code` | Quality cleanup of changed code: reuse, simplification, efficiency, and altitude |
| `write-code` | Write, edit, run, and debug code in the virtual computer — file editing, shell commands, package installs, long-running processes, git/GitHub |
| `write-drafts` | Compose complete short-form drafts — messages, emails, posts, bios, blurbs — register-matched, purpose-first, with unknowns marked rather than invented |
| `humanize-text` | Remove AI tells and patterns from writing so it reads like a competent human wrote it — kills em-dash spam, 'delve/dive' verbs, rule-of-three lists, hollow intensifiers, and structural tells like perfect parallelism and summary performances |
| `resolve-recipient` | Resolve and verify the correct people before sending messages, email, invitations, or creating calendar events |
| `personal-context` | Detect when prior conversation state, decisions, preferences, or past attempts should change the current answer — and pull the relevant memory before acting |

### Wave 2 — platform meta-skills (Omnideck-optimized creators)
| Skill | Purpose |
|---|---|
| `improve` | Reflect on the current conversation — what worked, what didn't — and turn those lessons into something concrete: a new skill, a custom tool, a change to an existing skill or tool, a custom app, or an agent profile |
| `create-skill` | Create high-quality, well-scoped skills — loadable bundles of a prompt plus tool categories |
| `create-agent` | Create agent profiles — reusable agent configurations bundling a persona (system prompt), skill grants, model, and inference parameters |
| `create-tool` | Create custom tools — parameterized, reusable operations that persist across sessions and are discoverable by all agents |
| `create-app` | Create and manage Omnideck Custom Apps — self-contained apps in the apps directory with a manifest (omnideck.json), a web/ frontend, optional app.py backend actions, and data persistence |

### Wave 3 — writing, docs & learning
| Skill | Purpose |
|---|---|
| `write-docs` | Write and maintain technical documentation — READMEs, how-tos, API references, architecture notes, changelogs |
| `research` | Multi-source research: refine the question, search and read broadly, triangulate across sources, and synthesize findings with provenance and confidence levels |
| `plan-learning` | Build spaced-repetition learning plans: break a topic into a dependency-ordered map, schedule it across available time, produce cards and resources, and set the review cadence |

### Wave 4 — office & media
| Skill | Purpose |
|---|---|
| `make-docs` | Create and edit Word-style documents (.docx) — outline-first structure, style-based formatting, preserved hierarchy on edits, verified output |
| `make-sheets` | Create, edit, analyze, and chart spreadsheets (xlsx, xls, csv, tsv, Google Sheets) — type-safe data models, formula-first authoring, chart-to-question matching, verified output |
| `make-slides` | Create and edit PowerPoint or Google Slides presentations — story-first structure, audience-appropriate design, assertion headlines, speaker notes, verified rendering |
| `make-pdfs` | Read, create, modify, and visually verify PDFs — extraction with the right tool per document type, source-format rendering, image-level verification before delivery |
| `generate-image` | Generate or edit images with deliberate craft — prompt structure, style control, iteration strategy, and when generation is the wrong tool |
| `draw-charts` | Create data visualizations — chart-type selection matched to the question, honest encodings, data hygiene, verified rendering |
| `visualize` | Build interactive diagrams, simulations, graphs, and mockups as self-contained HTML artifacts — parameter controls, live output, single-screen views |

## Sources

The `sources/` directory preserves upstream skill material these were derived from.
Skills in `skills/` are clean, Omnideck-optimized implementations — they contain no
upstream tool names or platform-specific references.

## Contributing a skill

1. Create `skills/<verb-first-name>/skill.json` following the SkillRecord schema
2. Run `scripts/validate.py` on it
3. Name convention: **verb-first kebab-case**, id = name (e.g. `review-code`, `create-skill`)
4. Add a `SKILL.md` describing purpose, triggers, and any port notes
5. Update the catalog tables above
