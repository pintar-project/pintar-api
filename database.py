from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import (
    TaskModel,
    UsersModel,
    TahunAjaranModel,
    MataPelajaranModel,
    KelasModel,
    ModulModel,
    SiswaProfileModel,
)
from core import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)

    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            TaskModel,
            UsersModel,
            TahunAjaranModel,
            MataPelajaranModel,
            KelasModel,
            ModulModel,
            SiswaProfileModel,
        ],
    )
