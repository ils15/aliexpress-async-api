"""
Tests for advanced utility features: logging, rate limiting, retries, webhooks
"""

import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aliexpress_async_api.utils.logging import log_request, setup_logging
from aliexpress_async_api.utils.rate_limiter import RateLimiter, rate_limit
from aliexpress_async_api.utils.retry import RetryPolicy, retry
from aliexpress_async_api.utils.webhooks import (
    WebhookEvent,
    WebhookManager,
    WebhookPayload,
)

# ==================== LOGGING TESTS ====================


class TestLoggingDecorator:
    """Tests for @log_request decorator"""

    @pytest.mark.asyncio
    async def test_log_request_success(self):
        """Test successful request logging"""

        @log_request("test_operation")
        async def test_func():
            return "success"

        with patch("aliexpress_async_api.utils.logging.logger") as mock_logger:
            result = await test_func()

            assert result == "success"
            assert mock_logger.info.call_count == 2
            calls = [str(call) for call in mock_logger.info.call_args_list]
            assert any("START" in str(call) for call in calls)
            assert any("SUCCESS" in str(call) for call in calls)

    @pytest.mark.asyncio
    async def test_log_request_failure(self):
        """Test failed request logging"""

        @log_request("test_operation")
        async def test_func():
            raise ValueError("Test error")

        with patch("aliexpress_async_api.utils.logging.logger") as mock_logger:
            with pytest.raises(ValueError):
                await test_func()

            assert mock_logger.info.call_count == 1
            assert mock_logger.error.call_count == 1


# ==================== RATE LIMITER TESTS ====================


class TestRateLimiter:
    """Tests for RateLimiter class"""

    @pytest.mark.asyncio
    async def test_rate_limiter_allows_calls_within_limit(self):
        """Test that calls within limit don't wait"""
        limiter = RateLimiter(calls=2, period=1.0)

        start = time.time()
        await limiter.acquire()
        await limiter.acquire()
        elapsed = time.time() - start

        # Should complete quickly (no waiting)
        assert elapsed < 0.5

    @pytest.mark.asyncio
    async def test_rate_limiter_waits_when_exhausted(self):
        """Test that limiter waits when calls exhausted"""
        limiter = RateLimiter(calls=1, period=0.5)

        start = time.time()
        await limiter.acquire()  # First call (no wait)
        await limiter.acquire()  # Second call (should wait ~0.5s)
        elapsed = time.time() - start

        # Should wait approximately 0.5 seconds
        assert elapsed >= 0.4


class TestRateLimitDecorator:
    """Tests for @rate_limit decorator"""

    @pytest.mark.asyncio
    async def test_rate_limit_decorator(self):
        """Test @rate_limit decorator enforces limits"""
        call_count = 0

        @rate_limit(calls=2, period=1.0)
        async def limited_func():
            nonlocal call_count
            call_count += 1

        start = time.time()
        await limited_func()
        await limited_func()
        await limited_func()  # Should wait
        elapsed = time.time() - start

        assert call_count == 3
        assert elapsed >= 0.4


# ==================== RETRY TESTS ====================


class TestRetryPolicy:
    """Tests for RetryPolicy class"""

    def test_exponential_backoff_calculation(self):
        """Test exponential backoff delay calculation"""
        policy = RetryPolicy(base_delay=1.0, exponential_base=2.0, max_delay=60.0)

        assert policy.get_delay(0) == 1.0  # 1 * 2^0
        assert policy.get_delay(1) == 2.0  # 1 * 2^1
        assert policy.get_delay(2) == 4.0  # 1 * 2^2
        assert policy.get_delay(3) == 8.0  # 1 * 2^3

    def test_max_delay_cap(self):
        """Test that delay is capped at max_delay"""
        policy = RetryPolicy(base_delay=1.0, exponential_base=2.0, max_delay=10.0)

        assert policy.get_delay(4) == 10.0  # Would be 16, but capped at 10


class TestRetryDecorator:
    """Tests for @retry decorator"""

    @pytest.mark.asyncio
    async def test_retry_succeeds_on_first_try(self):
        """Test that function returns immediately on success"""
        attempt_count = 0

        @retry(max_retries=3)
        async def succeeds_first():
            nonlocal attempt_count
            attempt_count += 1
            return "success"

        result = await succeeds_first()
        assert result == "success"
        assert attempt_count == 1

    @pytest.mark.asyncio
    async def test_retry_succeeds_after_failures(self):
        """Test that function retries on failure"""
        attempt_count = 0

        @retry(max_retries=3, base_delay=0.01)
        async def fails_twice():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise ValueError("Temporary error")
            return "success"

        result = await fails_twice()
        assert result == "success"
        assert attempt_count == 3

    @pytest.mark.asyncio
    async def test_retry_gives_up_after_max_retries(self):
        """Test that function raises after max retries exhausted"""
        attempt_count = 0

        @retry(max_retries=2, base_delay=0.01)
        async def always_fails():
            nonlocal attempt_count
            attempt_count += 1
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            await always_fails()

        assert attempt_count == 3  # Initial + 2 retries


# ==================== WEBHOOK TESTS ====================


class TestWebhookPayload:
    """Tests for WebhookPayload"""

    def test_webhook_payload_creation(self):
        """Test webhook payload creation and serialization"""
        payload = WebhookPayload(
            event="order.completed", timestamp=1234567890.0, data={"order_id": 123}
        )

        assert payload.event == "order.completed"
        assert payload.timestamp == 1234567890.0
        assert payload.data == {"order_id": 123}

    def test_webhook_payload_to_dict(self):
        """Test webhook payload to_dict conversion"""
        payload = WebhookPayload(
            event="product.found", timestamp=1234567890.0, data={"product_id": "abc123"}
        )

        payload_dict = payload.to_dict()
        assert payload_dict["event"] == "product.found"
        assert payload_dict["timestamp"] == 1234567890.0
        assert payload_dict["data"] == {"product_id": "abc123"}


class TestWebhookManager:
    """Tests for WebhookManager"""

    def test_webhook_registration(self):
        """Test registering webhook URLs"""
        manager = WebhookManager()

        manager.register("http://example.com/webhook", ["order.completed"])

        assert "order.completed" in manager.webhooks
        assert "http://example.com/webhook" in manager.webhooks["order.completed"]

    def test_webhook_registration_multiple_events(self):
        """Test registering webhook for multiple events"""
        manager = WebhookManager()

        manager.register(
            "http://example.com/webhook", ["order.completed", "product.found"]
        )

        assert "http://example.com/webhook" in manager.webhooks["order.completed"]
        assert "http://example.com/webhook" in manager.webhooks["product.found"]

    def test_webhook_unregistration(self):
        """Test unregistering webhook"""
        manager = WebhookManager()
        manager.register("http://example.com/webhook", ["order.completed"])

        manager.unregister("http://example.com/webhook", ["order.completed"])

        assert "http://example.com/webhook" not in manager.webhooks.get(
            "order.completed", []
        )

    def test_webhook_unregister_all_events(self):
        """Test unregistering from all events"""
        manager = WebhookManager()
        manager.register(
            "http://example.com/webhook", ["order.completed", "product.found"]
        )

        manager.unregister("http://example.com/webhook")

        assert "http://example.com/webhook" not in manager.webhooks.get(
            "order.completed", []
        )
        assert "http://example.com/webhook" not in manager.webhooks.get(
            "product.found", []
        )

    @pytest.mark.asyncio
    async def test_webhook_dispatch_no_subscribers(self):
        """Test dispatching to non-existent event (no subscribers)"""
        manager = WebhookManager()

        # Should not raise
        await manager.dispatch("unknown.event", {"data": "test"})

    @pytest.mark.asyncio
    async def test_webhook_dispatch_to_subscribers(self):
        """Test dispatching to registered subscribers"""
        manager = WebhookManager()
        manager.register("http://example.com/webhook1", ["order.completed"])
        manager.register("http://example.com/webhook2", ["order.completed"])

        # Mock aiohttp
        with patch(
            "aliexpress_async_api.utils.webhooks.aiohttp.ClientSession"
        ) as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__.return_value = mock_response
            mock_session.return_value.post.return_value = mock_ctx

            manager.session = mock_session.return_value

            await manager.dispatch("order.completed", {"order_id": 123})

            # Should attempt to POST to both URLs
            assert manager.session.post.call_count == 2

    @pytest.mark.asyncio
    async def test_webhook_cleanup(self):
        """Test webhook manager cleanup"""
        manager = WebhookManager()

        with patch(
            "aliexpress_async_api.utils.webhooks.aiohttp.ClientSession"
        ) as mock_session:
            mock_session_obj = AsyncMock()
            manager.session = mock_session_obj

            await manager.close()

            mock_session_obj.close.assert_called_once()


class TestWebhookIntegration:
    """Integration tests for webhook system"""

    @pytest.mark.asyncio
    async def test_webhook_event_enum(self):
        """Test webhook event enum"""
        assert WebhookEvent.ORDER_COMPLETED == "order.completed"
        assert WebhookEvent.PRODUCT_FOUND == "product.found"
        assert WebhookEvent.LINK_GENERATED == "link.generated"
        assert WebhookEvent.ERROR_OCCURRED == "error.occurred"


# ==================== SECURITY TESTS ====================


class TestWebhookSSRFProtection:
    """Tests that WebhookManager rejects SSRF-prone URLs"""

    def _manager(self) -> WebhookManager:
        return WebhookManager()

    # --- valid URLs that must be accepted ---
    @pytest.mark.parametrize(
        "url",
        [
            "https://example.com/hook",
            "http://example.com/hook",
            "https://hooks.example.org/events",
            "https://my-service.io:8080/webhook",
        ],
    )
    def test_valid_public_url_accepted(self, url):
        m = self._manager()
        m.register(url, ["order.completed"])  # must not raise
        assert url in m.webhooks["order.completed"]

    # --- URLs that must be rejected ---
    @pytest.mark.parametrize(
        "url",
        [
            "http://localhost/webhook",
            "http://localhost.localdomain/webhook",
            "http://127.0.0.1/webhook",
            "http://127.0.0.2/admin",
            "http://0.0.0.0/webhook",
            "http://10.0.0.1/webhook",
            "http://10.255.255.255/webhook",
            "http://172.16.0.1/webhook",
            "http://172.31.255.255/webhook",
            "http://192.168.1.1/webhook",
            "http://192.168.0.0/webhook",
            "http://169.254.169.254/latest/meta-data/",  # AWS metadata service
            "http://[::1]/webhook",  # IPv6 loopback
            "ftp://example.com/webhook",  # wrong scheme
            "file:///etc/passwd",  # file scheme
            "//example.com/webhook",  # scheme-relative (empty scheme)
        ],
    )
    def test_ssrf_url_rejected(self, url):
        m = self._manager()
        with pytest.raises(ValueError):
            m.register(url, ["order.completed"])


class TestRateLimiterValidation:
    """Tests that RateLimiter rejects invalid construction parameters"""

    def test_zero_calls_raises(self):
        with pytest.raises(ValueError, match="calls"):
            RateLimiter(calls=0, period=60.0)

    def test_negative_calls_raises(self):
        with pytest.raises(ValueError, match="calls"):
            RateLimiter(calls=-5, period=60.0)

    def test_zero_period_raises(self):
        with pytest.raises(ValueError, match="period"):
            RateLimiter(calls=10, period=0.0)

    def test_negative_period_raises(self):
        with pytest.raises(ValueError, match="period"):
            RateLimiter(calls=10, period=-1.0)

    def test_valid_params_accepted(self):
        limiter = RateLimiter(calls=1, period=0.001)
        assert limiter.calls == 1
