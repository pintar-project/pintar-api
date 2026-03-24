from models import KelasModel
from models import UsersModel, UserRole, SiswaProfileModel
from .database import Database
from core.security import get_password_hash


class UsersRepository(Database):
    async def insert(self, **kwargs):
        username = kwargs.get("username")
        nama_lengkap = kwargs.get("nama_lengkap")
        email = kwargs.get("email")
        password = kwargs.get("password")
        avatar_url = kwargs.get("avatar_url")
        role = kwargs.get("role")

        if password:
            hashed_password = get_password_hash(password)
        else:
            hashed_password = None

        new_user = UsersModel(
            username=username,
            nama_lengkap=nama_lengkap,
            email=email,
            password=hashed_password,
            avatar_url=avatar_url,
            role=role,
        )
        await new_user.insert()
        return new_user

    async def get(self, category, **kwargs):
        email = kwargs.get("email")
        kode_kelas = kwargs.get("kode_kelas")
        if category == "get_user_by_email":
            return await UsersModel.find_one({"email": email})
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
        username = kwargs.get("username")
        nama_lengkap = kwargs.get("nama_lengkap")
        email = kwargs.get("email")
        password = kwargs.get("password")
        avatar_url = kwargs.get("avatar_url")
        if category == "create_guru":
            data_guru = UsersModel(
                username=username,
                nama_lengkap=nama_lengkap,
                email=email,
                password=password,
                avatar_url=avatar_url,
                role=UserRole.GURU,
            )
            await data_guru.insert()
            return data_guru
        elif category == "create_siswa":
            data_siswa = UsersModel(
                username=username,
                nama_lengkap=nama_lengkap,
                email=email,
                password=password,
                avatar_url=avatar_url,
                role=UserRole.SISWA,
            )
            await data_siswa.insert()
            return data_siswa

    async def delete(self, **kwargs):
        pass
