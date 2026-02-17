class BaseAppException(Exception):
    """Базовый класс для всех кастомных исключений приложения."""

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: str | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)