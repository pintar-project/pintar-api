import asyncio
from database import init_db
from models import TahunAjaranModel


async def buat_tahun_ajaran(nama_tahun: str, semester: int, set_aktif: bool = False):
    await init_db()

    # Use nama_tahun as 'nama' for consistency with the model
    nama = nama_tahun

    # Consolidate duplicates: delete all but the one we'll use
    all_duplicates = await TahunAjaranModel.find(
        TahunAjaranModel.nama == nama, TahunAjaranModel.semester == semester
    ).to_list()
    
    if len(all_duplicates) > 1:
        print(f"Found {len(all_duplicates)} duplicates for {nama} Sem {semester}. Cleaning up...")
        to_keep = all_duplicates[0]
        for duplicate in all_duplicates[1:]:
            await duplicate.delete()
        existing = to_keep
    elif len(all_duplicates) == 1:
        existing = all_duplicates[0]
    else:
        existing = None

    if not existing:
        print(f"Creating new Tahun Ajaran {nama} Semester {semester}...")
        existing = TahunAjaranModel(nama=nama, semester=semester, is_active=set_aktif)
        await existing.insert()
    else:
        print(f"Tahun Ajaran {nama} Semester {semester} already exists. Using existing record.")
    
    if set_aktif:
        # Deactivate all OTHER years
        await TahunAjaranModel.find(TahunAjaranModel.id != existing.id).update(
            {"$set": {"is_active": False}}
        )
        existing.is_active = True
        await existing.save()
        print(f"Tahun Ajaran {nama} Semester {semester} set to ACTIVE.")
    
    return existing


if __name__ == "__main__":
    # Contoh penggunaan
    asyncio.run(buat_tahun_ajaran("2026/2027", semester=1, set_aktif=True))
