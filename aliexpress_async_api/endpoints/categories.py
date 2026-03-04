"""
Categories endpoint implementation
"""
from typing import Dict, Any, List, Optional
from aliexpress_async_api.models.category import Category, PromoInfo
from aliexpress_async_api.endpoints.base import BaseEndpoint


class CategoriesEndpoint(BaseEndpoint):
    """Endpoint for category-related operations"""
    
    async def get_categories(
        self,
        language: str = "en",
        **kwargs
    ) -> List[Category]:
        """
        Get product categories
        
        Args:
            language: Language code (default: "en")
            **kwargs: Additional parameters
        
        Returns:
            List[Category]: List of category objects
        """
        params = {
            "fields": "commission_rate,category_id,category_name",
            "language": language,
            **kwargs
        }
        
        response = await self.request(
            "aliexpress.affiliate.category.get",
            params
        )
        
        categories_data = response.get("categories", {}).get("category", [])
        if not isinstance(categories_data, list):
            categories_data = [categories_data] if categories_data else []
        
        return [
            Category(
                category_id=cat.get("category_id"),
                category_name=cat.get("category_name"),
                parent_category_id=cat.get("parent_category_id"),
                raw_data=cat
            )
            for cat in categories_data
        ]
    
    async def get_featured_promo(
        self,
        page_no: int = 1,
        page_size: int = 100,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get featured promotions
        
        Args:
            page_no: Page number
            page_size: Results per page
            **kwargs: Additional parameters
        
        Returns:
            Dict containing promotion list
        """
        params = {
            "fields": "main_pic,promo_id,promo_name,promo_desc",
            "page_no": page_no,
            "page_size": page_size,
            **kwargs
        }
        
        response = await self.request(
            "aliexpress.affiliate.promo.featured.get",
            params
        )
        
        return response.get("promos", {})
    
    async def get_featured_promo_products(
        self,
        promo_id: str,
        page_no: int = 1,
        page_size: int = 100,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Get products for a featured promotion
        
        Args:
            promo_id: Promotion ID
            page_no: Page number
            page_size: Results per page
            **kwargs: Additional parameters
        
        Returns:
            List of product data
        """
        params = {
            "fields": "sale_price,product_id,product_title",
            "promo_id": promo_id,
            "page_no": page_no,
            "page_size": page_size,
            **kwargs
        }
        
        response = await self.request(
            "aliexpress.affiliate.promo.product.list",
            params
        )
        
        products = response.get("products", {}).get("product", [])
        return products if isinstance(products, list) else [products] if products else []
