"""
Affiliates endpoint implementation
"""

from typing import Optional

from aliexpress_async_api.endpoints.base import BaseEndpoint
from aliexpress_async_api.models.affiliate import AffiliateLink


class AffiliatesEndpoint(BaseEndpoint):
    """Endpoint for affiliate link generation"""

    async def generate_affiliate_link(
        self,
        promotion_link_type: int = 0,
        source_values: Optional[str] = None,
        track_id: Optional[str] = None,
        **kwargs,
    ) -> AffiliateLink:
        """
        Generate affiliate tracking link for a product

        Args:
            promotion_link_type: Link type (0=text, 1=image)
            source_values: Comma-separated product IDs or URLs
            track_id: Custom tracking ID
            **kwargs: Additional parameters

        Returns:
            AffiliateLink: Generated tracking link
        """
        params = {
            "fields": "promotion_link_code",
            "promotion_link_type": promotion_link_type,
            **kwargs,
        }

        if source_values:
            params["source_values"] = source_values

        if track_id:
            params["track_id"] = track_id

        response = await self.request("aliexpress.affiliate.link.generate", params)

        link_data = response.get("promotion_links", {}).get("promotion_link", {})
        if isinstance(link_data, list):
            link_data = link_data[0] if link_data else {}

        return AffiliateLink(
            promotion_link=link_data.get("promotion_link", ""),
            source_value=source_values or "",
            raw_data=link_data,
        )
