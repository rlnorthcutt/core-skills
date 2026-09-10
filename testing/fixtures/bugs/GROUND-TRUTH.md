# Ground Truth — Seeded Bugs

Fixture: `inventory-service/` — the last commit ("Add bulk_restock, fulfill_by_skus, average_stock") contains the seeded bugs. Baseline commit is "Baseline inventory service (pre-change)".

## The diff under review

```bash
cd inventory-service && git diff HEAD~1
```

8 tests pass on both commits — the bugs are latent, not caught by tests. This is deliberate: reviewers must find them by reading, not by running tests.

## review-code — 3 planted bugs

### Bug 1: off-by-one / reimplementation of dict iteration (bulk_restock)
`bulk_restock` iterates with `for i in range(len(list(restocks.keys())))` and re-calls `list(restocks.keys())[i]` inside the loop.
- **Why it's wrong:** reinvents plain `for sku, amount in restocks.items()`; the index pattern is fragile and wasteful (rebuilds the key list every iteration — O(n²)). Functionally correct on CPython today, but it's a latent bug pattern: any dict mutation during iteration or insertion order dependence breaks it.
- **Finding quality bar:** flags the pattern AND the O(n²) rebuild; suggests `.items()`.

### Bug 2: empty-order semantics silently change (fulfill_by_skus)
`fulfill_by_skus` with an empty `skus` list creates an order with `items={}`, marks it fulfilled, and appends it — bypassing the availability checks.
- **Why it's wrong:** inconsistent with `fulfill()`'s contract: an empty order is degenerate but here it's recorded as fulfilled with zero validation. Caller passing an empty list gets a phantom fulfilled order instead of an error or a blocked status.
- **Finding quality bar:** identifies the empty-list branch as a semantic bug (not just "no items" oddness), traces the caller impact.

### Bug 3: division-by-zero + wrong contract (average_stock)
`average_stock` divides by `len(quantities)` where `quantities` excludes `None` quantities but does NOT exclude zero-quantity items — the docstring says "items with zero stock excluded" but the code keeps them. And with an empty service (or all-None quantities), it raises ZeroDivisionError.
- **Why it's wrong (two defects, one line each):**
  1. Docstring/behavior mismatch: zero-stock items are included despite the docstring excluding them.
  2. Unhandled empty case: ZeroDivisionError when there are no items or no valid quantities.
- **Finding quality bar:** catches BOTH the docstring mismatch and the ZeroDivisionError path.

### The trap (must NOT be flagged as a bug)
`fulfill()` checks availability in one loop, then decrements in a second loop. A naive reviewer flags this as a TOCTOU race. In this single-threaded service, it is not — there is no concurrency, and the two-loop structure is what makes "all-or-nothing" fulfillment work. Flagging it as a Critical race without noting the single-threaded context = false positive.

## Scoring anchors (review-code)

| Criterion | 2 (full) | 1 (partial) | 0 (fail) |
|---|---|---|---|
| R1 recall | finds all 3 bugs | finds 2 | ≤1 or flags only the trap |
| R2 precision | trap not flagged as race (or flagged-with-caveat only) | hedges ("possible race in concurrent contexts") | asserts race/Critical |
| R3 severity | bulk_restock pattern=Minor/Important, empty-order=Important, ZeroDivision=Important; nothing Critical | one severity clearly wrong | multiple inflation (trap=Critical etc.) |
| R4 specificity | every finding: file/line + concrete failure scenario | some findings vague | class-naming without scenario |
| R5 form | acknowledges non-bug parts + clear verdict paragraph | verdict only | neither |

## review-security — ground truth for the same diff

The diff is **deliberately benign**: no injection, no secrets, no auth surface. It's a pure logic-layer change on an in-memory service.

- **Expected finding(s):** at most a Low/Hardening note (e.g. `average_stock` ZeroDivisionError causing a 500 in a web context; no rate-limit/DoS concern worth raising here). The correct answer is essentially "no security findings in this diff."
- **What a bad run looks like:** inventing findings — "bulk_restock allows negative stock" (false: restock validates positive), "no input validation on skus" (false: KeyError is the natural handling here), "TOCTOU in fulfill" (out of scope, single-threaded).
- **Scoring anchor:** Precision is the whole test. R1 (recall) is vacuously satisfied — there is nothing to find. A run that produces ≥1 Medium+ invented finding scores 0 on R2 and fails the trial. Saying "nothing exploitable here, here are two hardening notes max" is the full-credit answer.

## simplify-code — ground truth for the same diff

| Seed | Location | Expected simplification |
|---|---|---|
| Reindex-in-loop | `bulk_restock` | `for sku, amount in restocks.items()` — removes the O(n²) key-list rebuild |
| Duplicated dict-building | `fulfill_by_skus` | build `items` dict directly: `items={sku: 1 for sku in skus}` |
| Misnamed dead-check | `average_stock` | the `is not None` filter is dead code (quantity can't be None per the dataclass default) — remove it and guard the empty case explicitly |

- **Trap:** rewriting `fulfill_by_skus` to call `fulfill()` differently, or "simplifying" the two-loop `fulfill` into one loop — that changes behavior (all-or-nothing semantics). Out of scope.
- **Scoring anchor:** R1 = all three seeds found; R2 = tests still pass after edits; R3 = fulfill() untouched.
