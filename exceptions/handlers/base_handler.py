from abc import ABC, abstractmethod
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse


class BaseExceptionHandler(ABC):

    @abstractmethod
    def handle(
        self,
        request: Request,
        exc: Exception,
        expose_internal_errors: bool,
    ) -> JSONResponse: ...

    def build_error_response(
        self,
        status_code: int,
        code: str,
        message: str,
        meta: dict[str, Any] | None = None,
    ) -> JSONResponse:
        payload: dict[str, Any] = {
            "error": {
                "code": code,
                "message": message,
            }
        }
        if meta:
            payload["error"]["meta"] = meta
        return JSONResponse(status_code=status_code, content=payload)
