class AliExpressException(Exception):
    """Base exception for all AliExpress API errors."""

    pass


class InvalidCredentialsException(AliExpressException):
    """Raised when missing or invalid credentials are provided."""

    pass


class ProductNotFoundException(AliExpressException):
    """Raised when a product search or lookup returns no results."""

    pass


class APIRequestException(AliExpressException):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, code: str = None, sub_code: str = None):
        self.code = code
        self.sub_code = sub_code
        super().__init__(f"[{code or 'ERROR'}] {message}")
