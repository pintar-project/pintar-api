from beanie import Indexed, Link
from .timestamp import TimestampDocument
from schemas import KelasCreated, Jurusan, Tingkat
from .users import UsersModel
from typing import List
from .tahun_ajaran import TahunAjaranModel
from .mata_pelajaran import MataPelajaranModel
from .modul import ModulModel


class KelasModel(TimestampDocument, KelasCreated):
    tingkat: Tingkat
    pembuat: Link[UsersModel]
    kode_unik: str = Indexed(unique=True)
    peserta: List[Link[UsersModel]] = []
    tahun_ajaran: Link[TahunAjaranModel]
    id_jurusan: Jurusan
    daftar_mapel: List[Link[MataPelajaranModel]] = []
    daftar_modul: List[Link[ModulModel]] = []

    class Settings:
        name = "kelas"
        indexes = ["deleted_at"]
