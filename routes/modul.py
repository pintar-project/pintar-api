from fastapi import APIRouter, status, Depends, Form, UploadFile, File
from schemas import ModulResponse, UserResponse, APIResponse, Jurusan
from controllers import AuthController, ModulController
from core import get_current_user
from typing import Annotated, Optional

router = APIRouter(prefix="/modul", tags=["Modul"], redirect_slashes=False)
auth_controller = AuthController()
modul_controller = ModulController()


@router.post(
    "/file",
    response_model=APIResponse[ModulResponse],
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def create_modul_by_file(
    judul: Annotated[str, Form()],
    tingkat: Annotated[str, Form()],
    id_mapel: Annotated[str, Form()],
    file_modul: Annotated[UploadFile, File()],
    id_jurusan: Annotated[Jurusan, Form()],
    kode_kelas: Annotated[Optional[str], Form()] = None,
    current_user: UserResponse = Depends(get_current_user),
):
    modul_data = {
        "judul": judul,
        "tingkat": tingkat,
        "id_mapel": id_mapel,
        "file_modul": file_modul,
        "id_jurusan": id_jurusan,
        "kode_kelas": kode_kelas,
    }
    return await modul_controller.create_modul(modul_data, current_user)


@router.get(
    "/",
    response_model=APIResponse[list[ModulResponse]],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_all_modul(
    current_user: UserResponse = Depends(get_current_user),
):
    return await modul_controller.get_all_modul()


@router.get(
    "/{tingkat}/{nama_mapel}",
    response_model=APIResponse[list[ModulResponse]],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_modul_by_filter(
    tingkat: str,
    nama_mapel: str,
    current_user: UserResponse = Depends(get_current_user),
):
    return await modul_controller.get_modul_by_filter(tingkat, nama_mapel)
