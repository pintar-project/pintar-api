from repositories import KelasRepository
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError
from models import UserRole


class KelasController:
    def __init__(self):
        self.repo = KelasRepository()

    async def get_kelas_by_kode(self, kode_kelas: str):
        data = await self.repo.get("get_kelas_by_kode_kelas", kode_kelas=kode_kelas)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="kelas tidak ditemukan",
            )
        return {"message": "success", "data": data}

    async def get_all_kelas(self):
        data = await self.repo.get("get_all_kelas")
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="tidak ada kelas yang tersedia",
            )
        return {"message": "success", "data": data}

    async def create_kelas(self, user_in, current_user):
        if not current_user.role == UserRole.GURU:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="anda tidak memiliki akses untuk membuat kelas",
            )
        try:
            data = await self.repo.insert(
                f"{current_user.id}", user_in["nama"], user_in["deskripsi"]
            )
            if isinstance(data, dict) and "error" in data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=data["error"],
                )
            return {"message": "success", "data": data}
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="kelas sudah ada",
            )
