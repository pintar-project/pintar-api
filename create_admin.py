import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from schemas.users import UserRole
from models import (
    UsersModel, TaskModel, TahunAjaranModel, KelasModel,
    ModulModel, MataPelajaranModel, SiswaProfileModel
)
from core import get_password_hash


async def create_admin():
    client = AsyncIOMotorClient("mongodb://localhost:27017/pintar-project")
    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            TaskModel, UsersModel, TahunAjaranModel, KelasModel,
            ModulModel, MataPelajaranModel, SiswaProfileModel
        ],
    )

    existing_admin = await UsersModel.find_one({"email": "admin_prod@gmail.com"})
    if existing_admin:
        print("Admin user already exists!")
        return

    admin_user = UsersModel(
        username="admin_prod",
        nama_lengkap="Administrator",
        email="admin_prod@gmail.com",
        password=get_password_hash("password123"),
        avatar_url="http://localhost:8000/users/avatar",
        role=UserRole.ADMIN,
    )

    await admin_user.insert()
    print("Admin user created successfully!")
    print("Email: admin_prod@gmail.com")
    print("Password: password123")


if __name__ == "__main__":
    asyncio.run(create_admin())
