from functools import wraps
from typing import Callable, Any
from sqlalchemy.ext.asyncio import AsyncSession

def transactional(repository_attr: str = "repository"):
    """
    Декоратор с возможностью указать имя атрибута репозитория.
    
    Usage:
        @transactional("user_repository")
        async def create_user(self, data: dict):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            service_instance = args[0]

            repository = getattr(service_instance, repository_attr, None)
            if repository is None:
                raise ValueError(f"Репозиторий '{repository_attr}' не найден в сервисе")

            session: AsyncSession = getattr(repository, 'session', None)
            if session is None:
                raise ValueError("Сессия не найдена в репозитории")
            
            try:
                result = await func(*args, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e
        
        return wrapper
    return decorator