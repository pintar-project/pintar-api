from models import TahunAjaranModel
from .database import Database


class TahunAjaranRepository(Database):
    async def insert(self, **kwargs):
        tahun_ajaran = TahunAjaranModel(**kwargs)
        await tahun_ajaran.insert()
        return tahun_ajaran

    async def get(self, category, **kwargs):
        id = kwargs.get("id")
        if category == "get_tahun_ajaran":
            active = await TahunAjaranModel.find_one({"is_active": True})
            if active:
                return active
            # Fallback to the latest one if no active found
            return await TahunAjaranModel.find_all().sort("-created_at").first_or_none()
        if category == "get_all":
            return await TahunAjaranModel.find_all().to_list()
        if category == "get_by_id":
            return await TahunAjaranModel.get(id)

    async def update(self, id, **kwargs):
        data_tahun_ajaran = await TahunAjaranModel.get(id)
        if not data_tahun_ajaran:
            return None
        for key, value in kwargs.items():
            setattr(data_tahun_ajaran, key, value)
        await data_tahun_ajaran.save()
        return data_tahun_ajaran

    async def delete(self, **kwargs):
        pass
