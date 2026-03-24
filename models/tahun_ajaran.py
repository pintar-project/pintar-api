from .timestamp import TimestampDocument
from schemas import TahunAjaranCreated


class TahunAjaranModel(TimestampDocument, TahunAjaranCreated):
    is_active: bool = False

    class Settings:
        name = "tahun_ajaran"
        indexes = ["deleted_at"]
