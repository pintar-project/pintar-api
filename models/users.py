from enum import Enum
from beanie import Indexed
from datetime import datetime
from typing import Optional, Annotated
from .timestamp import TimestampDocument
from pydantic import BaseModel, EmailStr, BeforeValidator


class UserRole(str, Enum):
    ADMIN = "admin"
    GURU = "guru"
    SISWA = "siswa"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UsersCreated(BaseModel):
    username: str
    nama_lengkap: str
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: str


class Token(BaseModel):
    access_token: str


class UserResponse(BaseModel):
    id: Annotated[str, BeforeValidator(str)]
    username: str
    nama_lengkap: str
    email: EmailStr
    role: UserRole
    avatar_url: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    user: UserResponse
    token: Token


class UsersModel(TimestampDocument, UsersCreated):
    avatar_url: str
    role: UserRole

    class Settings:
        name = "users"
        indexes = ["deleted_at"]
