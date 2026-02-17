from typing import Any


class PgErrorResult:
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        meta: dict[str, Any] | None = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.meta = meta
