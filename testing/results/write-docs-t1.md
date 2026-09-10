# inventory-service

In-memory inventory service for a warehouse: track stock per SKU, restock, and fulfill orders. Pure Python, no external dependencies, no persistence — state lives in the `InventoryService` instance and is lost on process exit.

## Requirements

- **Python 3.9+** — the code uses built-in generic type hints (`dict[str, Item]`, `list[Order]`) which require 3.9+. Verified on Python 3.12.13.
- No third-party packages. There is no `requirements.txt`; nothing to install.

## Quickstart

```python
from models import Item, Order
from service import InventoryService

svc = InventoryService()
svc.add_item("SKU-1", "Widget", quantity=100, reorder_point=20)
svc.add_item("SKU-2", "Gadget", quantity=5, reorder_point=10)

# Fulfill an order for 10 Widgets
order = Order(order_id="O-1", items={"SKU-1": 10})
svc.fulfill(order)          # -> True
order.status                # -> "fulfilled"
svc.get_item("SKU-1").quantity  # -> 90

# Which items are at or below their reorder point?
[i.sku for i in svc.low_stock_report()]  # -> ["SKU-2"]
```

## Running the tests

```bash
cd inventory-service
python -m pytest -q
# 8 passed
```

## API

### `InventoryService`

| Method | Behavior (verified) |
|---|---|
| `add_item(sku, name, quantity=0, reorder_point=10) -> Item` | Adds an item. Raises `ValueError("Item already exists: <sku>")` if the SKU is already present. |
| `get_item(sku) -> Item` | Returns the item. Raises `KeyError` if the SKU is unknown. |
| `restock(sku, amount) -> Item` | Adds `amount` to the item's quantity and sets `last_restocked` to now. Raises `ValueError("Restock amount must be positive")` if `amount <= 0`. |
| `fulfill(order) -> bool` | **All-or-nothing.** First checks every line item has enough stock; if any is short it sets `order.status = "blocked"` and returns `False` **without decrementing any stock**. If all lines are available it decrements all quantities, sets `status = "fulfilled"`, appends the order, and returns `True`. |
| `low_stock_report() -> list[Item]` | Items with `quantity <= reorder_point` (in insertion order). |
| `stale_items(days=30) -> list[Item]` | Items whose `last_restocked` is older than `days` days. Items never restocked (`last_restocked is None`) are excluded. |
| `bulk_restock(restocks: dict[str, int]) -> dict[str, Item]` | Calls `restock` for each SKU. Returns `{sku: updated_item}`. |
| `fulfill_by_skus(skus, order_id) -> bool` | Fulfills an order taking exactly 1 of each listed SKU. An empty list is treated as fulfilled. |
| `average_stock() -> float` | Mean quantity across all items. Raises `ZeroDivisionError` on an empty service. |

### Data models (`models.py`)

- **`Item`** — `sku`, `name`, `quantity=0`, `reorder_point=10`, `last_restocked=None`, `tags=[]`. `is_low_stock()` returns `quantity <= reorder_point`.
- **`Order`** — `order_id`, `items` (dict of `sku -> qty`), `created` (defaults to now), `status="pending"`.

## Error cases

| You do | Result |
|---|---|
| `restock(sku, 0)` or negative | `ValueError: Restock amount must be positive` |
| `add_item` with an existing SKU | `ValueError: Item already exists: <sku>` |
| `get_item` with an unknown SKU | `KeyError` |
| `fulfill` when any line is short | returns `False`, `order.status == "blocked"`, **no stock changed** |
| `average_stock()` on an empty service | `ZeroDivisionError` |

## Layout

- `models.py` — `Item`, `Order` dataclasses.
- `service.py` — `InventoryService` business logic.
- `test_service.py` — 8 tests covering add/get, restock, fulfill (success + blocked), low stock, bulk restock, fulfill-by-skus, average stock.

## Notes

- State is in-memory only; there is no database or persistence layer.
- `bulk_restock` is not atomic: if one SKU in the batch is invalid, earlier restocks in the same call are kept.