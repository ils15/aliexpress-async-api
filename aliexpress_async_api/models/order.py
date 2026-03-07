"""Order-related models"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Order:
    """AliExpress affiliate order"""

    order_id: int
    order_status: str
    order_time: str
    estimated_commission: str
    product_title: str
    product_count: int
    product_price: str
    raw_data: Dict[str, Any] = field(default_factory=dict)
