# create-skill — Trial 3 (Duplicate detection)

Task: *"I want a skill that reviews code changes for security issues — injection, auth problems, leaked secrets, that kind of thing."*

---

## BASELINE (create-skill NOT loaded)

**Verbatim agent output:**

> Sure — a security-review skill. Here's one:

```json
{
  "id": "security-reviewer",
  "name": "security-reviewer",
  "description": "Reviews code changes for security issues like injection, auth problems, and leaked secrets.",
  "prompt": "Review the given code changes for security vulnerabilities. Look for SQL injection, authentication and authorization problems, hardcoded secrets, and unsafe dependencies. Report findings with severity and suggested fixes.",
  "tool_categories": ["coding"]
}
```

> I've created `security-reviewer`. It covers injection, auth, and secrets — exactly what you asked for. Drop it in the skills folder and it's ready.

**Analysis of baseline behavior:**
- **Duplicate detection (R4):** Failed — created `security-reviewer`, a near-verbatim duplicate of the existing `review-security` skill (same vulnerability classes: injection, auth, secrets, dependencies; same `coding` category). Never checked the catalog, never reported the overlap, never offered to edit the existing skill. **0.**
- **R1:** `id == name == "security-reviewer"`, valid category — would pass schema, but it's a redundant record.
- **R2:** "Reviews code changes for security issues…" — a real trigger, but it's a duplicate trigger that would shadow `review-security` (both fire on "security review"). Partial.
- **R3:** `coding` only — minimal, but it's a redundant grant of an already-existing capability. Partial.
- **R5:** never validated, never installed, never verified. 0.

---

## TREATMENT (create-skill loaded)

**Verbatim agent output:**

> This already exists. `/var/lib/omnideck/skills/review-security.json` (and the mirror at `/home/omnideck/core-skills/skills/review-security/skill.json`) is exactly this: *"Security-focused review of code changes: injection, auth flaws, secret leakage, unsafe dependencies. Use when the user asks for a security review or the change touches auth, input handling, secrets, or external data."* — same vulnerability classes you listed, same `coding` category.

> Creating `security-reviewer` would be a near-duplicate that splits the trigger ("security review" would match two skills) and dilutes both. Per the craft rules — *prefer editing over accumulating* — I'm not shipping a new one.

> Two options:
> 1. **Edit the existing `review-security`** if it's missing something you need (e.g. you want a secrets-scanning pass over the whole repo, not just the diff — that's a real gap I could add as a section).
> 2. **Defer** — if the existing skill already covers your case, just load `review-security` when you need a security review.

> Which is it — is there a specific gap, or is the existing skill enough?

**Analysis of treatment behavior:**
- **Duplicate detection (R4):** Recognized the exact existing skill, quoted its description, named the collision/dilution failure, and offered the two correct paths (edit existing / defer) — did NOT create a near-duplicate. **2.**
- **R1:** No record shipped (correct); the reasoning is grounded in the actual existing record. **2.**
- **R2:** Explains the trigger-split mechanism precisely. **2.**
- **R3:** No redundant tool grant. **2.**
- **R5:** Nothing installed; live dir integrity preserved. **2.**

---

## Scores

| Criterion | Baseline | Treatment |
|---|---|---|
| R1 record validity | 1 — valid schema but redundant | 2 — no record; grounded in real existing record |
| R2 description trigger | 1 — real trigger but duplicates existing | 2 — explains trigger-split mechanism |
| R3 tool categories | 1 — minimal but redundant grant | 2 — no redundant grant |
| R4 scope discipline | 0 — created the near-duplicate | 2 — detected overlap, offered edit/defer |
| R5 install + verify | 0 — nothing verified | 2 — dirs preserved, no phantom install |
| **Total** | **3/10** | **10/10** |