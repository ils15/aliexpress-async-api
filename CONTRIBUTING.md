# Contributing to AliExpress Async API

Thanks for considering contributing! This document outlines the contribution process to ensure consistency and quality.

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/oferta-china/aliexpress-async-api.git
cd aliexpress-async-api

# Create virtual environment (recommended)
python3.10 -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

### 2. Before Making Changes

- Check existing [GitHub Issues](https://github.com/oferta-china/aliexpress-async-api/issues)
- Create an issue for new features before implementing
- Discuss breaking changes in issues first

### 3. Implementation - TDD Process

We follow **Test-Driven Development (TDD)**:

#### RED Phase
1. Write failing tests first in `tests/test_*.py`
2. Tests should cover:
   - Happy path (normal usage)
   - Edge cases (empty lists, None values)
   - Error conditions (exceptions)

#### GREEN Phase
2. Write minimal code to pass tests
3. Ensure all tests pass: `pytest tests/ -v`

#### REFACTOR Phase
4. Improve code quality while keeping tests passing
5. Run linting: `black aliexpress_async_api tests/`
6. Run type checking: `mypy aliexpress_async_api`

###  4. Code Quality Requirements

All PRs must meet these quality gates:

```bash
# Format code
black aliexpress_async_api tests/

# Sort imports
isort aliexpress_async_api tests/

# Type checking (must pass)
mypy aliexpress_async_api --ignore-missing-imports

# Tests with coverage (must be >85%)
pytest tests/ --cov=aliexpress_async_api --cov-fail-under=85

# Pre-commit (must pass)
pre-commit run --all-files
```

### 5. PR Submission Checklist

Before submitting a pull request:

- [ ] **Tests written** - All new code has corresponding tests
- [ ] **Coverage maintained** - At least 85% test coverage
- [ ] **Formatted** - Ran `black aliexpress_async_api tests/`
- [ ] **Imports sorted** - Ran `isort aliexpress_async_api tests/`
- [ ] **Type safe** - All functions have type hints, mypy passes
- [ ] **Docstrings** - Public methods documented with Google-style docstrings
- [ ] **No secrets** - No hardcoded API keys, tokens, or credentials
- [ ] **Tests pass** - `pytest tests/ -v` shows all passing
- [ ] **Related issue** - PR links to relevant GitHub issue

### 6. Review Process

1. One maintainer reviews code against checklist
2. Changes requested? Push new commits (don't force-push)
3. Approved? Squash merge to master
4. Auto-deploy on merge if tests pass

---

## Adding New Endpoints

### Step 1: Create Issue & Plan

```
Title: Add [endpoint name] support
Body: 
- AliExpress endpoint: aliexpress.affiliate.xxx
- Required parameters: ...
- Response model needed: ...
```

### Step 2: Write Model (if new response type)

**File:** `aliexpress_async_api/models/new_type.py`

```python
from dataclasses import dataclass, field
from typing import Optional, Any, Dict

@dataclass
class NewResponseType:
    """Description of response"""
    field1: str
    field2: Optional[int] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
```

Add to `models/__init__.py`:
```python
from .new_type import NewResponseType
__all__ = [..., "NewResponseType"]
```

### Step 3: Write Tests First

**File:** `tests/test_endpoints_new_feature.py`

```python
@pytest.mark.asyncio
async def test_new_endpoint_returns_correct_type():
    mock_response = {...}  # Mock API response
    
    with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
        async with AliExpressIOPClient("key", "secret") as client:
            result = await client.new_endpoint_method()
            assert isinstance(result, NewResponseType)
```

### Step 4: Implement Endpoint

**File:** `aliexpress_async_api/client.py`

```python
async def new_endpoint_method(
    self,
    required_param: str,
    optional_param: Optional[str] = None,
    access_token: Optional[str] = None
) -> NewResponseType:
    """
    Brief description of endpoint.
    
    Args:
        required_param: What this does
        optional_param: What this does (default: ...)
        access_token: Optional session token for authenticated endpoint
    
    Returns:
        NewResponseType with response data
        
    Raises:
        APIRequestException: If API returns error
    """
    api_method = "aliexpress.affiliate.xxx"
    business = {
        "required_param": required_param,
    }
    if optional_param:
        business["optional_param"] = optional_param
    
    raw = await self.request(api_method, business, access_token)
    resp = raw.get("aliexpress_affiliate_xxx_response", {})
    result = resp.get("resp_result", {}).get("result", {})
    
    return NewResponseType(
        field1=result.get("field1", ""),
        field2=result.get("field2"),
        raw_data=result
    )
```

### Step 5: Verify Tests Pass

```bash
pytest tests/test_endpoints_new_feature.py -v
pytest tests/ --cov=aliexpress_async_api --cov-fail-under=85
```

### Step 6: Submit PR

Link to your issue and reference test commits.

---

## Code Style Guide

### Naming

- **Classes**: `PascalCase` - `class ProductSearchResponse`
- **Functions**: `snake_case` - `async def search_products()`
- **Constants**: `UPPER_CASE` - `BASE_URL = "https://..."`
- **Private methods**: `_leading_underscore` - `def _check_error()`

### Docstrings (Google Style)

```python
async def search_products(
    self,
    keyword: str,
    page_no: int = 1,
) -> ProductSearchResponse:
    """
    Search for affiliate products by keyword.
    
    Args:
        keyword: Search term (e.g., "3d printer")
        page_no: Page number for pagination (default: 1)
    
    Returns:
        ProductSearchResponse containing matched products
        
    Raises:
        APIRequestException: If AliExpress API returns error
        InvalidCredentialsException: If credentials invalid
    """
```

### Type Hints

Always include type hints:

```python
from typing import Optional, List, Dict, Any

# Good ✅
async def get_orders(
    self,
    start_date: str,
    end_date: str,
    page_size: int = 20
) -> List[Order]:
    ...

# Bad ❌
async def get_orders(self, start_date, end_date, page_size=20):
    ...
```

### Comments

- Comments explain **WHY**, not **WHAT**
- Code should be self-documenting (clear names, types)

```python
# Good ✅
# V1 MD5 signature requires params sorted alphabetically (AliExpress spec)
sorted_keys = sorted(all_params.keys())

# Bad ❌
# Sort keys
sorted_keys = sorted(all_params.keys())
```

---

## Testing Best Practices

### Test Organization

```
tests/
├── test_auth_*.py              # Authentication tests
├── test_models_*.py            # Model validation tests
├── test_client_*.py            # Client initialization tests
├── test_endpoints_*.py         # Endpoint method tests
└── conftest.py                 # Shared fixtures
```

### Mock External Dependencies

Always mock HTTP requests in tests:

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_endpoint():
    mock_response = {"result": "data"}
    
    with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
        async with AliExpressIOPClient("key", "secret") as client:
            result = await client.method()
            assert result.property == expected
```

### Edge Cases

Always test:
- Empty responses: `{"products": {"product": []}}`
- Missing optional fields: `{"field1": "value"}` (field2 omitted)
- Error responses: `{"error_response": {...}}`

---

## Common Issues & Fixes

### Issue: "ImportError: cannot import name 'X' from 'aliexpress_async_api'"
**Fix**: Check that `__init__.py` files have proper imports and `__all__` lists

### Issue: "pytest: command not found"
**Fix**: Ensure dev dependencies installed: `pip install -e ".[dev]"`

### Issue: "mypy error: Incompatible types in assignment"
**Fix**: Add proper type hints to function signatures and variables

### Issue: "Coverage dropped below 85%"
**Fix**: Add tests for uncovered code paths. Check: `pytest --cov-report=html`

---

## Questions?

- **GitHub Discussions**: [Ask a question](https://github.com/oferta-china/aliexpress-async-api/discussions)
- **Issues**: [Report bugs](https://github.com/oferta-china/aliexpress-async-api/issues)

---

Thank you for contributing! 🎉
