from enum import Enum
from beanie import Link
from .timestamp import TimestampDocument
from .kelas import KelasModel
from pydantic import BaseModel, BeforeValidator
from typing import Annotated, Optional
from datetime import datetime


class TipeModul(str, Enum):
    FILE = "file"
    LINK = "link"


class ModulResponse(BaseModel):
    id: Annotated[str, BeforeValidator(str)]
    id_kelas: Link[KelasModel]
    judul: str
    tipe: TipeModul
    link: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ModulCreated(BaseModel):
    judul: str
    link: str


class ModulModel(TimestampDocument, ModulCreated):
    id_kelas: Link[KelasModel]
    tipe: TipeModul

    class Settings:
        name = "modul"
        indexes = ["deleted_at"]
