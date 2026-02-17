from .base_app_exception import BaseAppException
from fastapi import status


class UnauthorizedException(BaseAppException):
    def __init__(self, message: str = "Login failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="LOGIN_FAILED",
        )
