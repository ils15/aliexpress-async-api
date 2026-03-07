"""
Authentication endpoint implementation
"""

from typing import Any, Dict, Optional

from aliexpress_async_api.endpoints.base import BaseEndpoint
from aliexpress_async_api.models.token import TokenResponse


class AuthEndpoint(BaseEndpoint):
    """Endpoint for authentication operations"""

    async def get_token(self, authorization_code: str, **kwargs) -> TokenResponse:
        """
        Exchange authorization code for access token

        Args:
            authorization_code: OAuth authorization code
            **kwargs: Additional parameters

        Returns:
            TokenResponse: Access token and metadata
        """
        params = {"code": authorization_code, **kwargs}

        response = await self.request("aliexpress.open.oauth.authorize", params)

        token_data = response.get("access_token_response", {})

        return TokenResponse(
            access_token=token_data.get("access_token", ""),
            refresh_token=token_data.get("refresh_token", ""),
            expire_time=int(token_data.get("expires_in", 3600)),
            account=token_data.get("account", ""),
            raw_data=token_data,
        )

    async def refresh_token(self, refresh_token: str, **kwargs) -> TokenResponse:
        """
        Refresh an expired access token

        Args:
            refresh_token: Refresh token from previous authentication
            **kwargs: Additional parameters

        Returns:
            TokenResponse: New access token
        """
        params = {"refresh_token": refresh_token, **kwargs}

        response = await self.request("aliexpress.open.oauth.token.refresh", params)

        token_data = response.get("access_token_response", {})

        return TokenResponse(
            access_token=token_data.get("access_token", ""),
            refresh_token=token_data.get("refresh_token", ""),
            expire_time=int(token_data.get("expires_in", 3600)),
            account=token_data.get("account", ""),
            raw_data=token_data,
        )
