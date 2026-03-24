from pydantic import BaseModel, BeforeValidator
from typing import Annotated, Optional
from enum import Enum


class Semester(int, Enum):
    semester_1 = 1
    semester_2 = 2


class TahunAjaranCreated(BaseModel):
    nama: str
    semester: Semester


class TahunAjaranUpdated(BaseModel):
    is_active: bool


class TahunAjaranResponse(BaseModel):
    id: Annotated[str, BeforeValidator(str)]
    nama: str
    semester: Semester
    is_active: bool
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = None

    class Config:
        from_attributes = True
