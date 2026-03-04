from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict

@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str
    expire_time: int
    account: str
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Product:
    product_id: int
    product_title: str
    product_main_image_url: str
    sale_price: str
    original_price: str
    promotion_link: str
    shop_url: Optional[str] = None
    evaluate_rate: Optional[str] = None
    lastest_volume: Optional[int] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AffiliateLink:
    promotion_link: str
    source_value: str
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProductSearchResponse:
    products: List[Product]
    total_record_count: int
    current_record_count: int
    page_no: int
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Category:
    category_id: int
    category_name: str
    parent_category_id: Optional[int] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PromoInfo:
    promo_name: str
    promo_desc: str
    product_num: int
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShippingInfo:
    estimated_delivery_time: str
    freight: str
    tracking_available: str
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SKUInfo:
    sku_id: str
    sku_attr: str
    sku_price: str
    sku_stock: str
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Order:
    order_id: int
    order_status: str
    order_time: str
    estimated_commission: str
    product_title: str
    product_count: int
    product_price: str
    raw_data: Dict[str, Any] = field(default_factory=dict)
