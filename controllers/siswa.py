from repositories import UsersRepository
from fastapi import HTTPException, status


class SiswaController:
    def __init__(self):
        self.repo = UsersRepository()

    async def get_siswa_by_kelas(self, kode_kelas: str):
        data_siswa = await self.repo.get("get_siswa_by_kelas", kode_kelas=kode_kelas)

        if not data_siswa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="siswa tidak ditemukan",
            )

        total_siswa = len(data_siswa)

        statistik = {
            "kognitif": {
                "jumlah": {"tinggi": 0, "sedang": 0, "rendah": 0},
                "persentase": {"tinggi": 0, "sedang": 0, "rendah": 0},
            },
            "gaya_belajar": {
                "jumlah": {"auditori": 0, "visual": 0, "kinestetik": 0},
                "persentase": {"auditori": 0, "visual": 0, "kinestetik": 0},
            },
            "jumlah_siswa": total_siswa,
        }

        for siswa in data_siswa:
            kognitif_key = siswa.get("kognitif", "").lower()
            if kognitif_key in statistik["kognitif"]["jumlah"]:
                statistik["kognitif"]["jumlah"][kognitif_key] += 1

            gaya_key = siswa.get("gaya_belajar", "").lower()
            if gaya_key in statistik["gaya_belajar"]["jumlah"]:
                statistik["gaya_belajar"]["jumlah"][gaya_key] += 1

        if total_siswa > 0:
            for key in statistik["gaya_belajar"]["jumlah"]:
                jumlah = statistik["gaya_belajar"]["jumlah"][key]
                statistik["gaya_belajar"]["persentase"][key] = round(
                    (jumlah / total_siswa) * 100
                )

            for key in statistik["kognitif"]["jumlah"]:
                jumlah = statistik["kognitif"]["jumlah"][key]
                statistik["kognitif"]["persentase"][key] = round(
                    (jumlah / total_siswa) * 100
                )

        return {
            "message": "success",
            "statistik_pemetaan": statistik,
            "data": data_siswa,
        }

    async def get_all_siswa(self):
        data_siswa = await self.repo.get("get_all_siswa")

        if not data_siswa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="siswa tidak ditemukan",
            )

        total_siswa = len(data_siswa)

        # Inisialisasi counter untuk statistik (Jumlah & Persentase)
        statistik = {
            "kognitif": {
                "jumlah": {"tinggi": 0, "sedang": 0, "rendah": 0},
                "persentase": {"tinggi": 0, "sedang": 0, "rendah": 0},
            },
            "gaya_belajar": {
                "jumlah": {"auditori": 0, "visual": 0, "kinestetik": 0},
                "persentase": {"auditori": 0, "visual": 0, "kinestetik": 0},
            },
            "jumlah_siswa": total_siswa,
        }

        for siswa in data_siswa:
            kognitif_key = siswa.get("kognitif", "").lower()
            if kognitif_key in statistik["kognitif"]["jumlah"]:
                statistik["kognitif"]["jumlah"][kognitif_key] += 1

            gaya_key = siswa.get("gaya_belajar", "").lower()
            if gaya_key in statistik["gaya_belajar"]["jumlah"]:
                statistik["gaya_belajar"]["jumlah"][gaya_key] += 1

        if total_siswa > 0:
            for key in statistik["gaya_belajar"]["jumlah"]:
                jumlah = statistik["gaya_belajar"]["jumlah"][key]
                statistik["gaya_belajar"]["persentase"][
                    key
                ] = f"{round((jumlah / total_siswa) * 100)}%"

            for key in statistik["kognitif"]["jumlah"]:
                jumlah = statistik["kognitif"]["jumlah"][key]
                statistik["kognitif"]["persentase"][
                    key
                ] = f"{round((jumlah / total_siswa) * 100)}%"

        return {
            "message": "success",
            "statistik_pemetaan": statistik,
            "data": data_siswa,
        }
