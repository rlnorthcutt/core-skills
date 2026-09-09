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
| Skill | Purpose |
|---|---|
| `review-code` | Correctness-focused review of code changes |
| `review-security` | Security-focused review of code changes |
| `simplify-code` | Quality cleanup of changed code (not bug-hunting) |
| `write-draft` | Complete short-form drafts: emails, messages, posts, bios |
| `humanize-text` | Strip AI-sounding patterns from writing |
| `resolve-recipient` | Verify the right people before person-directed actions |
| `personal-context` | Pull relevant memory/continuity before acting |

### Wave 2 — platform meta-skills
| Skill | Purpose |
|---|---|
| `improve` | Review the conversation, then create the fix (skill/tool/app/profile) |
| `create-skill` | Create, validate, and install new skills |
| `create-agent` | Design and register agent profiles |
| `create-tool` | Design and register reusable custom tools |
| `create-app` | Build Omnideck Custom Apps |
| `write-docs` | Write and maintain documentation |

### Later waves
`research`, `plan-learning`, `generate-image`, `visualize`, `visualize-data`,
`edit-spreadsheet`, `edit-document`, `edit-presentation`, `edit-pdf`, `install-skill`,
`design`, and the artifact family.

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
