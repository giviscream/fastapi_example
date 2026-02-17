import re
from enum import Enum
from typing import Any, Optional

import asyncpg
from fastapi import status

from exceptions.custom_exceptions.pg_error_result import PgErrorResult


class PgDetailRegex(Enum):
    UNIQUE_DETAIL = re.compile(
        r"Key\s+\((?P<columns>[^)]+)\)=\((?P<values>[^)]+)\)\s+already exists",
        re.IGNORECASE,
    )
    FK_DETAIL = re.compile(
        r"Key\s+\((?P<columns>[^)]+)\)=\((?P<values>[^)]+)\)\s+"
        r"is not present in table\s+\"(?P<table>[^\"]+)\"",
        re.IGNORECASE,
    )
    NOT_NULL = re.compile(
        r"null value in column\s+\"(?P<column>[^\"]+)\"\s+"
        r"(?:of relation\s+\"(?P<relation>[^\"]+)\"\s+)?"
        r"violates not-null constraint",
        re.IGNORECASE,
    )
    NOT_FOUND_DETAIL = re.compile(
        r"Key\s+\((?P<columns>[^)]+)\)=\((?P<values>[^)]+)\)\s+is not present in table\s+\"(?P<table>[^\"]+)\"",
        re.IGNORECASE,
    )


def extract_pg_details(
    err: BaseException,
) -> tuple[Optional[str], str, Optional[BaseException]]:
    """
    Извлекает constraint_name, detail-сообщение и оригинальное
    asyncpg-исключение из SQLAlchemy IntegrityError.
    """
    orig = getattr(err, "orig", None)
    if orig is None:
        return None, str(err), None

    constraint = getattr(orig, "constraint_name", None)
    detail = getattr(orig, "detail", None)
    msg = detail or str(orig) or str(err)
    return constraint, msg, orig


def _parse_unique_violation(
    constraint: str | None,
    msg: str,
    orig: BaseException | None,
) -> PgErrorResult | None:
    msg_l = msg.lower()
    if not (
        isinstance(orig, asyncpg.exceptions.UniqueViolationError)
        or "duplicate key value violates unique constraint" in msg_l
    ):
        return None

    m = PgDetailRegex.UNIQUE_DETAIL.value.search(msg)
    meta: dict[str, Any] = {}
    if constraint:
        meta["constraint"] = constraint
    if m:
        meta["columns"] = [c.strip() for c in m.group("columns").split(",")]
        meta["values"] = [v.strip() for v in m.group("values").split(",")]

    return PgErrorResult(
        status_code=status.HTTP_409_CONFLICT,
        code="unique_violation",
        message="Resource already exists",
        meta=meta or None,
    )


def _parse_fk_violation(
    constraint: str | None,
    msg: str,
    orig: BaseException | None,
) -> PgErrorResult | None:
    msg_l = msg.lower()
    if not (
        isinstance(orig, asyncpg.exceptions.ForeignKeyViolationError)
        or "violates foreign key constraint" in msg_l
    ):
        return None

    m = PgDetailRegex.FK_DETAIL.value.search(msg)
    meta: dict[str, Any] = {}
    if constraint:
        meta["constraint"] = constraint
    if m:
        meta["columns"] = [c.strip() for c in m.group("columns").split(",")]
        meta["values"] = [v.strip() for v in m.group("values").split(",")]
        meta["ref_table"] = m.group("table")

    return PgErrorResult(
        status_code=status.HTTP_409_CONFLICT,
        code="foreign_key_violation",
        message="Related resource not found",
        meta=meta or None,
    )


def _parse_not_null_violation(
    constraint: str | None,
    msg: str,
    orig: BaseException | None,
) -> PgErrorResult | None:
    msg_l = msg.lower()
    if not (
        isinstance(orig, asyncpg.exceptions.NotNullViolationError)
        or "violates not-null constraint" in msg_l
    ):
        return None

    m = PgDetailRegex.NOT_NULL.value.search(msg)
    meta: dict[str, Any] = {"constraint": constraint} if constraint else {}
    if m:
        meta["column"] = m.group("column")

    return PgErrorResult(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="not_null_violation",
        message="Missing required field",
        meta=meta or None,
    )


def _parse_check_violation(
    constraint: str | None,
    msg: str,
    orig: BaseException | None,
) -> PgErrorResult | None:
    msg_l = msg.lower()
    if not (
        isinstance(orig, asyncpg.exceptions.CheckViolationError)
        or "violates check constraint" in msg_l
    ):
        return None

    meta = {"constraint": constraint} if constraint else None
    return PgErrorResult(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="check_violation",
        message="Invalid data",
        meta=meta,
    )

def _parse_not_found(
    constraint: str | None,
    msg: str,
    orig: BaseException | None,
) -> PgErrorResult | None:
    
    if "no row was found" not in msg.lower():
        return None

    return PgErrorResult(
        status_code=status.HTTP_404_NOT_FOUND,
        code="not_found",
        message="Resource not found",
        meta=None,
    )




_PARSERS = (
    _parse_unique_violation,
    _parse_fk_violation,
    _parse_not_null_violation,
    _parse_check_violation,
    _parse_not_found
)


def parse_integrity_error(exc: Exception) -> PgErrorResult | None:
    constraint, msg, orig = extract_pg_details(exc)
    for parser in _PARSERS:
        result = parser(constraint=constraint, msg=msg, orig=orig)
        if result is not None:
            return result
    return None
