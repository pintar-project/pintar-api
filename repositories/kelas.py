from models import KelasModel, TahunAjaranModel, UsersModel, ModulModel
from .database import Database
import random
import string


class KelasRepository(Database):
    async def insert(self, id_guru, nama, deskripsi, tingkat, id_jurusan=None):
        tahun_aktif = await TahunAjaranModel.find_one(
            TahunAjaranModel.is_active == True
        )
        if not tahun_aktif:
            return {"error": "Tidak ada tahun ajaran yang aktif saat ini."}
        guru = await UsersModel.get(id_guru)
        if not guru or guru.role != "guru":
            return {"error": "User bukan guru atau tidak ditemukan."}
        while True:
            kode = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            kode_ada = await KelasModel.find_one(KelasModel.kode_unik == kode)
            if not kode_ada:
                break
        new_kelas = KelasModel(
            nama=nama,
            deskripsi=deskripsi,
            tingkat=tingkat,
            kode_unik=kode,
            pembuat=guru,
            tahun_ajaran=tahun_aktif,
            id_jurusan=id_jurusan,
            peserta=[],
        )
        await new_kelas.insert()
        return new_kelas

    async def get(self, category, **kwargs):
        kode_kelas = kwargs.get("kode_kelas")
        if category == "get_all_kelas":
            tahun_aktif = await TahunAjaranModel.find_one(
                TahunAjaranModel.is_active == True
            )
            if not tahun_aktif:
                return []
            daftar_kelas = await KelasModel.find(
                {"tahun_ajaran.$id": tahun_aktif.id}
            ).to_list()
            for kelas in daftar_kelas:
                if kelas.pembuat and not isinstance(kelas.pembuat, UsersModel):
                    guru_id = (
                        kelas.pembuat.ref.id
                        if hasattr(kelas.pembuat, "ref")
                        else (
                            kelas.pembuat.id
                            if hasattr(kelas.pembuat, "id")
                            else kelas.pembuat
                        )
                    )
                    kelas.pembuat = await UsersModel.get(guru_id)
                if kelas.tahun_ajaran and not isinstance(
                    kelas.tahun_ajaran, TahunAjaranModel
                ):
                    ta_id = (
                        kelas.tahun_ajaran.ref.id
                        if hasattr(kelas.tahun_ajaran, "ref")
                        else (
                            kelas.tahun_ajaran.id
                            if hasattr(kelas.tahun_ajaran, "id")
                            else kelas.tahun_ajaran
                        )
                    )
                    kelas.tahun_ajaran = await TahunAjaranModel.get(ta_id)

                if kelas.peserta:
                    resolved_peserta = []
                    for p in kelas.peserta:
                        user_id = (
                            p.ref.id
                            if hasattr(p, "ref")
                            else p.id if hasattr(p, "id") else p
                        )
                        user = await UsersModel.get(user_id)
                        if user:
                            resolved_peserta.append(user)
                    kelas.peserta = resolved_peserta

                if kelas.daftar_mapel:
                    resolved_mapel = []
                    for m in kelas.daftar_mapel:
                        mapel = m
                        if hasattr(m, "fetch"):
                            mapel = await m.fetch()
                        if mapel:
                            resolved_mapel.append(mapel)
                    kelas.daftar_mapel = resolved_mapel

                if kelas.daftar_modul:
                    resolved_modul = []
                    for m in kelas.daftar_modul:
                        modul = m
                        if hasattr(m, "fetch"):
                            modul = await m.fetch()

                        if modul and isinstance(modul, ModulModel):
                            if hasattr(modul.id_mapel, "fetch"):
                                modul.id_mapel = await modul.id_mapel.fetch()
                            if hasattr(modul.pembuat, "fetch"):
                                modul.pembuat = await modul.pembuat.fetch()
                            if hasattr(modul.tahun_ajaran, "fetch"):
                                modul.tahun_ajaran = await modul.tahun_ajaran.fetch()
                            resolved_modul.append(modul)
                    kelas.daftar_modul = resolved_modul
            return daftar_kelas
        if category == "get_kelas_by_kode_kelas":
            kelas = await KelasModel.find_one(KelasModel.kode_unik == kode_kelas)
            if kelas:
                if kelas.pembuat and not isinstance(kelas.pembuat, UsersModel):
                    guru_id = (
                        kelas.pembuat.ref.id
                        if hasattr(kelas.pembuat, "ref")
                        else (
                            kelas.pembuat.id
                            if hasattr(kelas.pembuat, "id")
                            else kelas.pembuat
                        )
                    )
                    kelas.pembuat = await UsersModel.get(guru_id)

                if kelas.tahun_ajaran and not isinstance(
                    kelas.tahun_ajaran, TahunAjaranModel
                ):
                    ta_id = (
                        kelas.tahun_ajaran.ref.id
                        if hasattr(kelas.tahun_ajaran, "ref")
                        else (
                            kelas.tahun_ajaran.id
                            if hasattr(kelas.tahun_ajaran, "id")
                            else kelas.tahun_ajaran
                        )
                    )
                    kelas.tahun_ajaran = await TahunAjaranModel.get(ta_id)

                if kelas.peserta:
                    resolved_peserta = []
                    for p in kelas.peserta:
                        user_id = (
                            p.ref.id
                            if hasattr(p, "ref")
                            else p.id if hasattr(p, "id") else p
                        )
                        user = await UsersModel.get(user_id)
                        if user:
                            resolved_peserta.append(user)
                    kelas.peserta = resolved_peserta

                if kelas.daftar_mapel:
                    resolved_mapel = []
                    for m in kelas.daftar_mapel:
                        mapel = m
                        if hasattr(m, "fetch"):
                            mapel = await m.fetch()
                        if mapel:
                            resolved_mapel.append(mapel)
                    kelas.daftar_mapel = resolved_mapel

                if kelas.daftar_modul:
                    resolved_modul = []
                    for m in kelas.daftar_modul:
                        modul = m
                        if hasattr(m, "fetch"):
                            modul = await m.fetch()

                        if modul and isinstance(modul, ModulModel):
                            if hasattr(modul.id_mapel, "fetch"):
                                modul.id_mapel = await modul.id_mapel.fetch()
                            if hasattr(modul.pembuat, "fetch"):
                                modul.pembuat = await modul.pembuat.fetch()
                            if hasattr(modul.tahun_ajaran, "fetch"):
                                modul.tahun_ajaran = await modul.tahun_ajaran.fetch()
                            resolved_modul.append(modul)
                    kelas.daftar_modul = resolved_modul

            return kelas

    async def update(self, category, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass
