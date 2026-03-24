from repositories import UsersRepository
from fastapi import Request, HTTPException, status
from pymongo.errors import DuplicateKeyError


class UsersConroller:
    def __init__(self):
        self.repo = UsersRepository()

    async def create_user(self, user_data: dict, request: Request, role: str):
        avatar_url = request.url_for("get_avatar")
        user_data["avatar_url"] = str(avatar_url)
        user_data["role"] = role
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
