from pydantic import BaseModel, BeforeValidator
from .users import UserResponse
from .tahun_ajaran import TahunAjaranResponse
from .mata_pelajaran import MataPelajaranResponse
from .modul import ModulResponse
from .jurusan import Jurusan
from .tingkat import Tingkat
from typing import List, Annotated, Optional


class KelasCreated(BaseModel):
    nama: str
    deskripsi: str


class KelasResponse(BaseModel):
    id: Annotated[str, BeforeValidator(str)]
    nama: str
    deskripsi: str
    tingkat: Tingkat
    kode_unik: str
    created_at: int
    updated_at: int
    deleted_at: Optional[int] = None
    pembuat: UserResponse
    peserta: List[UserResponse] = []
    tahun_ajaran: TahunAjaranResponse
    id_jurusan: Jurusan
    daftar_mapel: List[MataPelajaranResponse] = []
    daftar_modul: List[ModulResponse] = []

    class Config:
        from_attributes = True
