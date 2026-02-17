from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.responses import JSONResponse

from exceptions.parsers.pg_parsers import parse_integrity_error
from exceptions.registry import exception_registry
from exceptions.handlers.base_handler import BaseExceptionHandler


@exception_registry.register(IntegrityError)
class IntegrityErrorHandler(BaseExceptionHandler):

    def handle(self, request: Request, exc: IntegrityError, expose_internal_errors: bool) -> JSONResponse:
        result = parse_integrity_error(exc=exc)
        if result is not None:
            return self.build_error_response(
                status_code=result.status_code,
                code=result.code,
                message=result.message,
                meta=result.meta if expose_internal_errors else None,
            )
        raise exc