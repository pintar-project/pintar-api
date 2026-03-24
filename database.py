from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import (
    TaskModel,
    UsersModel,
    TahunAjaranModel,
    KelasModel,
    SiswaProfileModel,
)


async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017/pintar-project")

    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            TaskModel,
            UsersModel,
            TahunAjaranModel,
            KelasModel,
            SiswaProfileModel,
        ],
    )
