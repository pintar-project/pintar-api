import asyncio
from database import init_db
from repositories.kelas import KelasRepository
from models import KelasModel

async def test():
    await init_db()
    from repositories.kelas import KelasRepository
    repo = KelasRepository()
    try:
        from models import UsersModel
        guru = await UsersModel.find_one(UsersModel.role == "guru")
        if not guru:
            print("No guru found!")
            return
        print(f"Testing insert with guru: {guru.nama_lengkap} ({guru.id})")
        new_kelas = await repo.insert(id_guru=str(guru.id), nama="XII MIPA 1", deskripsi="Test")
        print(f"Success! Created kelas: {new_kelas.nama} with kode: {new_kelas.kode_unik}")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
