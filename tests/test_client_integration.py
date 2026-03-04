"""
Integration tests for AliExpressIOPClient
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
from aliexpress_async_api import AliExpressIOPClient
from aliexpress_async_api.models import ProductSearchResponse, Product
from aliexpress_async_api.exceptions import InvalidCredentialsException, APIRequestException


class TestAliExpressIOPClient:
    """Client initialization and basic tests"""
    
    def test_client_init_requires_credentials(self):
        """Test that client requires app_key and app_secret"""
        with pytest.raises(InvalidCredentialsException):
            AliExpressIOPClient(app_key="", app_secret="secret")
        
        with pytest.raises(InvalidCredentialsException):
            AliExpressIOPClient(app_key="key", app_secret="")
    
    def test_client_init_with_all_params(self):
        """Test client initialization with tracking_id"""
        client = AliExpressIOPClient(
            app_key="test_key",
            app_secret="test_secret",
            tracking_id="test_tracking"
        )
        assert client.auth.app_key == "test_key"
        assert client.tracking_id == "test_tracking"
    
    @pytest.mark.asyncio
    async def test_client_context_manager(self):
        """Test async context manager"""
        async with AliExpressIOPClient("key", "secret") as client:
            assert client._session is not None
    
    @pytest.mark.asyncio
    async def test_get_auth_url(self):
        """Test OAuth URL generation"""
        client = AliExpressIOPClient("key", "secret")
        url = client.get_auth_url("https://example.com/callback")
        
        assert "https://auth.aliexpress.com/oauth/authorize" in url
        assert "client_id=key" in url
        assert "redirect_uri=" in url
    
    @pytest.mark.asyncio
    async def test_search_products_response_structure(self):
        """Test search_products returns correct structure"""
        with patch.object(AliExpressIOPClient, 'request') as mock_request:
            mock_request.return_value = {
                "aliexpress_affiliate_product_query_response": {
                    "resp_result": {
                        "result": {
                            "total_record_count": 100,
                            "current_record_count": 1,
                            "products": {
                                "product": [
                                    {
                                        "product_id": 123,
                                        "product_title": "Test Product",
                                        "product_main_image_url": "http://example.com/img.jpg",
                                        "sale_price": "10.00",
                                        "original_price": "20.00",
                                        "promotion_link": "http://affiliate.link"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
            
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.search_products("test")
                
                assert isinstance(result, ProductSearchResponse)
                assert result.total_record_count == 100
                assert len(result.products) == 1
                assert result.products[0].product_title == "Test Product"
    
    @pytest.mark.asyncio
    async def test_check_error_handling(self):
        """Test error response handling"""
        async with AliExpressIOPClient("key", "secret") as client:
            with pytest.raises(APIRequestException):
                client._check_error({
                    "error_response": {
                        "code": "ERROR_CODE",
                        "msg": "Test error message",
                        "sub_code": "SUB_CODE"
                    }
                })
    
    @pytest.mark.asyncio
    async def test_check_error_with_invalid_response_type(self):
        """Test error handling with invalid response type"""
        async with AliExpressIOPClient("key", "secret") as client:
            with pytest.raises(APIRequestException):
                client._check_error("invalid response")
    
    @pytest.mark.asyncio
    async def test_get_product_details_error_handling(self):
        """Test get_product_details with no results"""
        with patch.object(AliExpressIOPClient, 'request') as mock_request:
            mock_request.return_value = {
                "aliexpress_affiliate_productdetail_get_response": {
                    "resp_result": {
                        "result": {
                            "products": {
                                "product": []
                            }
                        }
                    }
                }
            }
            
            async with AliExpressIOPClient("key", "secret") as client:
                from aliexpress_async_api.exceptions import ProductNotFoundException
                with pytest.raises(ProductNotFoundException):
                    await client.get_product_details(["invalid_id"])


class TestEndpointSignatures:
    """Test that all endpoints can be called with proper signatures"""
    
    @pytest.mark.asyncio
    async def test_all_endpoints_exist(self):
        """Test that all documented endpoints exist as methods"""
        async with AliExpressIOPClient("key", "secret") as client:
            # Product endpoints
            assert hasattr(client, 'search_products')
            assert hasattr(client, 'get_product_details')
            assert hasattr(client, 'smart_match_products')
            assert hasattr(client, 'get_hotproducts')
            assert hasattr(client, 'get_hotproduct_download')
            
            # Category endpoints
            assert hasattr(client, 'get_categories')
            assert hasattr(client, 'get_featured_promo')
            assert hasattr(client, 'get_featured_promo_products')
            
            # Link endpoints
            assert hasattr(client, 'generate_affiliate_link')
            
            # Shipping endpoints
            assert hasattr(client, 'get_shipping_info')
            assert hasattr(client, 'get_sku_detail')
            
            # Order endpoints
            assert hasattr(client, 'get_order_list')
            assert hasattr(client, 'get_order_list_by_index')
            assert hasattr(client, 'get_order_info')
            
            # Auth endpoints
            assert hasattr(client, 'get_token')
            assert hasattr(client, 'refresh_token')
