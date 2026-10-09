from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from core.config import settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.TOKEN_LIFETIME_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )
