from fastapi import APIRouter, status, Depends
from typing import List
from schemas import SiswaProfileResponse, UserResponse, APIResponse
from controllers import SiswaController
from core import get_current_user

router = APIRouter(prefix="/siswa", tags=["Siswa"])
siswa_controller = SiswaController()


@router.get(
    "/",
    response_model=APIResponse[List[SiswaProfileResponse]],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_all_siswa(current_user: UserResponse = Depends(get_current_user)):
    return await siswa_controller.get_all_siswa()


@router.get(
    "/kelas/{kode_kelas}",
    response_model=APIResponse[List[SiswaProfileResponse]],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_siswa_by_kelas(
    kode_kelas: str, current_user: UserResponse = Depends(get_current_user)
):
    return await siswa_controller.get_siswa_by_kelas(kode_kelas)
