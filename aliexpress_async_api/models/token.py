"""Token and authentication response models"""
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class TokenResponse:
    """OAuth token response"""
    access_token: str
    refresh_token: str
    expire_time: int
    account: str
    raw_data: Dict[str, Any] = field(default_factory=dict)
