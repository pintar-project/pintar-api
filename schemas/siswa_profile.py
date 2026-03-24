from typing import Optional, Annotated
from pydantic import BaseModel, BeforeValidator
from .users import UserResponse, UsersCreated
from .jurusan import Jurusan


class SiswaProfileCreated(BaseModel):
    id_siswa: str
    gaya_belajar: Optional[str] = None
    kognitif: Optional[str] = None
    keaktifan: Optional[str] = None


class SiswaCreated(UsersCreated, SiswaProfileCreated):
    id_jurusan: Jurusan


class SiswaProfileResponse(SiswaProfileCreated):
    id: Annotated[str, BeforeValidator(str)]
    user: UserResponse
    id_jurusan: Jurusan
