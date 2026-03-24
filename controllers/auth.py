from repositories import UsersRepository
from fastapi import HTTPException, status
from core import verify_password, JwtToken, get_password_hash
import datetime
from models import UserResponse, UserRole


class AuthController:
    def __init__(self):
        self.repo = UsersRepository()
        self.jwt_token = JwtToken()

    async def user_login(self, user_data: dict):
        email = user_data["email"]
        user_database = await self.repo.get("get_user_by_email", email=email)
        password_verif = verify_password(user_data["password"], user_database.password)
        if not password_verif:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="password/email salah",
            )

        token = self.jwt_token.generate_jwt(
            str(user_database.id), datetime.datetime.now(datetime.timezone.utc)
        )

        return {
            "message": "oke",
            "data": user_database,
            "token": {"access_token": token},
        }

    async def user_me(self, current_user: UserResponse):
        return {"message": "oke", "data": current_user}

    async def create_guru(self, user_data: dict, current_user: UserResponse):
        if not current_user.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="kamu tidak punya akses untuk membuat guru",
            )
        user_data["password"] = get_password_hash(user_data["password"])
        user_data["avatar_url"] = "http://localhost:8000/users/avatar"
        await self.repo.update("create_guru", **user_data)
        return {"message": "oke", "data": current_user}

    async def create_siswa(self, user_data: dict, current_user: UserResponse):
        if not current_user.role == UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="kamu tidak punya akses untuk membuat siswa",
            )
        user_data["password"] = get_password_hash(user_data["password"])
        user_data["avatar_url"] = "http://localhost:8000/users/avatar"
        await self.repo.update("create_siswa", **user_data)
        return {"message": "oke", "data": current_user}
