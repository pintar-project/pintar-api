import asyncio
from database import init_db
from models import KelasModel, UsersModel, TahunAjaranModel
from schemas.jurusan import Jurusan

async def create_kelas_ips():
    await init_db()
    
    # Ensure active tahun ajaran exists
    tahun = await TahunAjaranModel.find_one(TahunAjaranModel.is_active == True)
    if not tahun:
        print("Error: No active Tahun Ajaran found. Please run create_tahun_ajaran.py first.")
        return

    # Ensure guru exists
    guru = await UsersModel.find_one(UsersModel.email == "guru@gmail.com")
    if not guru:
        print("Error: Guru not found. Please run create_guru.py first.")
        return

    existing_kelas = await KelasModel.find_one(KelasModel.kode_unik == "984RFR")
    if existing_kelas:
        print("Kelas XI IPS 2 already exists!")
        return

    new_kelas = KelasModel(
        nama="XI IPS 2",
        deskripsi="Kelas XI IPS 2",
        tingkat="XI",
        pembuat=guru,
        kode_unik="984RFR",
        id_jurusan=Jurusan.IPS,
        tahun_ajaran=tahun
    )
    
    await new_kelas.insert()
    print("Success! Created kelas: XI IPS 2 with kode: 984RFR")

if __name__ == "__main__":
    asyncio.run(create_kelas_ips())
