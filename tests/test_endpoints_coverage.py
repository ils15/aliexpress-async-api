"""
Endpoint method tests with mocks - covers all 14+ endpoints
"""
import pytest
from unittest.mock import AsyncMock, patch
from aliexpress_async_api import AliExpressIOPClient
from aliexpress_async_api.models import (
    Order, Category, PromoInfo, ShippingInfo, SKUInfo, AffiliateLink
)


class TestOrderEndpoints:
    """Test order-related endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_order_list(self):
        """Test get_order_list endpoint"""
        mock_response = {
            "aliexpress_affiliate_order_list_response": {
                "resp_result": {
                    "result": {
                        "orders": {
                            "order": [
                                {
                                    "order_id": 123,
                                    "order_status": "Completed",
                                    "order_time": "2026-01-01",
                                    "estimated_commission": "10.00",
                                    "product_title": "Test",
                                    "product_count": 1,
                                    "product_price": "100.00"
                                }
                            ]
                        }
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_order_list("2026-01-01", "2026-12-31")
                assert isinstance(result, list)
                assert len(result) > 0
                assert isinstance(result[0], Order)
    
    @pytest.mark.asyncio
    async def test_get_order_list_by_index(self):
        """Test get_order_list_by_index endpoint"""
        mock_response = {
            "aliexpress_affiliate_order_listbyindex_response": {
                "resp_result": {
                    "result": {
                        "orders": {"order": []}
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_order_list_by_index(
                    "0", "2026-01-01", "2026-12-31"
                )
                assert isinstance(result, list)
    
    @pytest.mark.asyncio
    async def test_get_order_info(self):
        """Test get_order_info endpoint"""
        mock_response = {
            "aliexpress_affiliate_order_get_response": {
                "resp_result": {
                    "result": {
                        "orders": {"order": []}
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_order_info(["123"])
                assert isinstance(result, list)


class TestCategoryEndpoints:
    """Test category endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_categories(self):
        """Test get_categories endpoint"""
        mock_response = {
            "aliexpress_affiliate_category_get_response": {
                "resp_result": {
                    "result": {
                        "categories": {
                            "category": [
                                {"category_id": 1, "category_name": "Electronics"}
                            ]
                        }
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_categories()
                assert isinstance(result, list)
                assert isinstance(result[0], Category)
    
    @pytest.mark.asyncio
    async def test_get_featured_promo(self):
        """Test get_featured_promo endpoint"""
        mock_response = {
            "aliexpress_affiliate_featuredpromo_get_response": {
                "resp_result": {
                    "result": {
                        "promos": {
                            "promo": [
                                {
                                    "promo_name": "Sale",
                                    "promo_desc": "Big sale",
                                    "product_num": 100
                                }
                            ]
                        }
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_featured_promo()
                assert isinstance(result, list)
                assert isinstance(result[0], PromoInfo)
    
    @pytest.mark.asyncio
    async def test_get_featured_promo_products(self):
        """Test get_featured_promo_products endpoint"""
        from aliexpress_async_api.models import ProductSearchResponse
        mock_response = {
            "aliexpress_affiliate_featuredpromo_products_get_response": {
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
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_featured_promo_products()
                assert isinstance(result, ProductSearchResponse)


class TestShippingEndpoints:
    """Test shipping and SKU endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_shipping_info(self):
        """Test get_shipping_info endpoint"""
        mock_response = {
            "aliexpress_affiliate_product_shipping_get_response": {
                "resp_result": {
                    "result": {
                        "shipping_info": {
                            "estimated_delivery_time": "10 days",
                            "freight": "0.00",
                            "tracking_available": "true"
                        }
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_shipping_info("123", "10.00")
                assert isinstance(result, ShippingInfo)
                assert result.estimated_delivery_time == "10 days"
    
    @pytest.mark.asyncio
    async def test_get_sku_detail(self):
        """Test get_sku_detail endpoint"""
        mock_response = {
            "aliexpress_affiliate_product_sku_detail_get_response": {
                "resp_result": {
                    "result": {
                        "skus": {
                            "sku": [
                                {
                                    "sku_id": "sku123",
                                    "sku_attr": "Color:Red",
                                    "sku_price": "10.00",
                                    "sku_stock": "100"
                                }
                            ]
                        }
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_sku_detail("123")
                assert isinstance(result, list)
                assert isinstance(result[0], SKUInfo)


class TestAffiliateEndpoints:
    """Test affiliate link endpoints"""
    
    @pytest.mark.asyncio
    async def test_generate_affiliate_link(self):
        """Test generate_affiliate_link endpoint"""
        mock_response = {
            "aliexpress_affiliate_link_generate_response": {
                "resp_result": {
                    "result": {
                        "promotion_links": {
                            "promotion_link": [
                                {
                                    "promotion_link": "https://affiliate.link",
                                    "source_value": "https://original.link"
                                }
                            ]
                        }
                    }
                }
            }
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.generate_affiliate_link("https://original.link")
                assert isinstance(result, list)
                assert isinstance(result[0], AffiliateLink)


class TestProductVariantEndpoints:
    """Test product variant endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_hotproducts(self):
        """Test get_hotproducts endpoint"""
        from aliexpress_async_api.models import ProductSearchResponse
        mock_response = {
            "aliexpress_affiliate_hotproduct_query_response": {
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
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_hotproducts()
                assert isinstance(result, ProductSearchResponse)
    
    @pytest.mark.asyncio
    async def test_get_hotproduct_download(self):
        """Test get_hotproduct_download endpoint"""
        mock_response = {"result": "download"}
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_hotproduct_download("123")
                assert isinstance(result, dict)
    
    @pytest.mark.asyncio
    async def test_smart_match_products(self):
        """Test smart_match_products endpoint"""
        from aliexpress_async_api.models import ProductSearchResponse
        mock_response = {
            "aliexpress_affiliate_product_smartmatch_response": {
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
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.smart_match_products(keywords="test")
                assert isinstance(result, ProductSearchResponse)


class TestTokenEndpoints:
    """Test token/auth endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_token(self):
        """Test get_token endpoint"""
        from aliexpress_async_api.models import TokenResponse
        mock_response = {
            "access_token": "token123",
            "refresh_token": "refresh123",
            "expire_time": 3600,
            "account": "test@example.com"
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.get_token("code123")
                assert isinstance(result, TokenResponse)
                assert result.access_token == "token123"
    
    @pytest.mark.asyncio
    async def test_refresh_token(self):
        """Test refresh_token endpoint"""
        from aliexpress_async_api.models import TokenResponse
        mock_response = {
            "access_token": "new_token",
            "refresh_token": "new_refresh",
            "expire_time": 3600,
            "account": "test@example.com"
        }
        
        with patch.object(AliExpressIOPClient, 'request', return_value=mock_response):
            async with AliExpressIOPClient("key", "secret") as client:
                result = await client.refresh_token("old_refresh")
                assert isinstance(result, TokenResponse)
