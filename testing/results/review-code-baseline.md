# Code Review — inventory-service (baseline, no skill)

**Scope:** `service.py` — new methods `bulk_restock`, `fulfill_by_skus`, `average_stock`, plus the pre-existing `fulfill` they interact with.

## Findings

### 1. `bulk_restock` — index-based dict iteration rebuilds the key list every pass (Minor)
`service.py:65-66`
```python
for i in range(len(list(restocks.keys()))):
    sku = list(restocks.keys())[i]
```
This reinvents `for sku, amount in restocks.items()`. It rebuilds `list(restocks.keys())` on **every iteration**, making it O(n²) in the number of keys. It also depends on dict insertion order and would break if the dict were mutated mid-loop. It happens to be correct on CPython today, but it's a fragile pattern with no benefit. **Recommendation:** replace with `for sku, amount in restocks.items():` and drop the index.

### 2. `fulfill_by_skus` — empty order is recorded as "fulfilled" with no validation (Important)
`service.py:77-80`
```python
if len(skus) == 0:
    order.status = "fulfilled"
    self.orders.append(order)
    return True
```
When the caller passes an empty `skus` list, this creates an `Order` with `items={}`, marks it `fulfilled`, appends it to `self.orders`, and returns `True` — completely bypassing the availability checks that `fulfill()` performs. This is inconsistent with the `fulfill()` contract: a caller that passes an empty list (e.g. from a buggy or empty upstream selection) silently gets a phantom fulfilled order recorded instead of an error or a blocked status. **Recommendation:** reject empty `skus` (raise `ValueError`) or route through the normal path so an empty order is not recorded as fulfilled.

### 3. `average_stock` — docstring/behavior mismatch and division-by-zero (Important)
`service.py:83-86`
```python
def average_stock(self) -> float:
    """Average quantity across all items (items with zero stock excluded)."""
    quantities = [item.quantity for item in self.items.values() if item.quantity is not None]
    return sum(quantities) / len(quantities)
```
Two problems:
- The docstring says "items with zero stock excluded", but the filter is `item.quantity is not None`, which keeps zero-quantity items. So the documented contract and the actual behavior disagree.
- If the service is empty, or every item's quantity is `None`, `quantities` is empty and `sum([]) / 0` raises `ZeroDivisionError`. There is no guard for the empty case.

**Recommendation:** filter on `item.quantity > 0` to match the docstring, and guard the empty/`len(quantities) == 0` case (return `0.0` or raise a clear error).

## Non-issues / notes
- `fulfill()` uses two loops — one to check availability, one to decrement. This is intentional "all-or-nothing" fulfillment and is fine in this single-threaded, in-memory service; it is not a race condition here.
- `restock()` correctly validates `amount <= 0`, so `bulk_restock` cannot drive stock negative through that path.

## Verdict
The change is small and mostly readable, and the existing tests pass. However, all three new methods carry latent defects that tests don't cover: the O(n²) index pattern in `bulk_restock`, the phantom-fulfilled-order path in `fulfill_by_skus`, and the docstring mismatch plus unhandled `ZeroDivisionError` in `average_stock`. The `average_stock` and `fulfill_by_skus` issues are the most likely to bite in production. I'd request changes before merge, primarily for findings 2 and 3.