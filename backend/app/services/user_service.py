from typing import Optional
from uuid import UUID

from backend.app.schemas.user_schema import UserAuth
from backend.app.models.user_model import User
from backend.app.core.security import get_password, verify_password


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        user_in = User(
            user_name=user.user_name,
            email=user.email,
            hashed_password=get_password(user.password),
        )
        await user_in.save()
        return user_in

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None

        if not verify_password(password=password, hashed_password=user.hashed_password):
            return None

        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user

    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user
