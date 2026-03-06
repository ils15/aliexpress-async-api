# Quick Start: aliexpress-async-api

Get up and running with the AliExpress Affiliate API in 5 minutes!

## Requirements

- An approved **AliExpress Open Platform** account.
- Your `app_key`, `app_secret`, and `tracking_id` from the [AliExpress Developer Console](https://developers.aliexpress.com).

## 1. Installation

```bash
pip install aliexpress-async-api
```

## 2. Basic Setup (FastAPI Example)

Here is how to use this library inside a modern async framework like FastAPI to avoid thread-blocking while waiting for AliExpress's API:

```python
from fastapi import FastAPI
from aliexpress_async_api import AliExpressClient

app = FastAPI()

# Load these from environment variables in production
APP_KEY    = "your_app_key"
APP_SECRET = "your_app_secret"
TRACKING   = "your_tracking_id"

# Instantiate once on startup and reuse across requests
# to share the connection pool and rate limiter.
client = AliExpressClient(
    app_key=APP_KEY,
    app_secret=APP_SECRET,
    tracking_id=TRACKING,
)

@app.get("/search/{keyword}")
async def search_products(keyword: str):
    response = await client.search_products(
        keyword=keyword,
        page_size=5,
        target_currency="BRL",
        target_language="PT",
        country="BR",
    )

    results = []
    for product in response.products:
        results.append({
            "product_id": product.product_id,
            "title":      product.product_title,
            "price":      product.target_sale_price,
            "image":      product.product_main_image_url,
            "affiliate":  product.promotion_link,
        })

    return {"total": response.total_record_count, "results": results}

@app.on_event("shutdown")
async def shutdown():
    await client.close()
```

## 3. Generating Affiliate Links

Turn any AliExpress product URL into a trackable affiliate link:

```python
links = await client.generate_affiliate_link(
    source_values="https://www.aliexpress.com/item/1234567890.html",
)

print(links[0].promotion_link)
# https://s.click.aliexpress.com/e/...
```

## 4. Parallel Execution (Safe Throttling)

Need to fetch multiple products at once? Use `asyncio.gather` — the built-in
`RateLimiter` will automatically space out requests so you don't hit API limits:

```python
import asyncio
from aliexpress_async_api import AliExpressClient

async def parallel_search():
    async with AliExpressClient(APP_KEY, APP_SECRET, TRACKING) as client:
        tasks = [
            client.search_products(keyword="smartphone", page_size=3),
            client.search_products(keyword="headphones",  page_size=3),
            client.search_products(keyword="smartwatch",  page_size=3),
        ]

        # Requests are spaced out automatically!
        phones, headphones, watches = await asyncio.gather(*tasks)
        return phones, headphones, watches
```

## 5. Using Advanced Decorators

Stack the built-in utility decorators on your own functions for production-grade reliability:

```python
from aliexpress_async_api.utils.logging     import log_request
from aliexpress_async_api.utils.rate_limiter import rate_limit
from aliexpress_async_api.utils.retry        import retry

@log_request("search_products")   # logs timing + errors automatically
@rate_limit(calls=10, period=60)  # max 10 calls per minute
@retry(max_retries=3)             # retries up to 3× with exponential backoff
async def search(keyword: str):
    async with AliExpressClient(APP_KEY, APP_SECRET, TRACKING) as client:
        return await client.search_products(keyword=keyword)
```

## 6. Environment Variables (Recommended)

Never hardcode credentials. Use a `.env` file:

```env
ALIEXPRESS_APP_KEY=your_app_key
ALIEXPRESS_APP_SECRET=your_app_secret
ALIEXPRESS_TRACKING_ID=your_tracking_id
```

```python
import os
from dotenv import load_dotenv
from aliexpress_async_api import AliExpressClient

load_dotenv()

client = AliExpressClient(
    app_key=os.environ["ALIEXPRESS_APP_KEY"],
    app_secret=os.environ["ALIEXPRESS_APP_SECRET"],
    tracking_id=os.environ["ALIEXPRESS_TRACKING_ID"],
)
```

A `.env.example` file is included in the repository.

