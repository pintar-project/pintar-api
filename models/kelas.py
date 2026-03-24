from beanie import Indexed, Link
from .timestamp import TimestampDocument
from pydantic import BaseModel, BeforeValidator
from .users import UsersModel, UserResponse
from typing import List, Annotated, Optional
from datetime import datetime
from .tahun_ajaran import TahunAjaranModel, TahunAjaranResponse


class KelasCreated(BaseModel):
    nama: str
    deskripsi: str


class KelasResponse(KelasCreated):
    id: Annotated[str, BeforeValidator(str)]
    nama: str
    deskripsi: str
    kode_unik: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    pembuat: UserResponse
    peserta: List[UserResponse] = []
    tahun_ajaran: TahunAjaranResponse

    class Config:
        from_attributes = True


class KelasModel(TimestampDocument, KelasCreated):
    pembuat: Link[UsersModel]
    kode_unik: str = Indexed(unique=True)
    peserta: List[Link[UsersModel]] = []
    tahun_ajaran: Link[TahunAjaranModel]

    class Settings:
        name = "kelas"
        indexes = ["deleted_at"]
