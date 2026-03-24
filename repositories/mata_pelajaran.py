from models import MataPelajaranModel
from .database import Database


class MataPelajaranRepository(Database):
    async def insert(self, **kwargs):
        new_mapel = MataPelajaranModel(**kwargs)
        await new_mapel.insert()
        return new_mapel

    async def get(self, category, **kwargs):
        kode_mapel = kwargs.get("kode_mapel")
        id = kwargs.get("id")
        if category == "get_by_id":
            return await MataPelajaranModel.get(id)
        elif category == "get_by_code":
            return await MataPelajaranModel.find_one({"kode_mapel": kode_mapel})

    async def update(self, category, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass
