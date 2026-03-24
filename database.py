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


import os

async def init_db():
    mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/pintar-project")
    client = AsyncIOMotorClient(mongodb_uri)

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
