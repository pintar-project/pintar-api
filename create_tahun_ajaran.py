import asyncio
from database import init_db
from models import TahunAjaranModel


async def buat_tahun_ajaran(nama_tahun: str, semester: int, set_aktif: bool = False):
    await init_db()

    if set_aktif:
        print(f"Mengaktifkan {nama_tahun}, menonaktifkan tahun ajaran lain...")
        await TahunAjaranModel.find(TahunAjaranModel.is_active == True).update(
            {"$set": {"is_active": False}}
        )

    tahun_baru = TahunAjaranModel(
        nama=nama_tahun, semester=semester, is_active=set_aktif
    )
    try:
        await tahun_baru.insert()
        print(f"Tahun ajaran {nama_tahun} berhasil dibuat!")
        return tahun_baru
    except Exception:
        # Menangani jika nama tahun ajaran sudah ada (Duplicate Key Error)
        print(f"Tahun ajaran {nama_tahun} sudah terdaftar. Mengupdate status aktif...")
        existing = await TahunAjaranModel.find_one(TahunAjaranModel.nama == nama_tahun)
        if existing:
            existing.semester = semester
            existing.is_active = set_aktif
            await existing.save()
            print(f"Tahun ajaran {nama_tahun} berhasil diupdate!")
            return existing
        return {"error": f"Gagal mengupdate atau membuat tahun ajaran {nama_tahun}."}


if __name__ == "__main__":
    asyncio.run(buat_tahun_ajaran("2026/2027", semester=1, set_aktif=True))
