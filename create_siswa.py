import asyncio
import json
from database import init_db
from models import UsersModel, SiswaProfileModel, KelasModel
from schemas.users import UserRole
from schemas.jurusan import Jurusan
from core import get_password_hash


async def create_siswa():
    await init_db()

    # Load JSON data
    with open("data_dasbor_analitik_XI_IPS_2.json", "r") as f:
        data = json.load(f)

    target_kelas = await KelasModel.find_one(KelasModel.kode_unik == "984RFR")
    if not target_kelas:
        print("Kelas dengan kode 984RFR tidak ditemukan!")
        return

    # Clear existing participants mapping to avoid broken links after deletion
    target_kelas.peserta = []

    siswa_list = data.get("data_siswa", [])

    # Delete existing students and their profiles
    print("Deleting existing students and profiles...")
    students = await UsersModel.find({"role": UserRole.SISWA}).to_list()
    for s in students:
        await SiswaProfileModel.find({"user.id": s.id}).delete()
        await s.delete()

    for s in siswa_list:
        # Create username from id_siswa (e.g., ID-1243 -> id1243)
        username = s["id_siswa"].lower().replace("-", "")
        email = f"{username}@gmail.com"
        nama_lengkap = s["nama"]

        # Strip % from keaktifan if present
        keaktifan = s["keaktifan"].replace("%", "")

        siswa_user = UsersModel(
            username=username,
            nama_lengkap=nama_lengkap,
            email=email,
            password=get_password_hash("password123"),
            avatar_url=f"https://i.pravatar.cc/150?u={username}",
            role=UserRole.SISWA,
        )

        await siswa_user.insert()

        # Create Profile
        profile = SiswaProfileModel(
            id_siswa=s["id_siswa"],
            user=siswa_user,
            gaya_belajar=s["gaya_belajar"],
            kognitif=s["kognitif"],
            keaktifan=keaktifan,
            id_jurusan=Jurusan.IPS,
        )
        await profile.insert()

        target_kelas.peserta.append(siswa_user)

        print(f"Siswa {nama_lengkap} ({username}) and profile created successfully!")

    await target_kelas.save()
    print(f"Success create {len(siswa_list)} siswa with profiles from JSON!")


if __name__ == "__main__":
    asyncio.run(create_siswa())
