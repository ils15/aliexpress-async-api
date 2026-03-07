"""
Base endpoint class with common response parsing logic
"""

from typing import Any, Dict, List, Optional


class BaseEndpoint:
    """Base class for all endpoint groups"""

    def __init__(self, request_method):
        """
        Initialize endpoint

        Args:
            request_method: Async function to make API requests
        """
        self.request = request_method

    @staticmethod
    def extract_nested_value(data: Dict[str, Any], *keys: str) -> Any:
        """
        Extract nested value from dict using key path

        Example:
            extract_nested_value(
                {"a": {"b": {"c": "value"}}},
                "a", "b", "c"
            ) -> "value"
        """
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, {})
            else:
                return None
        return value
