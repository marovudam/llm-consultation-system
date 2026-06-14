from datetime import datetime, timedelta, timezone

import pytest
import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def test_decode_and_validate() -> None:
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": "sub",
            "role": "user",
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=10)).timestamp()),
        },
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
    )
    payload = decode_and_validate(token)
    assert payload["sub"] == "sub"
    assert payload["role"] == "user"
    assert payload["exp"] > int(now.timestamp())

def test_decode_and_validate_expired() -> None:
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": "123",
            "role": "user",
            "iat": int(now.timestamp()),
            "exp": int((now - timedelta(minutes=10)).timestamp()),
        },
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
    )
    with pytest.raises(ValueError):
        decode_and_validate(token)

def test_decode_and_validate_invalid_token() -> None:
    with pytest.raises(ValueError):
        decode_and_validate("not_a_jwt")