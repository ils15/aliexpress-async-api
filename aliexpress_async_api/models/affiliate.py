"""Affiliate link models"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AffiliateLink:
    """Track able affiliate link"""

    promotion_link: str
    source_value: str
    raw_data: Dict[str, Any] = field(default_factory=dict)
