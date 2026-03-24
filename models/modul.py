from beanie import Link
from .timestamp import TimestampDocument
from schemas import ModulCreated, TipeModul, Jurusan
from .users import UsersModel
from .mata_pelajaran import MataPelajaranModel
from .tahun_ajaran import TahunAjaranModel
from typing import Optional


class ModulModel(TimestampDocument, ModulCreated):
    tipe: TipeModul
    thumbnail: Optional[str] = None
    id_mapel: Link[MataPelajaranModel]
    pembuat: Link[UsersModel]
    tahun_ajaran: Link[TahunAjaranModel]
    id_jurusan: Jurusan

    class Settings:
        name = "modul"
        indexes = ["deleted_at"]
