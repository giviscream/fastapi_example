import re
from enum import Enum
from typing import Any, Optional

import asyncpg
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from sqlalchemy.exc import IntegrityError


class PgDetailRegex(Enum):
    UNIQUE_DETAIL = (
        r"Key\s+\((?P<columns>[^)]+)\)=\((?P<values>[^)]+)\)\s+already exists"
    )
    FK_DETAIL = (
        r"Key\s+\((?P<columns>[^)]+)\)=\((?P<values>[^)]+)\)\s+is not present in table\s+\"(?P<table>[^\"]+)\""
    )
    NOT_NULL = (
        r"null value in column\s+\"(?P<column>[^\"]+)\"\s+violates not-null constraint"
    )

    @property
    def compiled(self) -> re.Pattern[str]:
        # Компилируем один раз на элемент Enum (и кешируем в _compiled)
        pattern = getattr(self, "_compiled", None)
        if pattern is None:
            pattern = re.compile(self.value, re.IGNORECASE)
            setattr(self, "_compiled", pattern)
        return pattern


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для централизованной обработки ошибок:
    - Postgres/asyncpg ошибки (через SQLAlchemy IntegrityError) парсим без кастомных исключений
    - Неизвестные ошибки -> 500
    - Поддерживает AsyncSession rollback через request.state.db
    """

    def __init__(self, app, *, expose_internal_errors: bool = False):
        super().__init__(app)
        self.expose_internal_errors = expose_internal_errors

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)

        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

        except IntegrityError as exc:
            parsed = self._parse_integrity_error(exc)
            if parsed is not None:
                return parsed
            return self._internal_error(exc)

        except Exception as exc:
            return self._internal_error(exc)

    def _internal_error(self, exc: Exception) -> JSONResponse:
        if self.expose_internal_errors:
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "internal_error",
                        "message": str(exc),
                        "type": type(exc).__name__,
                    }
                },
            )

        return JSONResponse(
            status_code=500,
            content={"error": {"code": "internal_error", "message": "Internal server error"}},
        )

    def _extract_pg_details(
        self, err: BaseException
    ) -> tuple[Optional[str], str, Optional[BaseException]]:
        """
        В SQLAlchemy DBAPI exception обычно в err.orig (для asyncpg это asyncpg exception).
        Возвращаем (constraint_name, detail/message, orig).
        """
        orig = getattr(err, "orig", None)
        if orig is None:
            return None, str(err), None

        constraint = getattr(orig, "constraint_name", None)
        detail = getattr(orig, "detail", None)
        msg = detail or str(orig) or str(err)
        return constraint, msg, orig

    def _client_error(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        meta: dict | None = None,
    ) -> JSONResponse:
        payload: dict[str, Any] = {"error": {"code": code, "message": message}}
        if meta:
            payload["error"]["meta"] = meta
        return JSONResponse(status_code=status_code, content=payload)

    def _parse_integrity_error(self, exc: IntegrityError) -> Optional[JSONResponse]:
        constraint, msg, orig = self._extract_pg_details(exc)
        msg_l = msg.lower()

        # UNIQUE (23505)
        if (
            isinstance(orig, asyncpg.exceptions.UniqueViolationError)
            or "duplicate key value violates unique constraint" in msg_l
        ):
            m = PgDetailRegex.UNIQUE_DETAIL.compiled.search(msg)
            meta: dict[str, Any] = {}
            if constraint:
                meta["constraint"] = constraint
            if m:
                meta["columns"] = [c.strip() for c in m.group("columns").split(",")]
                meta["values"] = [v.strip() for v in m.group("values").split(",")]

            return self._client_error(
                status_code=409,
                code="unique_violation",
                message="Resource already exists",
                meta=meta or None,
            )

        # FK (23503)
        if (
            isinstance(orig, asyncpg.exceptions.ForeignKeyViolationError)
            or "violates foreign key constraint" in msg_l
        ):
            m = PgDetailRegex.FK_DETAIL.compiled.search(msg)
            meta: dict[str, Any] = {}
            if constraint:
                meta["constraint"] = constraint
            if m:
                meta["columns"] = [c.strip() for c in m.group("columns").split(",")]
                meta["values"] = [v.strip() for v in m.group("values").split(",")]
                meta["ref_table"] = m.group("table")

            return self._client_error(
                status_code=409,
                code="foreign_key_violation",
                message="Related resource not found",
                meta=meta or None,
            )

        # NOT NULL (23502)
        if (
            isinstance(orig, asyncpg.exceptions.NotNullViolationError)
            or "violates not-null constraint" in msg_l
        ):
            m = PgDetailRegex.NOT_NULL.compiled.search(msg)
            meta: dict[str, Any] = {"constraint": constraint} if constraint else {}
            if m:
                meta["column"] = m.group("column")

            return self._client_error(
                status_code=422,
                code="not_null_violation",
                message="Missing required field",
                meta=meta or None,
            )

        # CHECK (23514)
        if (
            isinstance(orig, asyncpg.exceptions.CheckViolationError)
            or "violates check constraint" in msg_l
        ):
            meta = {"constraint": constraint} if constraint else None
            return self._client_error(
                status_code=422,
                code="check_violation",
                message="Invalid data",
                meta=meta,
            )

        return None