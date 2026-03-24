from .timestamp import TimestampDocument
from schemas import UserRole, UsersCreated


class UsersModel(TimestampDocument, UsersCreated):
    avatar_url: str
    role: UserRole

    class Settings:
        name = "users"
        indexes = ["deleted_at"]
