from pydantic import BaseModel, BeforeValidator
from typing import Annotated, Optional
from .jurusan import Jurusan


class MataPelajaranCreated(BaseModel):
    nama_mapel: str
    kode_mapel: str
    deskripsi: str


class MataPelajaranResponse(BaseModel):
    id: Annotated[str, BeforeValidator(str)]
    nama_mapel: str
    kode_mapel: str
    deskripsi: str
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = None
    id_jurusan: Jurusan

    class Config:
        from_attributes = True
