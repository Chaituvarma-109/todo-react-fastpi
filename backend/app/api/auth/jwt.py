from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from backend.app.core.security import create_access_token, create_refresh_access_token
from backend.app.models.user_model import User
from backend.app.schemas.auth_schema import TokenSchema, TokenPayload
from backend.app.schemas.user_schema import UserOut
from backend.app.services.user_service import UserService
from backend.app.deps.user_deps import get_current_user
from backend.app.core.config import settings


auth_router = APIRouter()


@auth_router.post('/login', summary="Create access and refresh tokens for user.", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    # create access and refresh tokens
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_access_token(user.user_id),
    }


@auth_router.post('/test-token', summary="test if the access token is valid", response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)):
    return user


@auth_router.post('/refresh', summary='Refresh token', response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token-expired",
                                headers={"WWW-Authenticate": "Bearer"}, )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"}, )

    user = await UserService.get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="could not find user")

    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_access_token(user.user_id),
    }
