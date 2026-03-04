# AliExpress Async API - Architecture & Development Guide

## Project Overview

Modern, fully async Python client for **AliExpress Open Platform (IOP) Affiliate API**.

### Key Features
- 100% asynchronous (aiohttp-based)
- 15+ Affiliate endpoints implemented
- Type-safe dataclasses for all responses
- MD5 V1 signature algorithm (matches official spec)
- OAuth 2.0 flow support
- 96% test coverage

## Architecture

### Module Structure

```
aliexpress_async_api/
├── client.py                       # Main async client orchestrating all requests
│
├── auth/                           # Authentication & signature
│   ├── oauth.py                   # OAuth2 authorization endpoints
│   └── signature.py                # V1 MD5 signature algorithm
│
├── models/                         # Response dataclasses
│   ├── product.py                 # Product, ProductSearchResponse
│   ├── order.py                   # Order
│   ├── token.py                   # TokenResponse
│   ├── category.py                # Category, PromoInfo
│   ├── affiliate.py                # AffiliateLink
│   ├── shipping.py                # ShippingInfo, SKUInfo
│   └── base.py                    # BaseModel (common functionality)
│
├── endpoints/                      # API method grouping (future)
│   └── __init__.py
│
├── exceptions.py                   # Custom exception classes
└── utils/                          # Utility functions
    └── __init__.py
```

### Design Patterns

#### 1. **Context Manager Pattern**
```python
async with AliExpressIOPClient(app_key, app_secret) as client:
    response = await client.search_products("laptop")
```
Ensures proper HTTP session cleanup.

#### 2. **Dataclass Models**
All API responses are type-safe dataclasses with:
- Required fields (product_id, title, etc.)
- Optional fields (shop_url, evaluate_rate)
- raw_data field (preserves complete API response)

#### 3. **Signature Algorithm**
V1 MD5 signature as per AliEx spec:
- Merge system + business parameters
- Sort alphabetically
- Concatenate: SECRET + k1v1k2v2...kNvN + SECRET
- MD5 hash (uppercase)

---

## API Endpoints Reference

### Product Endpoints (6)

| Method | Endpoint ID | Purpose |
|--------|-----------|---------|
| `search_products(keyword, page_no, page_size, ...)` | aliexpress.affiliate.product.query | Search by keywords |
| `get_product_details(product_ids, ...)` | aliexpress.affiliate.productdetail.get | Get details for specific IDs |
| `smart_match_products(keywords, ...)` | aliexpress.affiliate.product.smartmatch | Smart matching |
| `get_hotproducts(category_ids, ...)` | aliexpress.affiliate.hotproduct.query | Trending products |
| `get_hotproduct_download(category_id)` | aliexpress.affiliate.hotproduct.download | Download trending data |

### Category & Promo Endpoints (3)

| Method | Endpoint ID | Purpose |
|--------|-----------|---------|
| `get_categories()` | aliexpress.affiliate.category.get | List all categories |
| `get_featured_promo()` | aliexpress.affiliate.featuredpromo.get | List promotions |
| `get_featured_promo_products(promo_name, ...)` | aliexpress.affiliate.featuredpromo.products.get | Products in promo |

### Affiliate Link Endpoints (1)

| Method | Endpoint ID | Purpose |
|--------|-----------|---------|
| `generate_affiliate_link(source_values, ...)` | aliexpress.affiliate.link.generate | Create trackable links |

### Shipping & SKU Endpoints (2)

| Method | Endpoint ID | Purpose |
|--------|-----------|---------|
| `get_shipping_info(product_id, target_sale_price, ...)` | aliexpress.affiliate.product.shipping.get | Shipping details |
| `get_sku_detail(product_id, ...)` | aliexpress.affiliate.product.sku.detail.get | SKU variations |

### Order Endpoints (3)

| Method | Endpoint ID | Purpose |
|--------|-----------|---------|
| `get_order_list(start_time, end_time, status, ...)` | aliexpress.affiliate.order.list | List orders |
| `get_order_list_by_index(start_query_index_id, ...)` | aliexpress.affiliate.order.listbyindex | Pagination via index |
| `get_order_info(order_ids)` | aliexpress.affiliate.order.get | Get specific orders |

### Auth Endpoints (2)

| Method | Endpoint ID | Purpose |
|--------|-----------|---------|
| `get_token(code)` | aliexpress.auth.token.create | Exchange code for token |
| `refresh_token(refresh_token_value)` | aliexpress.auth.token.refresh | Refresh expired token |

---

## Development Guide

### Installation & Setup

```bash
# Clone repository
git clone https://github.com/ils15/aliexpress-async-api.git
cd aliexpress-async-api

# Install with dev dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=aliexpress_async_api --cov-report=html

# Run specific test file
pytest tests/test_client_integration.py -v

# Run with markers
pytest tests/ -m asyncio -v
```

### Code Quality

```bash
# Format code
black aliexpress_async_api tests

# Sort imports
isort aliexpress_async_api tests

# Type checking
mypy aliexpress_async_api --ignore-missing-imports

# Linting (via pre-commit)
pre-commit run --all-files
```

### Test Coverage Breakdown

| Module | Coverage | Status |
|--------|----------|--------|
| auth/oauth.py | 100% | ✅ Complete |
| auth/signature.py | 100% | ✅ Complete |
| models/* | 100% | ✅ Complete |
| client.py | 93% | ✅ Excellent |
| exceptions.py | 100% | ✅ Complete |
| **TOTAL** | **96%** | ✅ Exceeds 85% target |

**Missing Coverage (7% of 192 LOC in client.py):**
- Error paths for network failures (not testable without live API)
- Deprecated aliases (query_products, get_product_detail)

---

## Code Standards

### Naming Conventions
- Classes: `PascalCase` (e.g., `AliExpressIOPClient`)
- Functions: `snake_case` (e.g., `search_products`)
- Constants: `UPPER_CASE` (e.g., `BASE_URL`)
- Private methods: `_leading_underscore` (e.g., `_check_error`)

### Docstring Format
All public methods include Google-style docstrings:
```python
async def search_products(self, keyword: str) -> ProductSearchResponse:
    """
    Search for affiliate products.
    
    Args:
        keyword: Search term
        page_no: Page number (default 1)
        page_size: Results per page (default 20)
    
    Returns:
        ProductSearchResponse with matched products
        
    Raises:
        APIRequestException: If API returns error
    """
```

### Type Hints
All function signatures use complete type hints for IDE support and static analysis.

---

## Security Notes

### API Credentials
Never hardcode credentials. Always use environment variables:

```python
from dotenv import load_dotenv
load_dotenv()

app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")
```

### Token Management
Tokens are obtained via OAuth and should be:
- Stored securely (never in logs)
- Refreshed before expiry
- Passed via `access_token` parameter to methods

### Signature Security
The MD5 V1 algorithm is implemented exactly per AliExpress spec:
- Never expose app_secret
- Parameters are sorted before signing
- Signature covers both system and business parameters

---

## Contributing

### Adding New Endpoints

1. **Add model class** to appropriate `models/*.py` file
2. **Write tests first** in `tests/test_endpoints_*.py`
3. **Implement endpoint** in `client.py` or dedicated `endpoints/*.py`
4. **Ensure coverage** >85% for all new code
5. **Update README** with endpoint documentation

### PR Review Checklist
- [ ] 96%+ coverage maintained
- [ ] All tests pass (`pytest tests/`)
- [ ] Code formatted with Black
- [ ] Imports sorted with isort
- [ ] Type hints complete (mypy passes)
- [ ] Docstrings updated
- [ ] No hardcoded secrets

---

## Changelog

### v0.1.0 (March 2026)
- ✅ Initial refactor: modular structure (auth/, models/, endpoints/)
- ✅ 66 unit tests (96% coverage, was 4 tests with ~15%)
- ✅ CI/CD pipeline (GitHub Actions, Black, isort, mypy)
- ✅ All 15+ endpoints fully tested
- ✅ Complete type hint coverage
- ✅ Production-ready documentation

**Key Improvements:**
- Code organization: 3 monolithic files → 14 focused modules
- Test quality: 4 basic tests → 66 comprehensive tests
- Code quality: No linting → Full Black/isort/mypy compliance
- Automation: Manual testing → Automated CI/CD

---

## Support & Resources

- **GitHub Issues**: [Report bugs](https://github.com/ils15/aliexpress-async-api/issues)
- **Official Docs**: [AliExpress Open Platform](https://developers.aliexpress.com)
- **Examples**: See `tests/` directory for usage patterns

---

## License

MIT - See [LICENSE](LICENSE) file
