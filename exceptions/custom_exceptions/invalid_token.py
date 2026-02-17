from .base_app_exception import BaseAppException
from fastapi import status


class InvalidTokenException(BaseAppException):
    def __init__(self, message: str = "Invalid Token"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_TOKEN",
        )
