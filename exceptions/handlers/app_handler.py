from __future__ import annotations
from starlette.requests import Request
from starlette.responses import JSONResponse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from exceptions.custom_exceptions.base_app_exception import BaseAppException
from exceptions.custom_exceptions import (
    InvalidTokenException,
    UnauthorizedException,
)
from exceptions.registry import exception_registry
from exceptions.handlers.base_handler import BaseExceptionHandler


@exception_registry.register(
    InvalidTokenException,
    UnauthorizedException,
)
class AppExceptionHandler(BaseExceptionHandler):
    """
    Один обработчик для всех кастомных исключений.
    """

    def handle(self, request: Request, exc: BaseAppException, expose_internal_errors: bool) -> JSONResponse:
        return self.build_error_response(
            status_code=exc.status_code,
            code=exc.error_code,
            message=exc.message,
        )
