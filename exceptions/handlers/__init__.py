"""
Импортируем все модули обработчиков, чтобы декораторы @register
выполнились при старте приложения и обработчики попали в registry.
"""

from exceptions.handlers.base_handler import BaseExceptionHandler
from exceptions.handlers.app_handler import AppExceptionHandler
from exceptions.handlers.http_handler import HTTPExceptionHandler
from exceptions.handlers.integrity_handler import IntegrityErrorHandler
from exceptions.handlers.no_result_handler import NoResultFoundErrorHandler

__all__ = [
    "AppExceptionHandler",
    "BaseExceptionHandler",
    "HTTPExceptionHandler",
    "IntegrityErrorHandler",
    "NoResultFoundErrorHandler",
]
