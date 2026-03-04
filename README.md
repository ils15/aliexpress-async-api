# AliExpress Async API

A modern, fast, and 100% asynchronous Python client for the **AliExpress Open Platform (IOP) / Affiliate API**.

This library is a modern replacement for the official `aliexpress-sdk-python`. It natively bypasses the confusing `IncompleteSignature` errors by implementing the exact (but undocumented) V1 MD5 signature algorithm used by AliExpress for `/sync` Affiliate API endpoints, wrapping everything in `aiohttp`.

## ✨ Features

- **100% Asynchronous**: Built on `aiohttp` for high-performance concurrent requests.
- **Complete Affiliate Support**: Implementation for all 15+ AliExpress Affiliate endpoints.
- **Type Safety**: Structured `dataclasses` for all response objects (Products, Orders, Categories, etc.).
- **Easy Auth**: Seamlessly handle OAuth flows and token refreshing.
- **Modern Signing**: Implements the V1 MD5 signature algorithm for `/sync` endpoints.
- **Production Ready**: 96% test coverage, full CI/CD pipeline, pre-commit hooks.
- **Well Documented**: Architecture guide, contributing guide, complete API reference.

## 📦 Installation

```bash
pip install aliexpress-async-api
```

**Requires Python 3.8+**

## 🚀 Quick Start

### Basic Client Setup

```python
import asyncio
from aliexpress_async_api import AliExpressIOPClient

async def main():
    async with AliExpressIOPClient(
        app_key="YOUR_APP_KEY", 
        app_secret="YOUR_APP_SECRET", 
        tracking_id="YOUR_TRACKING_ID"
    ) as client:
        # Search for products
        response = await client.search_products("3d printer", page_size=5)
        for product in response.products:
            print(f"- {product.product_title} ({product.sale_price})")

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Endpoints

The library now supports all 15+ affiliate endpoints:

**Product Search**
```python
# Search by keyword
response = await client.search_products("laptop", page_no=1, page_size=20)

# Get product details
products = await client.get_product_details(["1005006648408257"])

# Smart matching
response = await client.smart_match_products(keywords="headphones")

# Hot/trending products
hot = await client.get_hotproducts(category_ids="100")
```

**Affiliates & Links**
```python
# Generate trackable affiliate links
links = await client.generate_affiliate_link("https://aliexpress.com/item/...")
for link in links:
    print(f"Affiliate: {link.promotion_link}")
```

**Orders & Commission**
```python
# Get your affiliate orders
orders = await client.get_order_list("2026-01-01", "2026-12-31")
for order in orders:
    print(f"Order {order.order_id}: {order.estimated_commission} commission")

# Get order by ID
order_details = await client.get_order_info(["order_id_123"])
```

**Categories & Promos**
```python
# List categories
categories = await client.get_categories()

# Get featured promotions
promos = await client.get_featured_promo()
promo_products = await client.get_featured_promo_products("promo_name")
```

**Shipping & SKU**
```python
# Check shipping info
shipping = await client.get_shipping_info(
    product_id="1005006648408257",
    target_sale_price="10.00"
)

# Get SKU variations
skus = await client.get_sku_detail("1005006648408257")
for sku in skus:
    print(f"SKU {sku.sku_id}: {sku.sku_price} - {sku.sku_stock} in stock")
```

**Authentication**
```python
# OAuth flow example
auth_url = client.get_auth_url("https://yourapp.com/callback")
print(f"Send user to: {auth_url}")

# After user authorizes and you get code...
token_response = await client.get_token("authorization_code_from_callback")
print(f"Access token: {token_response.access_token}")

# Use token for subsequent requests
response = await client.search_products(
    "test",
    access_token=token_response.access_token
)

# Refresh token if needed
new_token = await client.refresh_token(token_response.refresh_token)
```

## 🛠️ Development & Testing

We use `pytest` for testing with **96% code coverage**. 

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ils15/aliexpress-async-api.git
   cd aliexpress-async-api
   ```

2. Install dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Setup pre-commit hooks (for auto-formatting):
   ```bash
   pre-commit install
   ```

4. Create `.env` file for testing credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your APP_KEY, APP_SECRET, TRACKING_ID
   ```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=aliexpress_async_api --cov-report=html

# Run specific test file
pytest tests/test_client_integration.py -v

# Run with verbose output
pytest tests/ -v
```

### Code Quality

```bash
# Format code with Black
black aliexpress_async_api tests/

# Sort imports with isort
isort aliexpress_async_api tests/

# Type checking with mypy
mypy aliexpress_async_api --ignore-missing-imports

# All checks via pre-commit
pre-commit run --all-files
```

## 📊 Project Quality

| Metric | Status |
|--------|--------|
| Test Coverage | ✅ 96% (target: 85%) |
| Tests | ✅ 66 tests (including 4 original + 62 new) |
| Type Safety | ✅ 100% type hints |
| Documentation | ✅ Architecture guide + Contributing guide |
| CI/CD | ✅ GitHub Actions workflow |

## 📚 Documentation

- [**Architecture Guide**](docs/ARCHITECTURE.md) - Module structure, design patterns, API reference
- [**Contributing Guide**](CONTRIBUTING.md) - Development workflow, TDD process, code standards
- [**API Reference**](docs/ARCHITECTURE.md#api-endpoints-reference) - All 15+ endpoints documented
- [**Examples**](tests/test_endpoint_coverage.py) - Real usage patterns in tests

## ⚙️ Project Structure

```
aliexpress-async-api/
├── aliexpress_async_api/
│   ├── client.py              # Main async client
│   ├── auth/                  # OAuth + signature algorithm
│   ├── models/                # Response dataclasses
│   ├── exceptions.py          # Custom exceptions
│   └── utils/                 # Utility functions
├── tests/                      # 66 unit & integration tests
├── docs/                       # Architecture & development docs
├── .github/workflows/          # CI/CD pipeline
├── pyproject.toml            # Project metadata & deps
└── README.md                 # This file
```

## 🔒 Security

All requests are signed with the official V1 MD5 algorithm. Keep your credentials safe:

```python
import os
from dotenv import load_dotenv

load_dotenv()
client = AliExpressIOPClient(
    app_key=os.getenv("APP_KEY"),
    app_secret=os.getenv("APP_SECRET")
)
```

## 🚀 Deployment

The package includes GitHub Actions for automated testing on every push:
- Runs tests on Python 3.8 - 3.12
- Enforces 85%+ code coverage
- Runs Black/isort/mypy checks
- Uploads coverage reports

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- TDD workflow
- Code quality requirements
- Adding new endpoints
- PR review process

## ⚖️ License

MIT - See [LICENSE](LICENSE) file

## 📞 Support

- **Issues**: [Report bugs](https://github.com/ils15/aliexpress-async-api/issues)
- **Discussions**: [Ask questions](https://github.com/ils15/aliexpress-async-api/discussions)
- **Official Docs**: [AliExpress Developers](https://developers.aliexpress.com)
