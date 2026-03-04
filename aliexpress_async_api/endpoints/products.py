"""
Products endpoint module
"""
from typing import Optional, List, Dict
from aliexpress_async_api.models import Product, ProductSearchResponse
from .base import BaseEndpoint


class ProductsEndpoint(BaseEndpoint):
    """Products endpoint methods"""
    
    async def search_products(
        self,
        keyword: str,
        page_no: int = 1,
        page_size: int = 20,
        sort: str = "SALE_PRICE_ASC",
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        tracking_id: Optional[str] = None,
        access_token: Optional[str] = None
    ) -> ProductSearchResponse:
        """
        Search for affiliate products
        
        Args:
            keyword: Search term
            page_no: Page number (default: 1)
            page_size: Results per page (default: 20)
            sort: Sort order (default: SALE_PRICE_ASC)
            target_currency: Currency code (default: BRL)
            target_language: Language code (default: PT)
            country: Country code (default: BR)
            tracking_id: Tracking ID for affiliate
            access_token: Optional auth token
        
        Returns:
            ProductSearchResponse with matched products
        """
        api_method = "aliexpress.affiliate.product.query"
        business = {
            "keywords": keyword,
            "page_no": str(page_no),
            "page_size": str(page_size),
            "sort": sort,
            "tracking_id": tracking_id or "",
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
                raw_data=p
            )
            for p in products_data
        ]
        
        return ProductSearchResponse(
            products=products,
            total_record_count=result.get("total_record_count", 0),
            current_record_count=result.get("current_record_count", 0),
            page_no=page_no,
            raw_data=raw
        )
    
    async def get_product_details(
        self,
        product_ids: List[str],
        fields: str = "product_id,product_title,product_main_image_url,sale_price,original_price,evaluate_rate,lastest_volume,promotion_link,shop_url",
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        tracking_id: Optional[str] = None,
        access_token: Optional[str] = None
    ) -> List[Product]:
        """
        Get details for specific products
        
        Args:
            product_ids: List of product IDs
            fields: Fields to retrieve
            target_currency: Currency code
            target_language: Language code
            country: Country code
            tracking_id: Tracking ID for affiliate
            access_token: Optional auth token
        
        Returns:
            List of Product objects with details
        
        Raises:
            ProductNotFoundException: If no products found
        """
        from aliexpress_async_api.exceptions import ProductNotFoundException
        
        api_method = "aliexpress.affiliate.productdetail.get"
        business = {
            "product_ids": ",".join(str(i) for i in product_ids),
            "fields": fields,
            "tracking_id": tracking_id or "",
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
                raw_data=p
            )
            for p in products_data
        ]
    
    async def smart_match_products(
        self,
        keywords: Optional[str] = None,
        product_id: Optional[str] = None,
        page_no: int = 1,
        page_size: int = 20,
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        tracking_id: Optional[str] = None,
        access_token: Optional[str] = None
    ) -> ProductSearchResponse:
        """Smart match products by keyword or ID"""
        api_method = "aliexpress.affiliate.product.smartmatch"
        business = {
            "page_no": str(page_no),
            "page_size": str(page_size),
            "tracking_id": tracking_id or "",
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
                raw_data=p
            )
            for p in products_data
        ]
        return ProductSearchResponse(
            products=products,
            total_record_count=result.get("total_record_count", 0),
            current_record_count=result.get("current_record_count", 0),
            page_no=page_no,
            raw_data=raw
        )
    
    async def get_hotproducts(
        self,
        category_ids: Optional[str] = None,
        page_no: int = 1,
        page_size: int = 20,
        target_currency: str = "BRL",
        target_language: str = "PT",
        country: str = "BR",
        tracking_id: Optional[str] = None,
        access_token: Optional[str] = None
    ) -> ProductSearchResponse:
        """Get hot/trending products"""
        api_method = "aliexpress.affiliate.hotproduct.query"
        business = {
            "page_no": str(page_no),
            "page_size": str(page_size),
            "tracking_id": tracking_id or "",
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
                raw_data=p
            )
            for p in products_data
        ]
        return ProductSearchResponse(
            products=products,
            total_record_count=result.get("total_record_count", 0),
            current_record_count=result.get("current_record_count", 0),
            page_no=page_no,
            raw_data=raw
        )
    
    async def get_hotproduct_download(
        self,
        category_id: str,
        access_token: Optional[str] = None
    ) -> Dict:
        """Download hot product data"""
        api_method = "aliexpress.affiliate.hotproduct.download"
        business = {"category_id": category_id}
        return await self.request(api_method, business, access_token)
