# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-04

### Added

#### Architecture & Code Quality (Phase 1-5)
- Refactored monolithic code into 14 specialized modules
  - `auth/oauth.py`, `auth/signature.py` - OAuth 2.0 and MD5 V1 signing
  - `models/` - 8 dataclass modules for type-safe responses
  - `endpoints/` - 7 endpoint modules organizing 20 API methods
  - `exceptions.py` - Custom exception hierarchy
  - `utils/` - 4 utility modules with advanced features

- Comprehensive test suite with **103 tests, 89% coverage**
  - Unit tests for all auth, model, and endpoint modules
  - Integration tests for client and endpoint combinations
  - Mock-based async testing (no API dependency)

- CI/CD Pipeline via GitHub Actions
  - Multi-version Python testing (3.8-3.12)
  - Automated linting (Black, isort, mypy)
  - Pre-commit hooks for code quality
  - Coverage enforcement (89% baseline)

#### Features (New in v1.0.0)

**Feature 1: Endpoint Module Refactoring**
- Extracted 20 endpoint methods into specialized modules:
  - `ProductsEndpoint` - 5 methods (search, details, smart match, hotproducts, download)
  - `OrdersEndpoint` - 3 methods (list, list by index, get)
  - `CategoriesEndpoint` - 3 methods (get, featured promo, promo products)
  - `ShippingEndpoint` - 2 methods (shipping info, SKU details)
  - `AffiliatesEndpoint` - 1 method (generate link)
  - `AuthEndpoint` - 2 methods (get token, refresh token)
  - `BusinessEndpoint` - 1 method (business license inquiry)
- `BaseEndpoint` helper class with DRY response parsing
- 17 dedicated endpoint tests, all passing

**Feature 2: Structured Logging**
- `@log_request` decorator for async functions
- Captures operation name, parameters, timing, success/error states
- Automatic exception logging with tracebacks
- 2 comprehensive tests covering success and failure cases

**Feature 3: Async Rate Limiting**
- `RateLimiter` class with token bucket algorithm
- `@rate_limit` decorator (configurable calls/period)
- Non-blocking async acquisition with calculated wait times
- 3 tests validating limits enforcement and waiting behavior

**Feature 4: Request Retry with Exponential Backoff**
- `RetryPolicy` class with configurable parameters
- `@retry` decorator for automatic retry logic
- Exponential backoff: delay = base_delay × (exponential_base ^ attempt)
- Max delay cap to prevent excessive waits
- 3 tests covering first-try success, failure recovery, and exhaustion

**Feature 5: Webhook Support**
- `WebhookPayload` dataclass for event serialization
- `WebhookManager` for registration, dispatch, and cleanup
- Event-based dispatching (order.completed, product.found, link.generated, error.occurred)
- Async aiohttp POST to registered URLs
- 12 comprehensive tests for all webhook operations

### Projects & Documentation
- Comprehensive architecture documentation (`docs/ARCHITECTURE.md`)
  - Module overview and design patterns
  - All 20 endpoints detailed with examples
  - Development workflow and contribution guide

- Contributing guide (`CONTRIBUTING.md`)
  - TDD workflow explanation
  - Code standards and quality metrics
  - Step-by-step guide for adding new endpoints

- Updated README with
  - Feature highlights and quick start
  - All endpoint usage examples
  - Installation and configuration instructions
  - Quality metrics dashboard

### Changed
- **Breaking Change**: Monolithic `client.py` structure split into modules
  - Old direct method calls still work via `AliExpressClient`
  - New modular access via endpoint classes preferred for new code

### Technical Details
- **Framework**: Python 3.8+ with aiohttp async HTTP client
- **Testing**: pytest + pytest-asyncio + pytest-cov
- **Code Quality**: Black, isort, mypy with pre-commit integration
- **Async Patterns**: 100% async/await, no blocking I/O

---

## Future Roadmap

### Planned (v1.1.0+)
- WebSocket support for real-time order updates
- Advanced caching with TTL management
- SDK instrumentation (tracing, metrics)
- Async context managers for resource pooling
- Multi-account support for Enterprise affiliates
- Webhook event filtering and transformations

---

## Migration Guide

### From v0.x to v1.0.0

**Old pattern (still works):**
```python
async with AliExpressClient(app_key, app_secret) as client:
    products = await client.search_products(keyword="phone")
```

**New pattern (recommended):**
```python
async with AliExpressClient(app_key, app_secret) as client:
    endpoint = ProductsEndpoint(client.request)
    products = await endpoint.search_products(keyword="phone")
```

**With advanced features:**
```python
from aliexpress_async_api.utils.logging import log_request
from aliexpress_async_api.utils.retry import retry
from aliexpress_async_api.utils.rate_limiter import rate_limit

@log_request("search")
@rate_limit(calls=10, period=60)
@retry(max_retries=3)
async def search(keyword):
    async with AliExpressClient(app_key, app_secret) as client:
        endpoint = ProductsEndpoint(client.request)
        return await endpoint.search_products(keyword=keyword)
```

---

## Contributors
- Athena (Architecture & Planning)
- Apollo (Pattern Discovery)
- Hermes (Implementation & Testing)
- Ra (Infrastructure & CI/CD)
- Temis (Code Review)
- Mnemosyne (Documentation)
