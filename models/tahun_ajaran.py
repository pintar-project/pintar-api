from .timestamp import TimestampDocument
from schemas import TahunAjaranCreated
from pymongo import IndexModel, ASCENDING


class TahunAjaranModel(TimestampDocument, TahunAjaranCreated):
    is_active: bool = False

    class Settings:
        name = "tahun_ajaran"
        indexes = [
            IndexModel([("nama", ASCENDING), ("semester", ASCENDING)], unique=True),
            "deleted_at"
        ]
