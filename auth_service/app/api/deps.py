from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии БД"""
    async with AsyncSessionLocal() as session:
        yield session

async def get_users_repo(session: AsyncSession = Depends(get_db)) -> UserRepository:
    """Получение репозитория пользователя"""
    return UserRepository(session)

async def get_auth_uc(user_repo: UserRepository = Depends(get_users_repo)) -> AuthUseCase:
    """Получение usecase-объекта для авторизации"""
    return AuthUseCase(user_repo)

async def get_current_user_id(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))) -> int:
    """Получение текущего пользователя (user_id) из токена авторизации"""
    payload = decode_token(token)
    if payload is None:
        raise InvalidTokenError()
    try:
        user_id = int(payload["sub"])
        return user_id
    except (KeyError, ValueError):
        raise TokenExpiredError()