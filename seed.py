import asyncio
import os
from create_tahun_ajaran import buat_tahun_ajaran
from create_admin import create_admin
from create_guru import create_guru
from create_mapel_sosiologi import create_mapel
from create_kelas_ips import create_kelas_ips
from create_modul import create_modul
from create_siswa import create_siswa

async def run_seed():
    print("🚀 Starting Final Database Seeding for Docker...")
    
    # Phase 1: Foundations
    print("\n--- Phase 1: Foundations (Tahun Ajaran, Admin, Guru) ---")
    await buat_tahun_ajaran("2026/2027", semester=1, set_aktif=True)
    await create_admin()
    await create_guru()
    
    # Phase 2: Metadata
    print("\n--- Phase 2: Metadata (Mata Pelajaran) ---")
    await create_mapel()
    
    # Phase 3: Structure
    print("\n--- Phase 3: Structure (Kelas) ---")
    await create_kelas_ips()
    
    # Phase 4: Content & Participants
    print("\n--- Phase 4: Content & Participants (Modul & Siswa) ---")
    await create_modul()
    await create_siswa()
    
    print("\n✅ Seeding Completed Successfully! All relations established.")

if __name__ == "__main__":
    asyncio.run(run_seed())
