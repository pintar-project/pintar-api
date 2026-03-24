from models import ModulModel
from .database import Database


class ModulRepository(Database):
    async def insert(self, **kwargs):
        data_modul = ModulModel(**kwargs)
        await data_modul.insert()
        return data_modul

    async def get(self, category, **kwargs):
        pass

    async def update(self, category, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass
