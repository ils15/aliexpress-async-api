"""
Tests for OAuth authentication flow - aliexpress_async_api.auth.oauth
"""

import pytest

from aliexpress_async_api.auth.oauth import AliExpressOAuth


class TestAliExpressOAuth:
    """OAuth flow tests"""

    def test_build_auth_url_with_defaults(self):
        """Test OAuth authorization URL generation with default parameters"""
        oauth = AliExpressOAuth(app_key="test_key")
        url = oauth.build_auth_url(redirect_uri="https://example.com/callback")

        assert "https://auth.aliexpress.com/oauth/authorize" in url
        assert "client_id=test_key" in url
        assert "redirect_uri=https%3A%2F%2Fexample.com%2Fcallback" in url
        assert "response_type=code" in url
        assert "view=web" in url
        assert "state=aliexpress_oauth" in url

    def test_build_auth_url_with_custom_state(self):
        """Test OAuth URL with custom state parameter"""
        oauth = AliExpressOAuth(app_key="test_key")
        url = oauth.build_auth_url(
            redirect_uri="https://example.com/callback", state="custom_state_123"
        )

        assert "state=custom_state_123" in url

    def test_build_auth_url_with_mobile_view(self):
        """Test OAuth URL for mobile view"""
        oauth = AliExpressOAuth(app_key="test_key")
        url = oauth.build_auth_url(
            redirect_uri="https://example.com/callback", view="mobile"
        )

        assert "view=mobile" in url

    def test_oauth_init_requires_app_key(self):
        """Test that OAuth initialization requires app_key"""
        with pytest.raises(ValueError, match="app_key is required"):
            AliExpressOAuth(app_key="")

    def test_oauth_init_validates_app_key_is_string(self):
        """Test that app_key must be a string"""
        with pytest.raises(ValueError, match="app_key must be a string"):
            AliExpressOAuth(app_key=None)
