"""AliExpress Async API - Async SDK for AliExpress Open Platform"""

__version__ = "1.0.1"
__author__ = "GitHub Copilot"
__license__ = "MIT"

# Import main client for backward compatibility
from .client import AliExpressIOPClient
from .auth import AliExpressAuth
from .models import (
    Product, AffiliateLink, ProductSearchResponse, TokenResponse,
    Category, PromoInfo, ShippingInfo, SKUInfo, Order
)
from .exceptions import (
    AliExpressException,
    InvalidCredentialsException,
    ProductNotFoundException,
    APIRequestException
)

# Backward compatibility alias
AliExpressClient = AliExpressIOPClient

# Endpoint classes
from .endpoints.products import ProductsEndpoint
from .endpoints.orders import OrdersEndpoint
from .endpoints.categories import CategoriesEndpoint
from .endpoints.shipping import ShippingEndpoint
from .endpoints.affiliates import AffiliatesEndpoint
from .endpoints.auth import AuthEndpoint
from .endpoints.business import BusinessEndpoint

# Utility decorators
from .utils.logging import log_request, setup_logging
from .utils.rate_limiter import rate_limit, RateLimiter
from .utils.retry import retry, RetryPolicy
from .utils.webhooks import WebhookManager, WebhookPayload, WebhookEvent

__all__ = [
    # Version
    "__version__",
    # Client
    "AliExpressIOPClient",
    "AliExpressClient",  # Alias
    "AliExpressAuth",
    # Models
    "Product",
    "AffiliateLink",
    "ProductSearchResponse",
    "TokenResponse",
    "Category",
    "PromoInfo",
    "ShippingInfo",
    "SKUInfo",
    "Order",
    "AliExpressException",
    "InvalidCredentialsException",
    "ProductNotFoundException",
    "APIRequestException",
]
