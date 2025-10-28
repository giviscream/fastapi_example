from functools import lru_cache
import logging
from sys import stdout

from core.settings import settings

LOGS_FMT = "[%(asctime)s.%(msecs)05d][%(levelname)s][%(name)s] %(message)s"
LOGS_DATE_FMT = "%Y-%m-%dT%H:%M:%S"


# Создание и настройка логгера
def setup_logger(
    logs_level: str,
    logs_fmt: str,
    logs_date_fmt: str,
    logger_name: str,
) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(stdout)
    console_handler.setLevel(level=logs_level)

    formatter = logging.Formatter(fmt=logs_fmt, datefmt=logs_date_fmt)
    console_handler.setFormatter(fmt=formatter)

    logger.addHandler(hdlr=console_handler)
    return logger


@lru_cache
def get_logger() -> logging.Logger:
    return setup_logger(
        logs_level=settings.LOGS_LEVEL,
        logs_fmt=LOGS_FMT,
        logs_date_fmt=LOGS_DATE_FMT,
        logger_name="fastapi_app",
    )
