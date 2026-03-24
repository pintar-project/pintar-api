from repositories import TahunAjaranRepository
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException


from models import TahunAjaranModel


class TahunAjaranController:
    def __init__(self):
        self.repo = TahunAjaranRepository()

    async def tahun_ajaran_is_active(self, id: str, user_in: dict):
        try:
            # Pindahkan logika deaktifasi ke controller
            if user_in["is_active"]:
                await TahunAjaranModel.find({"is_active": True}).set({"is_active": False})
            
            tahun_ajaran_data = await self.repo.update(
                id, is_active=user_in["is_active"]
            )
            if not tahun_ajaran_data:
                raise HTTPException(
                    status_code=404, detail="tahun ajaran tidak ditemukan"
                )
            return {"message": "success", "data": tahun_ajaran_data}
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail="tahun ajaran sudah ada")

    async def create_tahun_ajaran(self, user_in: dict):
        try:
            # Set all other to inactive if this one is active (default True in repo before)
            # We'll make it explicit here.
            await TahunAjaranModel.find({"is_active": True}).set({"is_active": False})
            
            tahun_ajaran_data = await self.repo.insert(
                nama=user_in["nama"], semester=user_in["semester"], is_active=True
            )
            return {"message": "success", "data": tahun_ajaran_data}
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail="tahun ajaran sudah ada")

    async def get_tahun_ajaran(self):
        tahun_ajaran_data = await self.repo.get("get_tahun_ajaran")
        if not tahun_ajaran_data:
            raise HTTPException(status_code=404, detail="tahun ajaran tidak ditemukan")
        return {"message": "success", "data": tahun_ajaran_data}
