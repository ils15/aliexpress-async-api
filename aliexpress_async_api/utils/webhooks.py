"""
Webhook support for async notifications
"""

import asyncio
import ipaddress
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import aiohttp

logger = logging.getLogger(__name__)


class WebhookEvent(str, Enum):
    """Supported webhook events"""

    ORDER_COMPLETED = "order.completed"
    PRODUCT_FOUND = "product.found"
    LINK_GENERATED = "link.generated"
    ERROR_OCCURRED = "error.occurred"


@dataclass
class WebhookPayload:
    """Webhook notification payload"""

    event: str
    timestamp: float
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {"event": self.event, "timestamp": self.timestamp, "data": self.data}


class WebhookManager:
    """Manage webhook registrations and dispatch"""

    def __init__(self):
        """Initialize webhook manager"""
        self.webhooks: Dict[str, List[str]] = {}
        self.session: Optional[aiohttp.ClientSession] = None

    def _validate_webhook_url(self, url: str) -> None:
        """
        Validate a webhook URL to prevent SSRF attacks.

        Allows only http/https URLs that do not point to localhost,
        loopback addresses, or private/reserved IP ranges.

        Raises:
            ValueError: if the URL scheme is unsupported or the host is
                        a private/reserved/loopback address.
        """
        try:
            parsed = urlparse(url)
        except Exception:
            raise ValueError(f"Invalid webhook URL: {url!r}")

        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                f"Webhook URL must use http or https, got: {parsed.scheme!r}"
            )

        hostname = parsed.hostname
        if not hostname:
            raise ValueError(f"Webhook URL has no hostname: {url!r}")

        _BLOCKED_HOSTS = {"localhost", "localhost.localdomain", "0.0.0.0", "::1"}
        if hostname.lower() in _BLOCKED_HOSTS:
            raise ValueError(f"Webhook URL hostname is not allowed: {hostname!r}")

        # When the hostname is a literal IP address, reject private/reserved ranges.
        # (Hostname-based DNS rebinding is not covered here.)
        try:
            addr = ipaddress.ip_address(hostname)
        except ValueError:
            # Not an IP address — it's a fully-qualified domain name, which is fine.
            pass
        else:
            if (
                addr.is_private
                or addr.is_loopback
                or addr.is_reserved
                or addr.is_link_local
            ):
                raise ValueError(
                    f"Webhook URL points to a private or reserved address: {hostname!r}"
                )

    def register(self, url: str, events: List[str]) -> None:
        """
        Register webhook URL for events

        Args:
            url: Webhook URL to receive notifications (must be a public http/https URL)
            events: List of event names to subscribe to

        Raises:
            ValueError: if url fails security validation
        """
        self._validate_webhook_url(url)
        for event in events:
            if event not in self.webhooks:
                self.webhooks[event] = []
            if url not in self.webhooks[event]:
                self.webhooks[event].append(url)

    def unregister(self, url: str, events: Optional[List[str]] = None) -> None:
        """Unregister webhook"""
        if events is None:
            # Remove from all events
            for event_urls in self.webhooks.values():
                if url in event_urls:
                    event_urls.remove(url)
        else:
            # Remove from specific events
            for event in events:
                if event in self.webhooks and url in self.webhooks[event]:
                    self.webhooks[event].remove(url)

    async def dispatch(self, event: str, data: Dict[str, Any]) -> None:
        """
        Dispatch webhook to all registered URLs

        Args:
            event: Event name
            data: Event data
        """
        if event not in self.webhooks:
            return

        import time

        payload = WebhookPayload(event=event, timestamp=time.time(), data=data)

        if self.session is None:
            self.session = aiohttp.ClientSession()

        tasks = []
        for url in self.webhooks[event]:
            tasks.append(self._post_webhook(url, payload))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _post_webhook(self, url: str, payload: WebhookPayload) -> None:
        """Post webhook to URL"""
        try:
            async with self.session.post(
                url, json=payload.to_dict(), timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status >= 300:
                    logger.warning(f"Webhook POST to {url} returned {response.status}")
        except Exception as e:
            logger.error(f"Failed to POST webhook to {url}: {str(e)}")

    async def close(self) -> None:
        """Close session"""
        if self.session:
            await self.session.close()
