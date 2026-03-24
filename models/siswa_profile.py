from typing import Optional, Annotated
from beanie import Link, Indexed
from pydantic import BaseModel, BeforeValidator
from .users import UsersModel, UserResponse
from .timestamp import TimestampDocument


class SiswaProfileCreated(BaseModel):
    gaya_belajar: Optional[str] = None
    kognitif: Optional[str] = None
    keaktifan: Optional[str] = None
    id_siswa: str = Indexed(unique=True)


class SiswaProfileResponse(SiswaProfileCreated):
    id: Annotated[str, BeforeValidator(str)]
    user: UserResponse


class SiswaProfileModel(TimestampDocument, SiswaProfileCreated):
    user: Link[UsersModel]

    class Settings:
        name = "siswa"
        indexes = ["deleted_at"]
