import logging
import urllib.parse
from typing import Any, Dict, List, Optional

import aiohttp

from .auth import AliExpressAuth
from .exceptions import (
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

logger = logging.getLogger(__name__)


class AliExpressIOPClient:
    """
    Asynchronous AliExpress IOP Affiliate API Client.
    """

    BASE_URL = "https://api-sg.aliexpress.com/sync"

    def __init__(
        self, app_key: str, app_secret: str, tracking_id: Optional[str] = None
    ):
        """
        Initializes the client with your AliExpress Open Platform credentials.
        """
        if not app_key or not app_secret:
            raise InvalidCredentialsException("app_key and app_secret are required.")

        self.auth = AliExpressAuth(app_key, app_secret)
        self.tracking_id = tracking_id
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def close(self):
        """Explicitly close the HTTP session."""
        if self._session:
            await self._session.close()

    def get_auth_url(
        self,
        redirect_uri: str,
        state: str = "aliexpress_oauth",
        view: str = "web",
    ) -> str:
        """
        Returns the OAuth authorization URL.
        """
        params = {
            "client_id": self.auth.app_key,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "view": view,
            "state": state,
        }
        return "https://auth.aliexpress.com/oauth/authorize?" + urllib.parse.urlencode(
            params
        )

    async def request(
        self,
        api_method: str,
        business_params: Dict[str, str],
        access_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Makes an authenticated API request using the V1 MD5 signature.
        """
        if not self._session:
            self._session = aiohttp.ClientSession()

        sys_params = self.auth.build_system_params(api_method, session=access_token)
        sys_params["sign"] = self.auth.sign(sys_params, business_params)

        headers = {
            "Content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }

        async with self._session.post(
            self.BASE_URL, params=sys_params, data=business_params, headers=headers
        ) as response:
            raw = await response.json(content_type=None)
            self._check_error(raw)
            return raw

    def _check_error(self, raw: Any):
        if not isinstance(raw, dict):
            raise APIRequestException(f"Unexpected response type: {type(raw)}")

        if "error_response" in raw:
            err = raw["error_response"]
            raise APIRequestException(
                message=err.get("msg", "Unknown error"),
                code=err.get("code"),
                sub_code=err.get("sub_code"),
            )

    # ── API Methods ────────────────────────────────────────────────────────────

    async def search_products(
        self,
        keyword: str,
        page_no: int = 1,
        page_size: int = 20,
        sort: str = "SALE_PRICE_ASC",
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        access_token: Optional[str] = None,
    ) -> ProductSearchResponse:
        """
        Searches for affiliate products.
        """
        api_method = "aliexpress.affiliate.product.query"
        business = {
            "keywords": keyword,
            "page_no": str(page_no),
            "page_size": str(page_size),
            "sort": sort,
            "tracking_id": self.tracking_id or "",
            "target_currency": target_currency,
            "target_language": target_language,
            "country": country,
        }

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_product_query_response", {})
        result = resp.get("resp_result", {}).get("result", {})

        products_data = result.get("products", {}).get("product", [])

        products = [
            Product(
                **{k: v for k, v in p.items() if k in Product.__annotations__},
                raw_data=p,
            )
            for p in products_data
        ]

        return ProductSearchResponse(
            products=products,
            total_record_count=result.get("total_record_count", 0),
            current_record_count=result.get("current_record_count", 0),
            page_no=page_no,
            raw_data=raw,
        )

    # Alias for user's test script
    async def query_products(self, *args, **kwargs) -> ProductSearchResponse:
        """Alias for search_products to match test script."""
        # Map keywords to keyword
        if "keywords" in kwargs:
            kwargs["keyword"] = kwargs.pop("keywords")
        # Ignore unsupported args in test script gracefully
        kwargs.pop("category_ids", None)
        return await self.search_products(*args, **kwargs)

    async def get_product_details(
        self,
        product_ids: List[str],
        fields: str = "product_id,product_title,product_main_image_url,sale_price,original_price,evaluate_rate,lastest_volume,promotion_link,shop_url",
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        access_token: Optional[str] = None,
    ) -> List[Product]:
        """
        Gets detailed information about specific affiliate products.
        """
        api_method = "aliexpress.affiliate.productdetail.get"
        business = {
            "product_ids": ",".join(str(i) for i in product_ids),
            "fields": fields,
            "tracking_id": self.tracking_id or "",
            "target_currency": target_currency,
            "target_language": target_language,
            "country": country,
        }

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_productdetail_get_response", {})
        result = resp.get("resp_result", {}).get("result", {})

        products_data = result.get("products", {}).get("product", [])
        if not products_data:
            raise ProductNotFoundException("No products found for the given IDs.")

        return [
            Product(
                **{k: v for k, v in p.items() if k in Product.__annotations__},
                raw_data=p,
            )
            for p in products_data
        ]

    # Alias for user's test script
    async def get_product_detail(self, *args, **kwargs) -> List[Product]:
        """Alias for get_product_details to match test script."""
        return await self.get_product_details(*args, **kwargs)

    async def generate_affiliate_link(
        self,
        source_values: str,
        promotion_link_type: int = 0,
        access_token: Optional[str] = None,
    ) -> List[AffiliateLink]:
        """
        Generates trackable affiliate links.
        """
        api_method = "aliexpress.affiliate.link.generate"
        business = {
            "source_values": source_values,
            "promotion_link_type": str(promotion_link_type),
            "tracking_id": self.tracking_id or "",
        }

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_link_generate_response", {})
        links_data = (
            resp.get("resp_result", {})
            .get("result", {})
            .get("promotion_links", {})
            .get("promotion_link", [])
        )

        return [
            AffiliateLink(
                promotion_link=l.get("promotion_link", ""),
                source_value=l.get("source_value", ""),
                raw_data=l,
            )
            for l in links_data
        ]

    async def generate_affiliate_links(
        self,
        promotion_links: List[str],
        tracking_id: Optional[str] = None,
        promotion_link_type: int = 0,
        access_token: Optional[str] = None,
    ) -> List[AffiliateLink]:
        """Alias wrapper to handle list of links from test script directly."""
        source_values = ",".join(promotion_links)
        # Temporarily use specific tracking ID if provided via args
        old_tid = self.tracking_id
        if tracking_id:
            self.tracking_id = tracking_id
        try:
            return await self.generate_affiliate_link(
                source_values, promotion_link_type, access_token
            )
        finally:
            self.tracking_id = old_tid

    async def get_token(self, code: str) -> TokenResponse:
        """
        Exchanges an OAuth code for an access token.
        """
        api_method = "aliexpress.auth.token.create"
        raw = await self.request(api_method, {"code": code})

        return TokenResponse(
            access_token=raw.get("access_token", ""),
            refresh_token=raw.get("refresh_token", ""),
            expire_time=raw.get("expire_time", 0),
            account=raw.get("account", ""),
            raw_data=raw,
        )

    async def refresh_token(self, refresh_token_value: str) -> TokenResponse:
        """
        Refreshes an expired access token.
        """
        api_method = "aliexpress.auth.token.refresh"
        raw = await self.request(api_method, {"refresh_token": refresh_token_value})

        return TokenResponse(
            access_token=raw.get("access_token", ""),
            refresh_token=raw.get("refresh_token", ""),
            expire_time=raw.get("expire_time", 0),
            account=raw.get("account", ""),
            raw_data=raw,
        )

    # ── New Endpoints to Implement ──────────────────────────────────────

    async def smart_match_products(
        self,
        keywords: Optional[str] = None,
        product_id: Optional[str] = None,
        page_no: int = 1,
        page_size: int = 20,
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        access_token: Optional[str] = None,
    ) -> ProductSearchResponse:
        """aliexpress.affiliate.product.smartmatch"""
        api_method = "aliexpress.affiliate.product.smartmatch"
        business = {
            "page_no": str(page_no),
            "page_size": str(page_size),
            "tracking_id": self.tracking_id or "",
            "target_currency": target_currency,
            "target_language": target_language,
            "country": country,
        }
        if keywords:
            business["keywords"] = keywords
        if product_id:
            business["product_id"] = product_id

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_product_smartmatch_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        products_data = result.get("products", {}).get("product", [])

        products = [
            Product(
                **{k: v for k, v in p.items() if k in Product.__annotations__},
                raw_data=p,
            )
            for p in products_data
        ]
        return ProductSearchResponse(
            products=products,
            total_record_count=result.get("total_record_count", 0),
            current_record_count=result.get("current_record_count", 0),
            page_no=page_no,
            raw_data=raw,
        )

    async def get_hotproducts(
        self,
        category_ids: Optional[str] = None,
        page_no: int = 1,
        page_size: int = 20,
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        access_token: Optional[str] = None,
    ) -> ProductSearchResponse:
        """aliexpress.affiliate.hotproduct.query"""
        api_method = "aliexpress.affiliate.hotproduct.query"
        business = {
            "page_no": str(page_no),
            "page_size": str(page_size),
            "tracking_id": self.tracking_id or "",
            "target_currency": target_currency,
            "target_language": target_language,
            "country": country,
        }
        if category_ids:
            business["category_ids"] = category_ids

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_hotproduct_query_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        products_data = result.get("products", {}).get("product", [])

        products = [
            Product(
                **{k: v for k, v in p.items() if k in Product.__annotations__},
                raw_data=p,
            )
            for p in products_data
        ]
        return ProductSearchResponse(
            products=products,
            total_record_count=result.get("total_record_count", 0),
            current_record_count=result.get("current_record_count", 0),
            page_no=page_no,
            raw_data=raw,
        )

    async def get_hotproduct_download(
        self, category_id: str, access_token: Optional[str] = None
    ) -> Dict:
        """aliexpress.affiliate.hotproduct.download"""
        api_method = "aliexpress.affiliate.hotproduct.download"
        business = {
            "category_id": category_id,
        }
        raw = await self.request(api_method, business, access_token)
        return raw

    async def get_categories(
        self, access_token: Optional[str] = None
    ) -> List[Category]:
        """aliexpress.affiliate.category.get"""
        api_method = "aliexpress.affiliate.category.get"
        business = {}
        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_category_get_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        cats_data = result.get("categories", {}).get("category", [])

        return [
            Category(
                **{k: v for k, v in c.items() if k in Category.__annotations__},
                raw_data=c,
            )
            for c in cats_data
        ]

    async def get_featured_promo(
        self, access_token: Optional[str] = None
    ) -> List[PromoInfo]:
        """aliexpress.affiliate.featuredpromo.get"""
        api_method = "aliexpress.affiliate.featuredpromo.get"
        business = {}
        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_featuredpromo_get_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        promos_data = result.get("promos", {}).get("promo", [])

        return [
            PromoInfo(
                **{k: v for k, v in p.items() if k in PromoInfo.__annotations__},
                raw_data=p,
            )
            for p in promos_data
        ]

    async def get_featured_promo_products(
        self,
        promotion_name: Optional[str] = None,
        page_no: int = 1,
        page_size: int = 20,
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        access_token: Optional[str] = None,
    ) -> ProductSearchResponse:
        """aliexpress.affiliate.featuredpromo.products.get"""
        api_method = "aliexpress.affiliate.featuredpromo.products.get"
        business = {
            "page_no": str(page_no),
            "page_size": str(page_size),
            "tracking_id": self.tracking_id or "",
            "target_currency": target_currency,
            "target_language": target_language,
            "country": country,
        }
        if promotion_name:
            business["promotion_name"] = promotion_name

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_featuredpromo_products_get_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        products_data = result.get("products", {}).get("product", [])

        products = [
            Product(
                **{k: v for k, v in p.items() if k in Product.__annotations__},
                raw_data=p,
            )
            for p in products_data
        ]
        return ProductSearchResponse(
            products=products,
            total_record_count=result.get("total_record_count", 0),
            current_record_count=result.get("current_record_count", 0),
            page_no=page_no,
            raw_data=raw,
        )

    async def get_shipping_info(
        self,
        product_id: str,
        target_sale_price: str,
        tax_rate: str = "0.00",
        sku_id: str = "",
        target_language: str = "PT",
        target_currency: str = "BRL",
        send_goods_country_code: str = "CN",
        ship_to_country: str = "BR",
        access_token: Optional[str] = None,
    ) -> ShippingInfo:
        """aliexpress.affiliate.product.shipping.get"""
        api_method = "aliexpress.affiliate.product.shipping.get"
        business = {
            "product_id": str(product_id),
            "target_sale_price": target_sale_price,
            "tax_rate": tax_rate,
            "sku_id": sku_id,
            "target_language": target_language,
            "target_currency": target_currency,
            "send_goods_country_code": send_goods_country_code,
            "ship_to_country": ship_to_country,
        }
        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_product_shipping_get_response", {})
        result = resp.get("resp_result", {}).get("result", {}).get("shipping_info", {})

        return ShippingInfo(
            estimated_delivery_time=result.get("estimated_delivery_time", ""),
            freight=result.get("freight", ""),
            tracking_available=result.get("tracking_available", ""),
            raw_data=result,
        )

    async def get_sku_detail(
        self,
        product_id: str,
        target_currency: str = "BRL",
        target_language: str = "PT",
        ship_to_country: str = "BR",
        access_token: Optional[str] = None,
    ) -> List[SKUInfo]:
        """aliexpress.affiliate.product.sku.detail.get"""
        api_method = "aliexpress.affiliate.product.sku.detail.get"
        business = {
            "product_id": str(product_id),
            "target_currency": target_currency,
            "target_language": target_language,
            "ship_to_country": ship_to_country,
        }
        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_product_sku_detail_get_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        skus_data = result.get("skus", {}).get("sku", [])

        return [
            SKUInfo(
                **{k: v for k, v in s.items() if k in SKUInfo.__annotations__},
                raw_data=s,
            )
            for s in skus_data
        ]

    async def get_order_list(
        self,
        start_time: str,
        end_time: str,
        status: str = "Completed",
        page_no: int = 1,
        page_size: int = 20,
        access_token: Optional[str] = None,
    ) -> List[Order]:
        """aliexpress.affiliate.order.list"""
        api_method = "aliexpress.affiliate.order.list"
        business = {
            "start_time": start_time,
            "end_time": end_time,
            "status": status,
            "page_no": str(page_no),
            "page_size": str(page_size),
        }

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_order_list_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        orders_data = result.get("orders", {}).get("order", [])

        return [
            Order(
                **{k: v for k, v in o.items() if k in Order.__annotations__}, raw_data=o
            )
            for o in orders_data
        ]

    async def get_order_list_by_index(
        self,
        start_query_index_id: str,
        start_time: str,
        end_time: str,
        time_type: str = "payment_time",
        status: str = "Completed",
        page_size: int = 20,
        access_token: Optional[str] = None,
    ) -> List[Order]:
        """aliexpress.affiliate.order.listbyindex"""
        api_method = "aliexpress.affiliate.order.listbyindex"
        business = {
            "start_query_index_id": str(start_query_index_id),
            "start_time": start_time,
            "end_time": end_time,
            "time_type": time_type,
            "status": status,
            "page_size": str(page_size),
        }

        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_order_listbyindex_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        orders_data = result.get("orders", {}).get("order", [])

        return [
            Order(
                **{k: v for k, v in o.items() if k in Order.__annotations__}, raw_data=o
            )
            for o in orders_data
        ]

    async def get_order_info(
        self, order_ids: List[str], access_token: Optional[str] = None
    ) -> List[Order]:
        """aliexpress.affiliate.order.get"""
        api_method = "aliexpress.affiliate.order.get"
        business = {"order_ids": ",".join(str(i) for i in order_ids)}
        raw = await self.request(api_method, business, access_token)
        resp = raw.get("aliexpress_affiliate_order_get_response", {})
        result = resp.get("resp_result", {}).get("result", {})
        orders_data = result.get("orders", {}).get("order", [])

        return [
            Order(
                **{k: v for k, v in o.items() if k in Order.__annotations__}, raw_data=o
            )
            for o in orders_data
        ]

    async def inquire_business_license(
        self, merchant_item_id: str, access_token: Optional[str] = None
    ) -> Dict:
        """/aliexpress/xinghe/merchant/license/get"""
        api_method = "/aliexpress/xinghe/merchant/license/get"
        business = {"merchant_item_id": merchant_item_id}
        return await self.request(api_method, business, access_token)
