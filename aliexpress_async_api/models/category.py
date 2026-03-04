"""Category and promotion models"""
from dataclasses import dataclass, field
from typing import Optional, Any, Dict


@dataclass
class Category:
    """Product category"""
    category_id: int
    category_name: str
    parent_category_id: Optional[int] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PromoInfo:
    """Promotion information"""
    promo_name: str
    promo_desc: str
    product_num: int
    raw_data: Dict[str, Any] = field(default_factory=dict)
