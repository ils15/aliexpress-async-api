"""
MD5 V1 signature algorithm for AliExpress IOP /sync endpoint
"""
import hashlib
import time
from typing import Any, Dict, Optional


class SignatureV1:
    """Implements the V1 MD5 signature algorithm for AliExpress IOP"""
    
    def __init__(self, app_secret: str, app_key: Optional[str] = None):
        """
        Initialize signature handler
        
        Args:
            app_secret: AliExpress application secret (required)
            app_key: AliExpress application key (optional, for system params)
            
        Raises:
            ValueError: If app_secret is not provided or invalid
        """
        if not isinstance(app_secret, str):
            raise ValueError("app_secret must be a string")
        if not app_secret:
            raise ValueError("app_secret is required")
        
        self.app_secret = app_secret
        self.app_key = app_key
    
    @staticmethod
    def timestamp_ms() -> str:
        """Returns current time in milliseconds as string"""
        return str(int(time.time() * 1000))
    
    @staticmethod
    def _mix_str(value: Any) -> str:
        """Convert any value to string for signing"""
        if isinstance(value, str):
            return value
        elif isinstance(value, bytes):
            return value.decode("utf-8")
        else:
            return str(value)
    
    def build_system_params(
        self,
        api_method: str,
        session: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Build system parameters required by AliExpress API
        
        Args:
            api_method: API method name (e.g., 'aliexpress.affiliate.product.query')
            session: Optional session token for authenticated requests
            
        Returns:
            Dict of system parameters
        """
        params = {
            "format": "json",
            "sign_method": "md5",
            "v": "2.0",
            "timestamp": self.timestamp_ms(),
            "partner_id": "aliexpress-async-api",
            "method": api_method,
        }
        
        if self.app_key:
            params["app_key"] = self.app_key
        
        if session:
            params["session"] = session
        
        return params
    
    def sign(
        self,
        sys_params: Dict[str, str],
        business_params: Dict[str, str]
    ) -> str:
        """
        Calculate MD5 V1 signature
        
        Algorithm:
        1. Merge system and business parameters
        2. Sort by key alphabetically
        3. Concatenate: SECRET + key1value1key2value2... + SECRET
        4. Calculate MD5 hash, convert to uppercase
        
        Args:
            sys_params: System parameters
            business_params: Business-specific parameters
            
        Returns:
            str: MD5 signature (32-char hex string, uppercase)
        """
        # Merge all parameters
        all_params = {**sys_params, **business_params}
        
        # Sort by key
        sorted_keys = sorted(all_params.keys())
        
        # Build concatenation string: SECRET + k1v1k2v2...kNvN + SECRET
        sign_str = self.app_secret
        for key in sorted_keys:
            sign_str += key + self._mix_str(all_params[key])
        sign_str += self.app_secret
        
        # Calculate MD5 and return uppercase
        return hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()
