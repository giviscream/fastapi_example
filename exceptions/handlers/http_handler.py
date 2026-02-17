from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from exceptions.registry import exception_registry
from exceptions.handlers.base_handler import BaseExceptionHandler


@exception_registry.register(HTTPException)
class HTTPExceptionHandler(BaseExceptionHandler):

    def handle(self, request: Request, exc: HTTPException, expose_internal_errors: bool) -> JSONResponse:
        return self.build_error_response(
            status_code=exc.status_code,
            code="http_error",
            message=exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        )
