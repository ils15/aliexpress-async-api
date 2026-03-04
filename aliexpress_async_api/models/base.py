"""
Base model class with common functionality
"""
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class BaseModel:
    """
    Base model for all AliExpress API response objects.
    
    Provides:
    - raw_data: Complete unprocessed API response
    - Consistent structure for all models
    """
    raw_data: Dict[str, Any] = field(default_factory=dict)
