"""
Webhook support for async notifications
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import aiohttp
import asyncio
import logging


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
        return {
            "event": self.event,
            "timestamp": self.timestamp,
            "data": self.data
        }


class WebhookManager:
    """Manage webhook registrations and dispatch"""
    
    def __init__(self):
        """Initialize webhook manager"""
        self.webhooks: Dict[str, List[str]] = {}
        self.session: Optional[aiohttp.ClientSession] = None
    
    def register(self, url: str, events: List[str]) -> None:
        """
        Register webhook URL for events
        
        Args:
            url: Webhook URL to receive notifications
            events: List of event names to subscribe to
        """
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
        payload = WebhookPayload(
            event=event,
            timestamp=time.time(),
            data=data
        )
        
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
                url,
                json=payload.to_dict(),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status >= 300:
                    logger.warning(
                        f"Webhook POST to {url} returned {response.status}"
                    )
        except Exception as e:
            logger.error(f"Failed to POST webhook to {url}: {str(e)}")
    
    async def close(self) -> None:
        """Close session"""
        if self.session:
            await self.session.close()
