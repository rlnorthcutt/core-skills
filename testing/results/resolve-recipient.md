# resolve-recipient — Test Results (2026-09-10)

Fixture: `testing/fixtures/contacts/contacts.json` (6 contacts incl. two Chris Parkers + Chris Park; 3 threads). Ground truth = fixture file. Today = 2026-09-10.

## Trials

| # | Task | Baseline score | Treatment score | Notes |
|---|------|---------------|-----------------|-------|
| 1 | T1 "Send a note to Chris thanking for budget approval" | 2/10 | 10/10 | Baseline picked the Acme Chris (first in address book); treatment resolved Accounting Chris via budget thread |
| 2 | T2 "Email the team about the release going out tomorrow" | 2/10 | 10/10 | Baseline emailed Sam only, no roster; treatment built roster + asked for membership confirmation |
| 3 | T3 "Reply to Chris at Acme about pricing renegotiation" | 4/10 | 10/10 | Baseline OVER-ASKED on a decisive case; treatment proceeded with evidence |

## Trigger probes

- **Positive:** PASS — "Email the team about the release" / "Send a note to Chris" (person-directed, ambiguous reference) loads `resolve-recipient` (description: "Use whenever an action targets a person — especially with first names, duplicate names… or ambiguous references like 'the team'").
- **Negative:** PASS — a request to *compose* a message to an explicitly-named, unambiguous address (e.g. "draft an email to jordan.lee@ourcompany.com") is a drafting task, not a recipient-resolution task; `resolve-recipient` should not load. The skill's trigger is ambiguity/verification, not composition.

## Observations

- **Baseline T1 picked the WRONG Chris (Acme vendor) for an internal budget matter** — the exact mis-send the skill exists to prevent. It chose by "first in the address book / main external Chris" with zero thread evidence. Verbatim: "Sending a quick thank-you note to Chris Parker at Acme Corp… the main external 'Chris' in our address book."
- **Baseline T3 OVER-ASKED on a decisive case** — the skill's explicit failure mode. "Chris at Acme" + "pricing renegotiation" are decisive (pricing thread = Acme Chris), yet baseline asked "Which Chris do you mean?" Verbatim: "There are two Chris Parkers… Which Chris do you mean? Please confirm before I send."
- **Baseline T2 collapsed a group send to a single person** — treated "the team" as Sam Rivera alone, no roster, no membership reasoning, no confirmation. Verbatim: "Sam Rivera is our release manager, so I'll email Sam about the release."
- **Treatment never mis-sends and never over-asks.** Across all three trials it cited per-candidate evidence (thread + role + domain), proceeded without asking exactly when the evidence was decisive (T1, T3), and asked narrowly for roster confirmation exactly when it was a group inference (T2).
- **T2 treatment handled the unenumerable group honestly** — flagged that the "release-team" group's individual membership isn't in the address book and asked the user to confirm the roster rather than guessing members.

## Verdict

- **Pass.** Treatment avg (10/10) vs baseline avg (2.67/10) — treatment ~3.75× baseline, well above the ≥2× pass threshold and ≥70% of max.
- Marginal value: the skill converts a guesser/over-asker into a resolver. Baseline's two failure modes — mis-sending (T1) and over-asking (T3) — are precisely the "never guess" and "don't re-ask what the evidence answered" rules in the prompt. The group-inference case (T2) is where the skill's roster-review rule earns its keep.

## Refinements

- [ ] No refinement required for the core method — all three trials produced the expected marginal value.
- [ ] (Optional) The skill's "When to ask" list could add an explicit note that a group whose membership can't be enumerated should be surfaced as unresolved (as T2 did) rather than silently collapsed to the single most-likely member — this is already implied by rule 3 ("Group sends get roster review") but could be stated as a concrete fallback.