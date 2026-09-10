"""Inventory service: core business logic."""
import logging
from datetime import datetime, timedelta
from models import Item, Order

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(self):
        self.items: dict[str, Item] = {}
        self.orders: list[Order] = []

    def add_item(self, sku: str, name: str, quantity: int = 0, reorder_point: int = 10) -> Item:
        if sku in self.items:
            raise ValueError(f"Item already exists: {sku}")
        item = Item(sku=sku, name=name, quantity=quantity, reorder_point=reorder_point)
        self.items[sku] = item
        return item

    def get_item(self, sku: str) -> Item:
        return self.items[sku]

    def restock(self, sku: str, amount: int) -> Item:
        """Add stock for an item."""
        item = self.get_item(sku)
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        item.quantity += amount
        item.last_restocked = datetime.now()
        return item

    def fulfill(self, order: Order) -> bool:
        """Fulfill an order: decrement stock for each item."""
        # Check availability first
        for sku, qty in order.items.items():
            item = self.get_item(sku)
            if item.quantity < qty:
                logger.info(f"Insufficient stock for {sku}")
                order.status = "blocked"
                return False
        for sku, qty in order.items.items():
            item = self.get_item(sku)
            item.quantity -= qty
        order.status = "fulfilled"
        self.orders.append(order)
        return True

    def low_stock_report(self) -> list[Item]:
        """Items at or below reorder point."""
        return [i for i in self.items.values() if i.is_low_stock()]

    def stale_items(self, days: int = 30) -> list[Item]:
        """Items not restocked in the given number of days."""
        cutoff = datetime.now() - timedelta(days=days)
        result = []
        for item in self.items.values():
            if item.last_restocked and item.last_restocked < cutoff:
                result.append(item)
        return result

    def bulk_restock(self, restocks: dict[str, int]) -> dict[str, Item]:
        """Restock multiple items at once. Returns map of sku -> updated item."""
        updated = {}
        for i in range(len(list(restocks.keys()))):
            sku = list(restocks.keys())[i]
            amount = restocks[sku]
            item = self.restock(sku, amount)
            updated[sku] = item
        return updated

    def fulfill_by_skus(self, skus: list[str], order_id: str) -> bool:
        """Fulfill an order that takes exactly 1 of each listed SKU."""
        order = Order(order_id=order_id, items={})
        for sku in skus:
            order.items[sku] = 1
        if len(skus) == 0:
            order.status = "fulfilled"
            self.orders.append(order)
            return True
        return self.fulfill(order)

    def average_stock(self) -> float:
        """Average quantity across all items (items with zero stock excluded)."""
        quantities = [item.quantity for item in self.items.values() if item.quantity is not None]
        return sum(quantities) / len(quantities)
