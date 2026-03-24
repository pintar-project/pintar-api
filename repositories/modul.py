from models import ModulModel
from .database import Database
from beanie import PydanticObjectId
from models import MataPelajaranModel
import re


class ModulRepository(Database):
    async def insert(self, **kwargs):
        kode_kelas = kwargs.pop("kode_kelas", None)
        data_modul = ModulModel(**kwargs)
        await data_modul.insert()

        if kode_kelas:
            from models import KelasModel

            kelas = await KelasModel.find_one(KelasModel.kode_unik == kode_kelas)
            if not kelas and PydanticObjectId.is_valid(kode_kelas):
                kelas = await KelasModel.get(kode_kelas)

            if kelas:
                if kelas.daftar_modul is None:
                    kelas.daftar_modul = []
                kelas.daftar_modul.append(data_modul)
                await kelas.save()

        return data_modul

    async def get(self, category, **kwargs):

        tahun_ajaran = kwargs.get("tahun_ajaran")
        tingkat = kwargs.get("tingkat")
        nama_mapel = kwargs.get("nama_mapel")

        if category == "get_all_active_ta":
            moduls = await ModulModel.find(
                {"tahun_ajaran.$id": tahun_ajaran.id, "deleted_at": None}
            ).to_list()

            for modul in moduls:
                if hasattr(modul.id_mapel, "fetch"):
                    modul.id_mapel = await modul.id_mapel.fetch()
                if hasattr(modul.pembuat, "fetch"):
                    modul.pembuat = await modul.pembuat.fetch()
                if hasattr(modul.tahun_ajaran, "fetch"):
                    modul.tahun_ajaran = await modul.tahun_ajaran.fetch()

            return moduls

        if category == "get_by_filter":

            mapels = await MataPelajaranModel.find(
                {"nama_mapel": re.compile(f"^{re.escape(nama_mapel)}$", re.IGNORECASE)}
            ).to_list()

            if not mapels:
                return []

            mapel_ids = [m.id for m in mapels]

            moduls = await ModulModel.find(
                {
                    "tahun_ajaran.$id": tahun_ajaran.id,
                    "tingkat": tingkat,
                    "id_mapel.$id": {"$in": mapel_ids},
                    "deleted_at": None,
                }
            ).to_list()

            for modul in moduls:
                if hasattr(modul.id_mapel, "fetch"):
                    modul.id_mapel = await modul.id_mapel.fetch()
                if hasattr(modul.pembuat, "fetch"):
                    modul.pembuat = await modul.pembuat.fetch()
                if hasattr(modul.tahun_ajaran, "fetch"):
                    modul.tahun_ajaran = await modul.tahun_ajaran.fetch()

            return moduls

    async def update(self, category, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass
