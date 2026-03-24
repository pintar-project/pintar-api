from repositories import ModulRepository
from models import TipeModul
from fastapi import Request, HTTPException, status
from pymongo.errors import DuplicateKeyError
from services.cloudinary import upload_file


class ModulController:
    def __init__(self):
        self.repo = ModulRepository()

    async def create_modul(self, user_in, current_user):
        print(user_in)
        if user_in["file_modul"].content_type != "application/pdf":
            raise HTTPException(
                status_code=400, detail="hanya file pdf yang diperbolehkan"
            )
        result = upload_file("module", user_in["file_modul"].file)
        await self.repo.insert(
            id_kelas=user_in["id_kelas"],
            judul=user_in["judul"],
            link=result["url"],
            tipe=TipeModul.FILE,
        )
        return {"message": "success", "data": None}
