import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import UsersModel, SiswaProfileModel, TaskModel, UserRole, KelasModel, TahunAjaranModel

async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017/pinter-project")
    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            TaskModel,
            UsersModel,
            SiswaProfileModel,
            KelasModel,
            TahunAjaranModel,
        ],
    )
    profiles = await SiswaProfileModel.find_all().to_list()
    for p in profiles[:1]:
        await p.fetch_link(SiswaProfileModel.user)
        print("Fetched user:", p.user.username)

if __name__ == "__main__":
    asyncio.run(main())
