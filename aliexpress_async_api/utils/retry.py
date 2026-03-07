"""
Retry logic with exponential backoff
"""

import asyncio
import functools
from typing import Any, Callable, Tuple, Type


class RetryPolicy:
    """Configurable retry policy with exponential backoff"""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
    ):
        """
        Initialize retry policy

        Args:
            max_retries: Maximum number of retries
            base_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff
            exceptions: Tuple of exceptions to retry on
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.exceptions = exceptions

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for attempt number"""
        delay = self.base_delay * (self.exponential_base**attempt)
        return min(delay, self.max_delay)


def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """
    Decorator to retry async function with exponential backoff

    Usage:
        @retry(max_retries=3, base_delay=1.0)
        async def search_products(...):
            ...
    """
    policy = RetryPolicy(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        exceptions=exceptions,
    )

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(policy.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except policy.exceptions as e:
                    last_exception = e

                    if attempt >= policy.max_retries:
                        raise

                    delay = policy.get_delay(attempt)
                    await asyncio.sleep(delay)

            raise last_exception

        return wrapper

    return decorator
