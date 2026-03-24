from beanie import Indexed, Document
from .timestamp import TimestampDocument
from pydantic import BaseModel, BeforeValidator
from typing import Annotated, Optional
from datetime import datetime
from enum import Enum


class Semester(int, Enum):
    semester_1 = 1
    semester_2 = 2


class TahunAjaranResponse(BaseModel):
    id: Annotated[str, BeforeValidator(str)]
    nama: Annotated[str, Indexed(unique=True)]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    is_active: bool
    semester: Semester

    class Config:
        from_attributes = True


class TahunAjaranUpdated(BaseModel):
    is_active: bool


class TahunAjaranCreated(BaseModel):
    nama: Annotated[str, Indexed(unique=True)]
    semester: Semester


class TahunAjaranModel(TimestampDocument, TahunAjaranCreated):
    is_active: bool = False

    class Settings:
        name = "tahun_ajaran"
        indexes = ["deleted_at"]
