import time
import jwt
from passlib.context import CryptContext
from typing import Any

from app.core.config import settings
from app.core.exceptions import TokenExpiredError


pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    """Функция хеширования пароля"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Функция проверки пароля"""
    return pwd_context.verify(password, hashed_password)


def create_access_token(sub: str, role: str) -> str:
    """Генерация access-токена"""
    payload = {
        "type": "access",
        "sub": sub,
        "role": role,
        "exp": int(time.time()) + 60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "iat": int(time.time())
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> dict[str, Any]:
    """Декодирование access-токена"""
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    if int(time.time() > payload["exp"]):
        raise TokenExpiredError()
    return payload