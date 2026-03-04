"""
OAuth authentication flow for AliExpress IOP API
"""
import urllib.parse
from typing import Optional


class AliExpressOAuth:
    """Handles OAuth authorization flow for AliExpress IOP"""
    
    AUTHORIZE_URL = "https://auth.aliexpress.com/oauth/authorize"
    
    def __init__(self, app_key: str):
        """
        Initialize OAuth handler
        
        Args:
            app_key: AliExpress Open Platform application key
            
        Raises:
            ValueError: If app_key is not provided or invalid
        """
        if not isinstance(app_key, str):
            raise ValueError("app_key must be a string")
        if not app_key:
            raise ValueError("app_key is required")
        
        self.app_key = app_key
    
    def build_auth_url(
        self,
        redirect_uri: str,
        state: str = "aliexpress_oauth",
        view: str = "web"
    ) -> str:
        """
        Build OAuth authorization URL
        
        Args:
            redirect_uri: URL to redirect after authorization
            state: Anti-CSRF state parameter
            view: Display view ('web' or 'mobile')
            
        Returns:
            str: Complete OAuth authorization URL
        """
        params = {
            "client_id": self.app_key,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "view": view,
            "state": state,
        }
        return self.AUTHORIZE_URL + "?" + urllib.parse.urlencode(params)
