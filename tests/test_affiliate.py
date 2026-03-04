import pytest
from aliexpress_async_api import ProductSearchResponse

@pytest.mark.asyncio
async def test_search_products(api_client):
    """Test product searching."""
    result = await api_client.search_products(keyword="3d printer")
    assert isinstance(result, ProductSearchResponse)
    assert len(result.products) >= 0

@pytest.mark.asyncio
async def test_get_categories(api_client):
    """Test retrieving categories."""
    result = await api_client.get_categories()
    assert isinstance(result, list)
    if len(result) > 0:
        assert hasattr(result[0], 'category_id')

@pytest.mark.asyncio
async def test_generate_affiliate_links(api_client, tracking_id):
    """Test link generation."""
    urls = [
        "https://www.aliexpress.com/item/1005006648408257.html"
    ]
    result = await api_client.generate_affiliate_links(
        promotion_links=urls,
        tracking_id=tracking_id
    )
    assert isinstance(result, list)
    if len(result) > 0:
        assert result[0].promotion_link.startswith("https://")

@pytest.mark.asyncio
async def test_get_product_details(api_client):
    """Test product details retrieval."""
    product_ids = ["1005006648408257"]
    result = await api_client.get_product_details(product_ids=product_ids)
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0].product_id == 1005006648408257
