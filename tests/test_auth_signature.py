"""
Tests for MD5 V1 signature algorithm - aliexpress_async_api.auth.signature
"""

import hashlib

import pytest

from aliexpress_async_api.auth.signature import SignatureV1


class TestSignatureV1:
    """MD5 V1 signature tests"""

    def test_signature_generation_basic(self):
        """Test basic MD5 V1 signature generation"""
        sig = SignatureV1(app_secret="secret123")
        sys_params = {"app_key": "test", "method": "test.method"}
        business_params = {"keywords": "test"}

        result = sig.sign(sys_params, business_params)

        # Signature should be a hex string of 32 chars (MD5)
        assert isinstance(result, str)
        assert len(result) == 32
        assert all(c in "0123456789ABCDEF" for c in result)

    def test_signature_deterministic(self):
        """Test that same inputs produce same signature"""
        sig = SignatureV1(app_secret="secret123")
        sys_params = {"app_key": "test", "method": "test.method"}
        business_params = {"keywords": "test"}

        result1 = sig.sign(sys_params, business_params)
        result2 = sig.sign(sys_params, business_params)

        assert result1 == result2

    def test_signature_changes_with_different_secrets(self):
        """Test that different secrets produce different signatures"""
        sig1 = SignatureV1(app_secret="secret1")
        sig2 = SignatureV1(app_secret="secret2")
        sys_params = {"app_key": "test", "method": "test.method"}
        business_params = {"keywords": "test"}

        result1 = sig1.sign(sys_params, business_params)
        result2 = sig2.sign(sys_params, business_params)

        assert result1 != result2

    def test_signature_changes_with_different_params(self):
        """Test that different parameters produce different signatures"""
        sig = SignatureV1(app_secret="secret")
        sys_params = {"app_key": "test", "method": "test.method"}

        result1 = sig.sign(sys_params, {"keywords": "test1"})
        result2 = sig.sign(sys_params, {"keywords": "test2"})

        assert result1 != result2

    def test_signature_with_empty_params(self):
        """Test signature with minimal params"""
        sig = SignatureV1(app_secret="secret")
        result = sig.sign({}, {})

        assert isinstance(result, str)
        assert len(result) == 32

    def test_signature_with_special_chars(self):
        """Test signature with special characters in params"""
        sig = SignatureV1(app_secret="secret")
        sys_params = {"app_key": "test&key", "method": "test.method"}
        business_params = {"description": "test@special#chars"}

        result = sig.sign(sys_params, business_params)

        assert isinstance(result, str)
        assert len(result) == 32

    def test_build_system_params_basic(self):
        """Test system parameters building"""
        sig = SignatureV1(app_secret="secret")
        params = sig.build_system_params(api_method="test.method")

        assert params["method"] == "test.method"
        assert params["format"] == "json"
        assert params["v"] == "2.0"
        assert params["sign_method"] == "md5"
        assert "timestamp" in params
        assert "app_key" not in params  # Should not include in base build

    def test_build_system_params_with_session(self):
        """Test system params with session token"""
        sig = SignatureV1(app_secret="secret", app_key="key123")
        params = sig.build_system_params(api_method="test.method", session="token123")

        assert params["session"] == "token123"
        assert params["method"] == "test.method"

    def test_mix_str_conversion(self):
        """Test string conversion utility"""
        sig = SignatureV1(app_secret="secret")

        # String passthrough
        assert sig._mix_str("test") == "test"

        # Integer conversion
        assert sig._mix_str(123) == "123"

        # Bytes conversion
        assert sig._mix_str(b"test") == "test"

    def test_signature_init_requires_app_secret(self):
        """Test that signature initialization requires app_secret"""
        with pytest.raises(ValueError, match="app_secret is required"):
            SignatureV1(app_secret="")

    def test_signature_init_validates_app_secret_is_string(self):
        """Test that app_secret must be a string"""
        with pytest.raises(ValueError, match="app_secret must be a string"):
            SignatureV1(app_secret=None)
