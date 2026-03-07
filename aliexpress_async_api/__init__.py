"""AliExpress Async API - Async SDK for AliExpress Open Platform"""

__version__ = "1.0.1"
__author__ = "GitHub Copilot"
__license__ = "MIT"

from .auth import AliExpressAuth

# Import main client for backward compatibility
from .client import AliExpressIOPClient
from .exceptions import (
    AliExpressException,
    APIRequestException,
    InvalidCredentialsException,
    ProductNotFoundException,
)
from .models import (
    AffiliateLink,
    Category,
    Order,
    Product,
    ProductSearchResponse,
    PromoInfo,
    ShippingInfo,
    SKUInfo,
    TokenResponse,
)

# Backward compatibility alias
AliExpressClient = AliExpressIOPClient

from .endpoints.affiliates import AffiliatesEndpoint
from .endpoints.auth import AuthEndpoint
from .endpoints.business import BusinessEndpoint
from .endpoints.categories import CategoriesEndpoint
from .endpoints.orders import OrdersEndpoint

# Endpoint classes
from .endpoints.products import ProductsEndpoint
from .endpoints.shipping import ShippingEndpoint

# Utility decorators
from .utils.logging import log_request, setup_logging
from .utils.rate_limiter import RateLimiter, rate_limit
from .utils.retry import RetryPolicy, retry
from .utils.webhooks import WebhookEvent, WebhookManager, WebhookPayload

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
