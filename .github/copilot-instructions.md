# GitHub Copilot Instructions — aliexpress-async-api

## Project Overview
Async Python client for the AliExpress IOP Open Platform API.
Target: Python 3.8+, `aiohttp`-based, zero blocking I/O.

---

## Architecture

```
aliexpress_async_api/
├── client.py          # AliExpressIOPClient — main entry point
├── auth/
│   ├── oauth.py       # OAuth 2.0 token flow
│   └── signature.py   # MD5-V1 request signing (IOP protocol)
├── endpoints/
│   ├── base.py        # BaseEndpoint — shared HTTP helpers
│   ├── products.py    # search, details, smart_match, hotproducts, download
│   ├── orders.py      # list_orders, list_by_index, get_order
│   ├── categories.py  # get_categories, promo products
│   ├── shipping.py    # shipping info, SKU details
│   ├── affiliates.py  # generate_affiliate_link
│   ├── auth.py        # get_token, refresh_token
│   └── business.py    # business_license_inquiry
├── models/            # Typed dataclasses for all API responses
└── utils/
    ├── rate_limiter.py # Token-bucket RateLimiter + @rate_limit decorator
    ├── retry.py        # Exponential-backoff RetryPolicy + @retry decorator
    ├── logging.py      # @log_request decorator
    └── webhooks.py     # WebhookManager (async POST delivery)
```

---

## Code Conventions

1. **All I/O is async** — never use blocking calls (`requests`, `time.sleep`, open without aiofiles, etc.)
2. **Type hints everywhere** — all functions must be annotated; use `from __future__ import annotations` at module top if needed
3. **Models = dataclasses** — never return raw `dict`; always return a typed model from `models/`
4. **Errors** — raise specific exceptions from `exceptions.py`, never bare `except Exception`
5. **No hardcoded credentials** — use env vars or client constructor params
6. **Conventional Commits** — every commit message must follow: `type(scope): description`
   - Valid types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
   - Example: `feat(products): add download_products endpoint`

---

## Testing Rules

- Test runner: `pytest tests/ --cov=aliexpress_async_api --cov-fail-under=85`
- **85% minimum coverage** — any PR that drops below 85% must add missing tests
- Tests must be **fully async** (`pytest-asyncio`, `asyncio_mode = "auto"`)
- **No live API calls** — mock all HTTP using `aiohttp` mock or `pytest-mock`
- Every new endpoint method needs at least one success test and one error test

---

## Branch Strategy

```
develop  ──── day-to-day development
    │
    └── auto PR ──► master ──► CI bump + PyPI publish
```

- Develop on `develop` or feature branches merged into `develop`
- Only `master`-merges trigger PyPI releases
- The auto-PR bot reads commits and classifies the change type automatically

---

## Semantic Versioning Rules (from commit messages on PR to master)

| Commit prefix   | Version bump |
|-----------------|--------------|
| `BREAKING CHANGE` or `feat!:` | MAJOR |
| `feat:`         | MINOR        |
| `fix:`, `refactor:` | PATCH   |
| `docs:`, `test:`, `chore:` | no publish |

---

## When Generating Code

- Prefer `async with aiohttp.ClientSession() as session` patterns
- Reuse `BaseEndpoint._request()` for all API calls — do not create raw HTTP calls
- When adding a model, add it to `models/__init__.py` re-exports
- When adding an endpoint method, add it to `client.py` as a delegating property
- Tests go in `tests/test_endpoints_<module>.py` or `tests/test_models_<module>.py`

---

## Agent Ecosystem

Agents are defined in `.github/agents/`. Use them in Copilot Chat with `@agent-name`.

| Agent | Role | When to use |
|---|---|---|
| `@zeus` | Orchestrator | Start here for any new feature or epic |
| `@athena` | Planner | Design a feature — produces a TDD plan, never writes code |
| `@hermes` | Backend | Implement Python/async code (endpoints, models, utils) |
| `@iris` | GitHub ops | Open PRs, create releases, manage branches and issues |
| `@temis` | Reviewer | Code review, security check, coverage validation |
| `@apollo` | Discovery | Codebase exploration, docs research |
| `@mnemosyne` | Memory/Docs | Update CHANGELOG, README, memory bank |
| `@hephaestus` | Hotfix | Emergency fixes directly to master |
| `@ra` | Infra/CI | GitHub Actions, Docker, deployment scripts |
| `@maat` | Data/DB | Data models, schema, serialization |

### Release flow with agents

```
# 1. Develop on develop branch (normal push)
#    → auto-pr.yml creates PR develop → master automatically
#    → @iris can also create the PR manually if needed

# 2. To plan a new feature before starting:
@athena plan: <describe the feature>

# 3. To open / update the release PR manually:
@iris create PR from develop to master for release

# 4. To review the PR before merging:
@temis review PR #<number>
```
