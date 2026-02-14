from logging import Logger
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar, cast

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.containers import Container
from dependency_injector.wiring import Provide, inject

P = ParamSpec('P')
R = TypeVar('R')


def managed_db_session():
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        @inject
        async def wrapper(*args: P.args, logger: Logger = Depends(Provide[Container.logger]), **kwargs: P.kwargs) -> R:
            db_session: AsyncSession = cast(AsyncSession, kwargs.get('db_session'))
            try:
                result = await func(*args, **kwargs)
                logger.debug('Got successful result. Commit DB changes.: %s', result)
                await db_session.commit()
                return result
            except Exception as exc:
                logger.warning('Exception caught. Roll DB changes back.: %s', exc)
                await db_session.rollback()
                raise exc
            finally:
                await db_session.close()
        return wrapper
    return decorator