from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type

from starlette.requests import Request
from starlette.responses import JSONResponse

if TYPE_CHECKING:
    from exceptions.handlers.base_handler import BaseExceptionHandler

logger = logging.getLogger(__name__)


class ExceptionHandlerRegistry:

    def __init__(self) -> None:
        self._handlers: dict[Type[Exception], BaseExceptionHandler] = {}

    def register(self, *exc_types: Type[Exception]):
        def decorator(handler_cls):
            instance = handler_cls()
            for exc_type in exc_types:
                if exc_type in self._handlers:
                    logger.warning(
                        "Handler for %s overridden by %s",
                        exc_type.__name__,
                        handler_cls.__name__,
                    )
                self._handlers[exc_type] = instance
            return handler_cls

        return decorator

    def handle(
        self, request: Request, exc: Exception, expose_internal_errors: bool = False
    ) -> JSONResponse:
        handler = self._handlers.get(type(exc))
        if handler is None:
            raise exc
        return handler.handle(
            request=request,
            exc=exc,
            expose_internal_errors=expose_internal_errors,
        )


exception_registry = ExceptionHandlerRegistry()
