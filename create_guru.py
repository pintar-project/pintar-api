import asyncio
from database import init_db
from models import UsersModel
from schemas.users import UserRole
from core import get_password_hash


async def create_guru():
    await init_db()

    existing_guru = await UsersModel.find_one({"email": "guru@gmail.com"})
    if existing_guru:
        print("Guru user already exists!")
        return

    guru_user = UsersModel(
        username="guru_prod",
        nama_lengkap="Guru Pengajar",
        email="guru@gmail.com",
        password=get_password_hash("password123"),
        avatar_url="http://localhost:8000/users/avatar",
        role=UserRole.GURU,
    )

    await guru_user.insert()
    print("Guru user created successfully!")
    print("Email: guru@gmail.com")
    print("Password: password123")


if __name__ == "__main__":
    asyncio.run(create_guru())
