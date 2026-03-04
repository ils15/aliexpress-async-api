# AliExpress Async API

A modern, fast, and 100% asynchronous Python client for the **AliExpress Open Platform (IOP) / Affiliate API**.

This library is a modern replacement for the official `aliexpress-sdk-python`. It natively bypasses the confusing `IncompleteSignature` errors by implementing the exact (but undocumented) V1 MD5 signature algorithm used by AliExpress for `/sync` Affiliate API endpoints, wrapping everything in `aiohttp`.

## ✨ Features
- **100% Asynchronous**: Built on `aiohttp` for high-performance concurrent requests.
- **Complete Affiliate Support**: Implementation for all 15 AliExpress Affiliate endpoints.
- **Type Safety**: Structured `dataclasses` for all response objects (Products, Orders, Categories, etc.).
- **Easy Auth**: Seamlessly handle OAuth flows and token refreshing.
- **Modern Signing**: Implements the V1 MD5 signature algorithm for `/sync` endpoints.

## 📦 Installation

```bash
pip install aliexpress-async-api
```

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

The library now supports exhaustive affiliate endpoints:

- **Hot Products**: `await client.get_hotproducts()`
- **Shipping Info**: `await client.get_shipping_info(product_id, target_sale_price="10.00")`
- **SKU Details**: `await client.get_sku_detail(product_id)`
- **Order Tracking**: `await client.get_order_list(start_time, end_time)`
- **Smart Match**: `await client.smart_match_products(keywords="...")`

## 🛠️ Development & Testing

We use `pytest` for testing. To run tests locally:

1. Clone the repository.
2. Create a `.env` file based on `.env.example`.
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest
   ```

## ⚖️ License
MIT
