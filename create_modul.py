import asyncio
from database import init_db
from models import ModulModel, MataPelajaranModel, UsersModel, TahunAjaranModel, KelasModel
from schemas.jurusan import Jurusan

async def create_modul():
    await init_db()
    
    # Prasyarat
    mapel = await MataPelajaranModel.find_one({"nama_mapel": "Sosiologi"})
    admin = await UsersModel.find_one({"email": "admin_prod@gmail.com"})
    tahun = await TahunAjaranModel.find_one({"is_active": True})
    kelas = await KelasModel.find_one({"kode_unik": "984RFR"})
    
    if not all([mapel, admin, tahun, kelas]):
        print("Error: Mapel, Admin, Tahun, or Kelas not found. Run other scripts first.")
        return

    modul_data = [
        {
            "judul": "CONTOH MODUL AJAR SOSIOLOGI XI IPS 2",
            "link": "https://res.cloudinary.com/ducs7evff/image/upload/v1774371360/module/thumbnails/fxpz0fvaajlktexemtmx.pdf",
            "tingkat": "XI",
            "tipe": "file",
            "thumbnail": "https://res.cloudinary.com/ducs7evff/image/upload/c_limit,h_450,pg_1,w_300/v1/module/thumbnails/fxpz0fvaajlktexemtmx.jpg",
            "id_mapel": mapel,
            "pembuat": admin,
            "tahun_ajaran": tahun,
            "id_jurusan": Jurusan.IPS
        },
        {
            "judul": "MODUL AJAR SOSIOLOGI KELAS XI",
            "link": "https://res.cloudinary.com/ducs7evff/image/upload/v1774371388/module/thumbnails/xwjh20cazgeboddyicqy.pdf",
            "tingkat": "XI",
            "tipe": "file",
            "thumbnail": "https://res.cloudinary.com/ducs7evff/image/upload/c_limit,h_450,pg_1,w_300/v1/module/thumbnails/xwjh20cazgeboddyicqy.jpg",
            "id_mapel": mapel,
            "pembuat": admin,
            "tahun_ajaran": tahun,
            "id_jurusan": Jurusan.IPS
        }
    ]

    for data in modul_data:
        existing = await ModulModel.find_one({"judul": data["judul"]})
        if not existing:
            modul = ModulModel(**data)
            await modul.insert()
            print(f"Modul '{data['judul']}' created successfully!")
            
            # Link to class
            if modul not in kelas.daftar_modul:
                kelas.daftar_modul.append(modul)
        else:
            print(f"Modul '{data['judul']}' already exists!")

    await kelas.save()
    print("Modul linked to kelas XI IPS 2.")

if __name__ == "__main__":
    asyncio.run(create_modul())
