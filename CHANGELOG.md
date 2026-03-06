# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) —
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [1.0.1] - 2026-03-05

### Fixed
- Corrected author contact email and URL in package metadata.

---

## [1.0.0] - 2026-03-04

### Added

- **`AliExpressClient`** — fully async HTTP client for the AliExpress IOP Open Platform API.
- **20 API methods** across 7 endpoint classes:
  - `ProductsEndpoint` — `search_products`, `get_product_details`, `smart_match`, `get_hotproducts`, `download_products`
  - `OrdersEndpoint` — `list_orders`, `list_orders_by_index`, `get_order`
  - `CategoriesEndpoint` — `get_categories`, `get_featured_promo_products`, `get_promo_products`
  - `ShippingEndpoint` — `get_shipping_info`, `get_sku_details`
  - `AffiliatesEndpoint` — `generate_affiliate_link`
  - `AuthEndpoint` — `get_token`, `refresh_token`
  - `BusinessEndpoint` — `business_license_inquiry`
- **OAuth 2.0 + MD5-V1 signing** (`auth/`) — request signing as required by the IOP protocol.
- **Token-bucket rate limiter** (`utils/rate_limiter.py`) — `RateLimiter` class and `@rate_limit` decorator.
- **Exponential-backoff retry** (`utils/retry.py`) — `RetryPolicy` class and `@retry` decorator.
- **Structured async logging** (`utils/logging.py`) — `@log_request` decorator with timing and error tracking.
- **Webhook notifications** (`utils/webhooks.py`) — `WebhookManager` for event-based async POST delivery.
- **Typed response models** (`models/`) — dataclasses for products, orders, categories, shipping, tokens, and affiliates.
- **128-test suite** with 89%+ coverage; fully async, no live API dependency required.
- **GitHub Actions CI/CD** — multi-Python (3.8–3.12) test matrix, automated PyPI publishing with semantic versioning.
