from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class BaseUserModelSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str] = "admin"
    organization: Optional[str] = None
    isActive: bool | None = False

    class Config:
        from_attributes = True


class InputUserModelSchema(BaseUserModelSchema):
    password: str


class InDBUserModelSchema(BaseUserModelSchema):
    id: int
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class OutputUserModelSchema(BaseUserModelSchema):
    id: int
    createdAt: Optional[datetime]


class UpdateUserModelSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None
    isActive: Optional[bool] = None
    password: Optional[str] = None
    updatedAt: Optional[datetime] = None
