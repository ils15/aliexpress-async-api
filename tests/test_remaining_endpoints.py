"""
Tests for remaining endpoint modules (categories, shipping, affiliates, auth, business)
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from aliexpress_async_api.endpoints.affiliates import AffiliatesEndpoint
from aliexpress_async_api.endpoints.auth import AuthEndpoint
from aliexpress_async_api.endpoints.business import BusinessEndpoint
from aliexpress_async_api.endpoints.categories import CategoriesEndpoint
from aliexpress_async_api.endpoints.shipping import ShippingEndpoint


class TestCategoriesEndpoint:
    """Tests for CategoriesEndpoint"""

    @pytest.mark.asyncio
    async def test_get_categories(self):
        """Test getting product categories"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "categories": {
                "category": [
                    {"category_id": 1, "category_name": "Electronics"},
                    {"category_id": 2, "category_name": "Fashion"},
                ]
            }
        }

        endpoint = CategoriesEndpoint(mock_request)
        result = await endpoint.get_categories()

        assert len(result) == 2
        assert result[0].category_id == 1
        assert result[0].category_name == "Electronics"

    @pytest.mark.asyncio
    async def test_get_featured_promo(self):
        """Test getting featured promotions"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "promos": {"promotion": [{"promo_id": "p1", "promo_name": "Summer Sale"}]}
        }

        endpoint = CategoriesEndpoint(mock_request)
        result = await endpoint.get_featured_promo()

        assert isinstance(result, dict)
        mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_featured_promo_products(self):
        """Test getting products for promotion"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "products": {
                "product": [{"product_id": 123, "product_title": "Test Product"}]
            }
        }

        endpoint = CategoriesEndpoint(mock_request)
        result = await endpoint.get_featured_promo_products("p1")

        assert len(result) == 1
        assert result[0]["product_id"] == 123


class TestShippingEndpoint:
    """Tests for ShippingEndpoint"""

    @pytest.mark.asyncio
    async def test_get_shipping_info(self):
        """Test getting shipping information"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "result": {
                "delivery_time": "5-10 days",
                "shipping_fee": "5.00",
                "currency": "USD",
            }
        }

        endpoint = ShippingEndpoint(mock_request)
        result = await endpoint.get_shipping_info(12345)

        assert result.estimated_delivery_time == "5-10 days"
        assert result.freight == "5.00"

    @pytest.mark.asyncio
    async def test_get_sku_detail(self):
        """Test getting SKU details"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "products": {
                "product": [
                    {
                        "skuPriceList": {
                            "skuPrice": [
                                {
                                    "sku_id": "sku1",
                                    "propId": "color",
                                    "originalPrice": "10.00",
                                    "discountPrice": "8.00",
                                }
                            ]
                        }
                    }
                ]
            }
        }

        endpoint = ShippingEndpoint(mock_request)
        result = await endpoint.get_sku_detail(12345)

        assert len(result) == 1
        assert result[0].sku_id == "sku1"
        assert result[0].sku_price == "10.00"


class TestAffiliatesEndpoint:
    """Tests for AffiliatesEndpoint"""

    @pytest.mark.asyncio
    async def test_generate_affiliate_link(self):
        """Test generating affiliate link"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "promotion_links": {
                "promotion_link": {
                    "promotion_link": "https://tracking.example.com/abc123",
                    "track_id": "abc123",
                }
            }
        }

        endpoint = AffiliatesEndpoint(mock_request)
        result = await endpoint.generate_affiliate_link(source_values="123,456")

        assert result.promotion_link == "https://tracking.example.com/abc123"
        assert result.source_value == "123,456"

    @pytest.mark.asyncio
    async def test_generate_affiliate_link_with_track_id(self):
        """Test generating affiliate link with custom tracking ID"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "promotion_links": {
                "promotion_link": {
                    "promotion_link": "https://tracking.example.com/custom",
                    "track_id": "custom_id",
                }
            }
        }

        endpoint = AffiliatesEndpoint(mock_request)
        result = await endpoint.generate_affiliate_link(
            source_values="123", track_id="custom_id"
        )

        assert result.source_value == "123"


class TestAuthEndpoint:
    """Tests for AuthEndpoint"""

    @pytest.mark.asyncio
    async def test_get_token(self):
        """Test exchanging auth code for token"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "access_token_response": {
                "access_token": "token123",
                "expires_in": 3600,
                "refresh_token": "refresh123",
                "account": "user@example.com",
            }
        }

        endpoint = AuthEndpoint(mock_request)
        result = await endpoint.get_token("auth_code_123")

        assert result.access_token == "token123"
        assert result.expire_time == 3600
        assert result.refresh_token == "refresh123"

    @pytest.mark.asyncio
    async def test_refresh_token(self):
        """Test refreshing access token"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "access_token_response": {
                "access_token": "new_token456",
                "expires_in": 3600,
                "refresh_token": "refresh456",
                "account": "user@example.com",
            }
        }

        endpoint = AuthEndpoint(mock_request)
        result = await endpoint.refresh_token("old_refresh_token")

        assert result.access_token == "new_token456"
        assert result.refresh_token == "refresh456"


class TestBusinessEndpoint:
    """Tests for BusinessEndpoint"""

    @pytest.mark.asyncio
    async def test_inquire_business_license(self):
        """Test querying business license info"""
        mock_request = AsyncMock()
        mock_request.return_value = {
            "business_license_info": {
                "seller_id": 12345,
                "license_status": "verified",
                "license_number": "ABC123",
            }
        }

        endpoint = BusinessEndpoint(mock_request)
        result = await endpoint.inquire_business_license(12345)

        assert result["license_status"] == "verified"
        assert result["seller_id"] == 12345


class TestEndpointIntegration:
    """Integration tests for all endpoint modules"""

    @pytest.mark.asyncio
    async def test_all_endpoints_instantiation(self):
        """Test that all endpoint classes can be instantiated"""
        mock_request = AsyncMock()

        endpoints = [
            CategoriesEndpoint(mock_request),
            ShippingEndpoint(mock_request),
            AffiliatesEndpoint(mock_request),
            AuthEndpoint(mock_request),
            BusinessEndpoint(mock_request),
        ]

        assert len(endpoints) == 5
        assert all(hasattr(ep, "request") for ep in endpoints)
