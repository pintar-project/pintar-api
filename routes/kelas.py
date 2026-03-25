from fastapi import APIRouter, status, Depends
from schemas import KelasCreated, KelasResponse, UserResponse, APIResponse
from typing import List
from controllers import AuthController, KelasController
from core import get_current_user

router = APIRouter(prefix="/kelas", tags=["Kelas"], redirect_slashes=False)
auth_controller = AuthController()
kelas_controller = KelasController()


@router.post(
    "/",
    response_model=APIResponse[KelasResponse],
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def create_kelas(
    user_in: KelasCreated, current_user: UserResponse = Depends(get_current_user)
):
    return await kelas_controller.create_kelas(user_in.model_dump(), current_user)


@router.get(
    "",
    response_model=APIResponse[List[KelasResponse]],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_all_kelas(current_user: UserResponse = Depends(get_current_user)):
    return await kelas_controller.get_all_kelas()


@router.get(
    "/{kode_kelas}",
    response_model=APIResponse[KelasResponse],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_kelas_by_kode(
    kode_kelas: str, current_user: UserResponse = Depends(get_current_user)
):
    return await kelas_controller.get_kelas_by_kode(kode_kelas)
