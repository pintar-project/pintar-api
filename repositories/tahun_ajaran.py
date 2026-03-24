from models import TahunAjaranModel
from .database import Database


class TahunAjaranRepository(Database):
    async def insert(self, nama, semester):
        await TahunAjaranModel.find({"is_active": True}).set({"is_active": False})
        tahun_ajaran = TahunAjaranModel(nama=nama, semester=semester, is_active=True)
        await tahun_ajaran.insert()
        return tahun_ajaran

    async def get(self, category, **kwargs):
        if category == "get_tahun_ajaran":
            return await TahunAjaranModel.find_one({"is_active": True})

    async def update(self, category, **kwargs):
        id = kwargs.get("id")
        is_active = kwargs.get("is_active")
        if category == "update_tahun_ajaran_by_id":
            await TahunAjaranModel.find({"is_active": True}).set({"is_active": False})
            data_tahun_ajaran = await TahunAjaranModel.get(id)
            if not data_tahun_ajaran:
                return None
            data_tahun_ajaran.is_active = is_active
            await data_tahun_ajaran.save()
            return data_tahun_ajaran

    async def delete(self, **kwargs):
        pass
