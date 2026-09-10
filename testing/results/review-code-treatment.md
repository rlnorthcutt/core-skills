# Code Review — inventory-service (treatment: review-code skill)

**Scope:** diff of `service.py` adding `bulk_restock`, `fulfill_by_skus`, `average_stock`, and the pre-existing `fulfill` they call. I traced each finding through its callers/callees and the `Item`/`Order` dataclasses before reporting. 8 tests pass on both commits; the defects below are latent and not covered by tests.

## Findings (severity-ranked)

### Important — `average_stock`: docstring/behavior mismatch AND unhandled ZeroDivisionError
`service.py:83-86`
```python
def average_stock(self) -> float:
    """Average quantity across all items (items with zero stock excluded)."""
    quantities = [item.quantity for item in self.items.values() if item.quantity is not None]
    return sum(quantities) / len(quantities)
```
Two defects:
1. **Contract mismatch.** The docstring promises "items with zero stock excluded", but the filter is `item.quantity is not None`. `Item.quantity` defaults to `0` (`models.py:11`) and is never `None` in practice, so the filter keeps zero-quantity items. The documented average and the computed average disagree whenever any item has zero stock.
2. **ZeroDivisionError.** If the service is empty, or all items have `quantity is None`, `quantities` is `[]` and `sum([]) / 0` raises `ZeroDivisionError`. Concrete failure: a fresh `InventoryService()` with no `add_item` calls, or one where every item was added with `quantity=0` (which is allowed — `add_item` does not reject 0), crashes the call. In a web context this surfaces as an unhandled 500.

**Fix:** filter `item.quantity > 0` to match the docstring, and guard `if not quantities: return 0.0` (or raise a clear error) before dividing.

### Important — `fulfill_by_skus`: empty order recorded as "fulfilled" with zero validation
`service.py:77-80`
```python
if len(skus) == 0:
    order.status = "fulfilled"
    self.orders.append(order)
    return True
```
Traced path: with `skus == []`, the loop at line 75 never runs, `order.items` stays `{}`, and the branch bypasses `fulfill()` entirely — no availability check, no `get_item`, no decrement. The order is appended to `self.orders` as `fulfilled`. This is inconsistent with `fulfill()`'s contract (`service.py:33-47`), which validates availability before ever marking anything fulfilled. Concrete failure: a caller that passes an empty list (e.g. an upstream selection that filtered everything out) silently records a phantom fulfilled order and returns `True`, so downstream reporting counts an order that shipped nothing. **Fix:** reject empty `skus` (raise `ValueError`) or route through the normal path so an empty order is not recorded as fulfilled.

### Minor — `bulk_restock`: index-based dict iteration rebuilds the key list every pass (O(n²))
`service.py:65-66`
```python
for i in range(len(list(restocks.keys()))):
    sku = list(restocks.keys())[i]
```
Traced: this reinvents `for sku, amount in restocks.items()`. Each iteration re-materializes `list(restocks.keys())`, so the loop is O(n²) in the number of keys — wasteful for large restock batches. It also depends on dict insertion order and would break if `restocks` were mutated mid-loop. It is functionally correct on CPython today (the tests pass), so this is a latent fragility rather than an active bug. **Fix:** `for sku, amount in restocks.items():` and drop the index.

## Trap check — `fulfill()` two-loop structure (NOT a bug)
`service.py:36-44` checks availability in one loop, then decrements in a second. I considered flagging this as a TOCTOU race, but this is a single-threaded, in-memory service with no concurrency — there is no interleaving window. The two-loop structure is exactly what makes "all-or-nothing" fulfillment work (nothing is decremented unless every item is available). Not a defect.

## What's good
- `restock()` correctly validates `amount <= 0` (`service.py:27`), so `bulk_restock` cannot drive stock negative through that path.
- `fulfill()` correctly sets `status = "blocked"` and returns `False` without mutating stock on insufficient availability — the all-or-nothing invariant is sound.
- The new methods are short and readable; the issues are edge-case and contract problems, not structural ones.

## Verdict
Not safe to merge as-is. The two Important findings are real latent defects: `average_stock` will crash on an empty/all-zero service and misreports the documented average, and `fulfill_by_skus` records phantom fulfilled orders for empty input. The `bulk_restock` O(n²) pattern is Minor and worth fixing while here. The `fulfill()` two-loop structure is correct and should not be "simplified." Fix findings 2 and 3 (and ideally 1) before merge; the existing tests do not cover these paths, so add regression tests for empty/all-zero inputs.