from .timestamp import TimestampDocument
from schemas import MataPelajaranCreated, Jurusan


class MataPelajaranModel(TimestampDocument, MataPelajaranCreated):
    id_jurusan: Jurusan

    class Settings:
        name = "mata_pelajaran"
        indexes = ["deleted_at"]
