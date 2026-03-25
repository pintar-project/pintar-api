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

    # 2. Buat dokumen baru
    tahun_baru = TahunAjaranModel(
        nama=nama_tahun, semester=semester, is_active=set_aktif
    )

    # 3. Simpan ke database
    try:
        await tahun_baru.insert()
        print(f"Tahun ajaran {nama_tahun} berhasil dibuat!")
        return tahun_baru
    except Exception as e:
        # Menangani jika nama tahun ajaran sudah ada (Duplicate Key Error)
        print(f"Error: Tahun ajaran {nama_tahun} sudah terdaftar.")
        return {"error": f"Tahun ajaran {nama_tahun} sudah terdaftar."}


if __name__ == "__main__":
    # Contoh penggunaan
    asyncio.run(buat_tahun_ajaran("2026/2027", semester=1, set_aktif=True))
