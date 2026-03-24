from enum import Enum
from pydantic import BaseModel, EmailStr, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime


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
    email: EmailStr
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
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = None

    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    user: UserResponse
    token: Token
