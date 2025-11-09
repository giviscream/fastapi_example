from fastapi.security import OAuth2PasswordBearer
from core.containers import Container
from schemas.user.response import UserResponse
from services.auth import AuthService
from fastapi import Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

@inject
async def get_current_user(
    token: str = Depends(dependency=oauth_scheme),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> UserResponse:
    user: UserResponse = await auth_service.get_current_user(token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user