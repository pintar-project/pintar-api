from enum import Enum
from pydantic import BaseModel, BeforeValidator
from typing import Annotated, Optional
from .users import UserResponse
from .mata_pelajaran import MataPelajaranResponse
from .tahun_ajaran import TahunAjaranResponse
from .jurusan import Jurusan
from .tingkat import Tingkat


class TipeModul(str, Enum):
    FILE = "file"
    LINK = "link"


class ModulCreated(BaseModel):
    judul: str
    link: str
    tingkat: Tingkat


class ModulResponse(BaseModel):
    id: Annotated[str, BeforeValidator(str)]
    judul: str
    tipe: TipeModul
    link: str
    thumbnail: Optional[str] = None
    tingkat: Tingkat
    id_mapel: MataPelajaranResponse
    pembuat: UserResponse
    tahun_ajaran: TahunAjaranResponse
    id_jurusan: Jurusan
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = None

    class Config:
        from_attributes = True
