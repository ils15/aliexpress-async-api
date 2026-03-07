"""
Rate limiting utilities for API calls
"""

import asyncio
import functools
import time
from typing import Any, Callable


class RateLimiter:
    """Async rate limiter using token bucket algorithm"""

    def __init__(self, calls: int = 10, period: float = 60.0):
        """
        Initialize rate limiter

        Args:
            calls: Number of calls allowed (must be > 0)
            period: Time period in seconds (must be > 0)
        """
        if calls <= 0:
            raise ValueError("calls must be a positive integer")
        if period <= 0:
            raise ValueError("period must be a positive number")
        self.calls = calls
        self.period = period
        self.tokens: float = calls
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary"""
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_update

            # Replenish tokens
            self.tokens = min(
                self.calls, self.tokens + (elapsed * self.calls / self.period)
            )
            self.last_update = now

            # Wait if no tokens available
            if self.tokens < 1:
                wait_time = (1 - self.tokens) * self.period / self.calls
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1


def rate_limit(calls: int = 10, period: float = 60.0):
    """
    Decorator to rate limit async function calls

    Usage:
        @rate_limit(calls=10, period=60)
        async def search_products(...):
            ...
    """
    limiter = RateLimiter(calls=calls, period=period)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            await limiter.acquire()
            return await func(*args, **kwargs)

        return wrapper

    return decorator
