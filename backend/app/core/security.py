from datetime import datetime, timedelta
from typing import Union, Any

from passlib.context import CryptContext
from jose import jwt

from backend.app.core.config import settings


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(subject: Union[str, Any], expired_delta: int = None) -> str:
    if expired_delta is not None:
        expired_delta = datetime.utcnow() + expired_delta
    else:
        expired_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expired_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_refresh_access_token(subject: Union[str, Any], expired_delta: int = None) -> str:
    if expired_delta is not None:
        expired_delta = datetime.utcnow() + expired_delta
    else:
        expired_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expired_delta, "sub": str(subject)}
    encoded_refresh_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)

    return encoded_refresh_jwt


def get_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)
