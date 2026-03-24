from beanie import Link
from .timestamp import TimestampDocument
from schemas import SiswaProfileCreated, Jurusan
from .users import UsersModel


class SiswaProfileModel(TimestampDocument, SiswaProfileCreated):
    user: Link[UsersModel]
    id_jurusan: Jurusan

    class Settings:
        name = "siswa"
        indexes = ["deleted_at"]
