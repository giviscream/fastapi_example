# exceptions/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from exceptions.registry import exception_registry

import exceptions.handlers  # noqa: F401 — триггерим декораторы


class ErrorHandlingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, *, expose_internal_errors: bool = False):
        super().__init__(app)
        self.expose_internal_errors = expose_internal_errors

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            return exception_registry.handle(
                request=request,
                exc=exc,
                expose_internal_errors=self.expose_internal_errors,
            )
