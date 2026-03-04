"""Package initialization - auth module"""
from .oauth import AliExpressOAuth
from .signature import SignatureV1


# Backward compatibility: AliExpressAuth is now SignatureV1
class AliExpressAuth(SignatureV1):
    """
    Backward compatibility wrapper for existing code.
    AliExpressAuth is now SignatureV1 with the same interface.
    """
    def __init__(self, app_key: str, app_secret: str):
        super().__init__(app_secret=app_secret, app_key=app_key)


__all__ = ["AliExpressOAuth", "SignatureV1", "AliExpressAuth"]
