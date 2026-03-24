import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import UsersModel, TaskModel, TahunAjaranModel, KelasModel, ModulModel


async def buat_tahun_ajaran(nama_tahun: str, semester: int, set_aktif: bool = False):
    client = AsyncIOMotorClient("mongodb://localhost:27017/pintar-project")
    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            TaskModel,
            UsersModel,
            TahunAjaranModel,
            KelasModel,
            ModulModel,
        ],
    )

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
