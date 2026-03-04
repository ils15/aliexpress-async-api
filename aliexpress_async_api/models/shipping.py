"""Shipping and SKU models"""
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ShippingInfo:
    """Shipping information for a product"""
    estimated_delivery_time: str
    freight: str
    tracking_available: str
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SKUInfo:
    """Stock Keeping Unit information"""
    sku_id: str
    sku_attr: str
    sku_price: str
    sku_stock: str
    raw_data: Dict[str, Any] = field(default_factory=dict)
