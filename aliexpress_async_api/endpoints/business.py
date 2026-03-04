"""
Business endpoint implementation (seller business info queries)
"""
from typing import Dict, Any
from aliexpress_async_api.endpoints.base import BaseEndpoint


class BusinessEndpoint(BaseEndpoint):
    """Endpoint for business/seller information queries"""
    
    async def inquire_business_license(
        self,
        seller_user_id: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Inquire seller business license information
        
        Args:
            seller_user_id: Seller user ID
            **kwargs: Additional parameters
        
        Returns:
            Dict: Business license information
        """
        params = {
            "seller_user_id": seller_user_id,
            **kwargs
        }
        
        response = await self.request(
            "aliexpress.seller.inquiry.business.license",
            params
        )
        
        return response.get("business_license_info", {})
