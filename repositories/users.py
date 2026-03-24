from models import UsersModel, SiswaProfileModel, KelasModel
from schemas import UserRole
from .database import Database


class UsersRepository(Database):
    async def insert(self, **kwargs):
        new_user = UsersModel(**kwargs)
        await new_user.insert()
        return new_user

    async def get(self, category, **kwargs):
        email = kwargs.get("email")
        kode_kelas = kwargs.get("kode_kelas")
        id = kwargs.get("id")
        if category == "get_user_by_email":
            return await UsersModel.find_one({"email": email})
        elif category == "get_user_by_id":
            return await UsersModel.get(id)
        elif category == "get_siswa_by_kelas":
            kelas = await KelasModel.find_one(KelasModel.kode_unik == kode_kelas)

            if not kelas:
                return []

            user_ids = [p.ref.id for p in kelas.peserta]

            users = await UsersModel.find({"_id": {"$in": user_ids}}).to_list()
            profiles = await SiswaProfileModel.find(
                {"user.$id": {"$in": user_ids}}
            ).to_list()

            profile_dict = {str(p.user.ref.id): p for p in profiles}

            result = []
            for user in users:
                user_id_str = str(user.id)

                user_data = user.model_dump()
                user_data["id"] = user_id_str

                profile_data = {}
                if user_id_str in profile_dict:
                    p = profile_dict[user_id_str]
                    profile_data = p.model_dump()
                    profile_data["id"] = str(p.id)

                result.append({**profile_data, "user": user_data})

            return result
        elif category == "get_all_siswa":

            profiles = await SiswaProfileModel.find_all().to_list()
            users = await UsersModel.find({"role": UserRole.SISWA}).to_list()

            user_dict = {str(u.id): u for u in users}

            result = []
            for p in profiles:
                user_id_str = str(p.user.ref.id)
                if user_id_str in user_dict:
                    profile_data = p.model_dump()
                    profile_data["id"] = str(p.id)

                    user_data = user_dict[user_id_str].model_dump()
                    user_data["id"] = str(user_dict[user_id_str].id)

                    profile_data["user"] = user_data
                    result.append(profile_data)

            return result

    async def update(self, category, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass
