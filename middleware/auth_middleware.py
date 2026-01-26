from uuid import UUID
from fastapi import Depends, Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from dependency_injector.wiring import inject, Provide
from core.containers import Container
from services.auth import AuthService


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки токенов"""

    # Публичные эндпоинты, которые не требуют авторизации
    PUBLIC_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/login",
        "/api/v1/auth/token",
        "/api/v1/auth/register",
        "/api/v1/auth/",
    ]

    @inject
    async def dispatch(
        self,
        request: Request,
        call_next,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
    ):

        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Валидация токена
        user_id: UUID = await auth_service.with_session(
            session=request.state.db_session
        ).get_current_user_id(token=token)

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Добавляем данные пользователя в state запроса
        request.state.user_id = user_id

        response = await call_next(request)
        return response
