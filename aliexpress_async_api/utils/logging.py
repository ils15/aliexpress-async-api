"""
Structured logging utilities and decorators
"""

import functools
import inspect
import logging
import time
from typing import Any, Callable

logger = logging.getLogger("aliexpress_async_api")


def log_request(operation_name: str):
    """
    Decorator to log API requests and responses

    Usage:
        @log_request("search_products")
        async def search_products(...):
            ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            logger.info(f"[START] {operation_name} - Args: {kwargs}")

            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"[SUCCESS] {operation_name} completed in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"[ERROR] {operation_name} failed in {duration:.3f}s: {str(e)}",
                    exc_info=True,
                )
                raise

        return wrapper

    return decorator


def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging configuration"""
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    logger.addHandler(console_handler)
    logger.setLevel(level)
