from repositories import UsersRepository
from fastapi import Request, HTTPException, status
from pymongo.errors import DuplicateKeyError


from core import get_password_hash


class UsersController:
    def __init__(self):
        self.repo = UsersRepository()

    async def create_user(self, user_data: dict, request: Request, role: str):
        avatar_url = request.url_for("get_avatar")
        user_data["avatar_url"] = str(avatar_url)
        user_data["role"] = role
        if "password" in user_data and user_data["password"]:
            user_data["password"] = get_password_hash(user_data["password"])
        try:
            users = await self.repo.insert(**user_data)
            return {
                "message": "users berhasil dibuat",
                "data": users,
            }
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email sudah terdaftar",
            )
