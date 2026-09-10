"""Tests for the inventory service."""
from datetime import datetime, timedelta
from models import Item, Order
from service import InventoryService


def make_service() -> InventoryService:
    svc = InventoryService()
    svc.add_item("SKU-1", "Widget", quantity=100, reorder_point=20)
    svc.add_item("SKU-2", "Gadget", quantity=5, reorder_point=10)
    svc.add_item("SKU-3", "Doohickey", quantity=50, reorder_point=10)
    return svc


def test_add_and_get():
    svc = make_service()
    assert svc.get_item("SKU-1").name == "Widget"


def test_restock():
    svc = make_service()
    svc.restock("SKU-2", 30)
    assert svc.get_item("SKU-2").quantity == 35


def test_fulfill_success():
    svc = make_service()
    order = Order(order_id="O-1", items={"SKU-1": 10})
    assert svc.fulfill(order) is True
    assert svc.get_item("SKU-1").quantity == 90
    assert order.status == "fulfilled"


def test_fulfill_blocked():
    svc = make_service()
    order = Order(order_id="O-2", items={"SKU-2": 100})
    assert svc.fulfill(order) is False
    assert order.status == "blocked"


def test_low_stock():
    svc = make_service()
    low = svc.low_stock_report()
    assert [i.sku for i in low] == ["SKU-2"]


def test_bulk_restock():
    svc = make_service()
    svc.bulk_restock({"SKU-2": 30, "SKU-3": 10})
    assert svc.get_item("SKU-2").quantity == 35
    assert svc.get_item("SKU-3").quantity == 60


def test_fulfill_by_skus():
    svc = make_service()
    assert svc.fulfill_by_skus(["SKU-1"], "O-3") is True
    assert svc.get_item("SKU-1").quantity == 99


def test_average_stock():
    svc = make_service()
    assert svc.average_stock() == (100 + 5 + 50) / 3
