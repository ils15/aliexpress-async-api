"""
Tests for products endpoint module
"""
import pytest
from unittest.mock import patch, AsyncMock
from typing import Dict, Any
from aliexpress_async_api.endpoints.products import ProductsEndpoint
from aliexpress_async_api.models import Product, ProductSearchResponse


class TestProductsEndpoint:
    """Test ProductsEndpoint module"""
    
    def test_products_endpoint_instantiation(self):
        """Test that ProductsEndpoint can be instantiated"""
        async_mock = AsyncMock()
        endpoint = ProductsEndpoint(async_mock)
        assert endpoint.request == async_mock
    
    @pytest.mark.asyncio
    async def test_search_products_delegates_to_request(self):
        """Test search_products calls request with correct params"""
        mock_request = AsyncMock(return_value={
            "aliexpress_affiliate_product_query_response": {
                "resp_result": {
                    "result": {
                        "total_record_count": 1,
                        "current_record_count": 1,
                        "products": {"product": []}
                    }
                }
            }
        })
        
        endpoint = ProductsEndpoint(mock_request)
        result = await endpoint.search_products(
            keyword="test",
            tracking_id="track123"
        )
        
        assert isinstance(result, ProductSearchResponse)
        mock_request.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_product_details_returns_list(self):
        """Test get_product_details returns list of Products"""
        mock_request = AsyncMock(return_value={
            "aliexpress_affiliate_productdetail_get_response": {
                "resp_result": {
                    "result": {
                        "products": {
                            "product": [
                                {
                                    "product_id": 123,
                                    "product_title": "Test",
                                    "product_main_image_url": "http://image.url",
                                    "sale_price": "10.00",
                                    "original_price": "20.00",
                                    "promotion_link": "http://promo.link"
                                }
                            ]
                        }
                    }
                }
            }
        })
        
        endpoint = ProductsEndpoint(mock_request)
        result = await endpoint.get_product_details(
            product_ids=["123"],
            tracking_id="track123"
        )
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Product)


class TestOrdersEndpoint:
    """Test OrdersEndpoint module"""
    
    def test_orders_endpoint_instantiation(self):
        """Test that OrdersEndpoint can be instantiated"""
        async_mock = AsyncMock()
        from aliexpress_async_api.endpoints.orders import OrdersEndpoint
        endpoint = OrdersEndpoint(async_mock)
        assert endpoint.request == async_mock
    
    @pytest.mark.asyncio
    async def test_get_order_list_returns_list(self):
        """Test get_order_list returns list of Orders"""
        mock_request = AsyncMock(return_value={
            "aliexpress_affiliate_order_list_response": {
                "resp_result": {
                    "result": {
                        "orders": {"order": []}
                    }
                }
            }
        })
        
        from aliexpress_async_api.endpoints.orders import OrdersEndpoint
        from aliexpress_async_api.models import Order
        
        endpoint = OrdersEndpoint(mock_request)
        result = await endpoint.get_order_list(
            start_time="2026-01-01",
            end_time="2026-12-31"
        )
        
        assert isinstance(result, list)


class TestEndpointIntegration:
    """Test that client uses endpoint modules"""
    
    @pytest.mark.asyncio
    async def test_client_products_endpoint_integration(self):
        """Test that client.search_products uses products endpoint"""
        from aliexpress_async_api import AliExpressIOPClient
        
        mock_response = {
            "aliexpress_affiliate_product_query_response": {
                "resp_result": {
                    "result": {
                        "total_record_count": 0,
                        "current_record_count": 0,
                        "products": {"product": []}
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret", tracking_id="track123") as client:
                result = await client.search_products("test")
                assert isinstance(result, ProductSearchResponse)
