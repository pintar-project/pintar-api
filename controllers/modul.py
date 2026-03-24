from repositories import (
    ModulRepository,
    MataPelajaranRepository,
    UsersRepository,
    TahunAjaranRepository,
)
from schemas import TipeModul, UserRole
from fastapi import HTTPException, status
from beanie import PydanticObjectId
from services import upload_pdf_with_thumbnail


class ModulController:
    def __init__(self):
        self.repo = ModulRepository()
        self.mapel_repo = MataPelajaranRepository()
        self.user_repo = UsersRepository()
        self.tahun_ajaran_repo = TahunAjaranRepository()

    async def create_modul(self, user_in, current_user):
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="hanya admin yang dapat mengupload modul",
            )
        if user_in["file_modul"].content_type != "application/pdf":
            raise HTTPException(
                status_code=400, detail="hanya file pdf yang diperbolehkan"
            )

        tahun_ajaran = await self.tahun_ajaran_repo.get("get_tahun_ajaran")
        if not tahun_ajaran:
            raise HTTPException(
                status_code=400, detail="tahun ajaran aktif tidak ditemukan"
            )

        mapel = await self.mapel_repo.get("get_by_code", kode_mapel=user_in["id_mapel"])
        if not mapel:
            if PydanticObjectId.is_valid(user_in["id_mapel"]):
                mapel = await self.mapel_repo.get("get_by_id", id=user_in["id_mapel"])

        if not mapel:
            raise HTTPException(
                status_code=404, detail="mata pelajaran tidak ditemukan"
            )
        upload_result = upload_pdf_with_thumbnail("module", user_in["file_modul"].file)
        pembuat = await self.user_repo.get("get_user_by_id", id=current_user.id)

        await self.repo.insert(
            judul=user_in["judul"],
            tingkat=user_in["tingkat"],
            link=upload_result["view_url"],
            thumbnail=upload_result["thumbnail_url"],
            tipe=TipeModul.FILE,
            id_mapel=mapel,
            pembuat=pembuat,
            tahun_ajaran=tahun_ajaran,
            id_jurusan=user_in.get("id_jurusan"),
            kode_kelas=user_in.get("kode_kelas"),
        )
        return {"message": "success", "data": None}

    async def get_all_modul(self):
        tahun_ajaran = await self.tahun_ajaran_repo.get("get_tahun_ajaran")
        if not tahun_ajaran:
            raise HTTPException(
                status_code=400, detail="tahun ajaran aktif tidak ditemukan"
            )
        moduls = await self.repo.get("get_all_active_ta", tahun_ajaran=tahun_ajaran)

        return {"message": "success", "data": moduls}

    async def get_modul_by_filter(self, tingkat, nama_mapel):
        tahun_ajaran = await self.tahun_ajaran_repo.get("get_tahun_ajaran")
        if not tahun_ajaran:
            raise HTTPException(
                status_code=400, detail="tahun ajaran aktif tidak ditemukan"
            )
        moduls = await self.repo.get(
            "get_by_filter",
            tahun_ajaran=tahun_ajaran,
            tingkat=tingkat,
            nama_mapel=nama_mapel,
        )

        return {"message": "success", "data": moduls}
