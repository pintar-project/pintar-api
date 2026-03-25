import asyncio
from database import init_db
from models import MataPelajaranModel, KelasModel
from schemas.jurusan import Jurusan


async def create_mapel():
    await init_db()

    existing_mapel = await MataPelajaranModel.find_one({"nama_mapel": "Sosiologi"})
    if not existing_mapel:
        mapel = MataPelajaranModel(
            nama_mapel="Sosiologi",
            kode_mapel="SOS",
            deskripsi="Mata Pelajaran Sosiologi",
            id_jurusan=Jurusan.IPS,
        )
        await mapel.insert()
        print("Mata Pelajaran Sosiologi created successfully!")
        existing_mapel = mapel
    else:
        print("Mata Pelajaran Sosiologi already exists!")

    target_kelas = await KelasModel.find_one(KelasModel.kode_unik == "984RFR")
    if target_kelas:
        mapel_ids = [str(m.ref.id if hasattr(m, "ref") else m.id) for m in target_kelas.daftar_mapel]
        if str(existing_mapel.id) not in mapel_ids:
            target_kelas.daftar_mapel.append(existing_mapel)
            await target_kelas.save()
            print(
                f"Mata Pelajaran Sosiologi terhubung ke kelas {target_kelas.nama} (984RFR)"
            )
        else:
            print(
                f"Mata Pelajaran Sosiologi sudah terhubung ke kelas {target_kelas.nama} (984RFR)"
            )
    else:
        print("Kelas dengan kode 984RFR tidak ditemukan!")


if __name__ == "__main__":
    asyncio.run(create_mapel())
