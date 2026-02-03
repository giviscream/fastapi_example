from .base_app_exception import BaseAppException


class InvalidTokenException(BaseAppException):
    def __init__(self, message: str = "Token is invalid"):
        super().__init__(message=message, status_code=401, error_code="INVALID_TOKEN")
