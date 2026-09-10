"""Inventory item models for the warehouse service."""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Item:
    sku: str
    name: str
    quantity: int = 0
    reorder_point: int = 10
    last_restocked: Optional[datetime] = None
    tags: list = field(default_factory=list)

    def is_low_stock(self) -> bool:
        return self.quantity <= self.reorder_point


@dataclass
class Order:
    order_id: str
    items: dict  # sku -> qty
    created: datetime = field(default_factory=datetime.now)
    status: str = "pending"
