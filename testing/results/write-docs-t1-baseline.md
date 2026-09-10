# Inventory Service

A simple inventory management service for a warehouse.

## Features

- Add items to the inventory
- Restock items
- Fulfill orders
- Generate low-stock reports
- Track stale items
- Bulk restock operations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from service import InventoryService

svc = InventoryService()
svc.add_item("SKU-1", "Widget", quantity=100)
svc.restock("SKU-1", 50)
```

## Testing

```bash
pytest
```

## API

- `add_item(sku, name, quantity, reorder_point)` — add a new item
- `get_item(sku)` — get an item by SKU
- `restock(sku, amount)` — add stock to an item
- `fulfill(order)` — fulfill an order
- `low_stock_report()` — items at or below reorder point
- `stale_items(days)` — items not restocked recently
- `bulk_restock(restocks)` — restock multiple items
- `average_stock()` — average quantity across items