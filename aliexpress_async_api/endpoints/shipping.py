"""
Shipping endpoint implementation
"""
from typing import Dict, Any, List
from aliexpress_async_api.models.shipping import ShippingInfo, SKUInfo
from aliexpress_async_api.endpoints.base import BaseEndpoint


class ShippingEndpoint(BaseEndpoint):
    """Endpoint for shipping-related operations"""
    
    async def get_shipping_info(
        self,
        product_id: int,
        country_code: str = "US",
        **kwargs
    ) -> ShippingInfo:
        """
        Get shipping information for a product
        
        Args:
            product_id: Product ID
            country_code: Destination country code
            **kwargs: Additional parameters
        
        Returns:
            ShippingInfo: Shipping details
        """
        params = {
            "fields": "delivery_time,shipping_fee,shipping_fcl",
            "product_id": product_id,
            "country_code": country_code,
            **kwargs
        }
        
        response = await self.request(
            "aliexpress.affiliate.shipping.get",
            params
        )
        
        shipping_data = response.get("result", {})
        
        return ShippingInfo(
            estimated_delivery_time=shipping_data.get("delivery_time", ""),
            freight=shipping_data.get("shipping_fee", ""),
            tracking_available=shipping_data.get("currency", ""),
            raw_data=shipping_data
        )
    
    async def get_sku_detail(
        self,
        product_id: int,
        skill_id: str = "",
        **kwargs
    ) -> List[SKUInfo]:
        """
        Get SKU (variant) details for a product
        
        Args:
            product_id: Product ID
            skill_id: Specific SKU ID (optional)
            **kwargs: Additional parameters
        
        Returns:
            List[SKUInfo]: List of variant information
        """
        params = {
            "fields": "sku_id,propId,sku_code,original_price,discount_price",
            "product_id": product_id,
            **kwargs
        }
        
        if skill_id:
            params["skill_id"] = skill_id
        
        response = await self.request(
            "aliexpress.affiliate.sku.detail.get",
            params
        )
        
        skus_data = response.get("products", {}).get("product", [])
        if not isinstance(skus_data, list):
            skus_data = [skus_data] if skus_data else []
        
        result = []
        for sku in skus_data:
            sku_items = sku.get("skuPriceList", {}).get("skuPrice", [])
            if not isinstance(sku_items, list):
                sku_items = [sku_items] if sku_items else []
            
            for item in sku_items:
                result.append(
                    SKUInfo(
                        sku_id=item.get("sku_id", ""),
                        sku_attr=item.get("propId", ""),
                        sku_price=item.get("originalPrice", ""),
                        sku_stock=item.get("discountPrice", ""),
                        raw_data=item
                    )
                )
        
        return result
