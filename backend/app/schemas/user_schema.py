from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="user email")
    user_name: str = Field(..., min_length=5, max_length=100, description="user username")
    password: str = Field(..., min_length=5, max_length=25, description="user password")


class UserOut(BaseModel):
    user_id: UUID
    user_name: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: Optional[bool] = False
