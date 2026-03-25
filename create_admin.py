import asyncio
from database import init_db
from models import UsersModel
from schemas.users import UserRole
from core import get_password_hash


async def create_admin():
    await init_db()

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
