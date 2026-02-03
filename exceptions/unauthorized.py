from .base_app_exception import BaseAppException


class UnauthorizedException(BaseAppException):
    def __init__(self, message: str = "Login failed"):
        super().__init__(message=message, status_code=401, error_code="LOGIN_FAILED")
