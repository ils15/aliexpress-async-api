"""Product-related models"""
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict


@dataclass
class Product:
    """AliExpress affiliate product"""
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
class ProductSearchResponse:
    """Response from product search/query endpoints"""
    products: List[Product]
    total_record_count: int
    current_record_count: int
    page_no: int
    raw_data: Dict[str, Any] = field(default_factory=dict)
