import jwt
from app.core.config import settings
import time


def decode_and_validate(token: str) -> dict:
    """Декодирование access-токена"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        if not payload:
            raise ValueError("Токен некорректен")
        if int(time.time() > payload["exp"]):
            raise ValueError("Токен истек. Пожалуйста, получите новый")
        return payload
    except Exception as e:
        raise ValueError(str(e))