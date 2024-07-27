from typing import Optional
from pydantic import BaseModel, EmailStr

from app.utils.user_roles_enum import UserRoles


class BaseUserSchema(BaseModel):
    username: str
    f_name: Optional[str] = None
    l_name: Optional[str] = None
    email: EmailStr
    role: Optional[UserRoles] = UserRoles.ADMIN

    class Config:
        from_attributes = True


class CreateUserSchema(BaseUserSchema):
    password: str


class OutputUserSchema(BaseUserSchema):
    id: int
