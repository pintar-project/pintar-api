from fastapi import APIRouter, status, Depends
from models import (
    UserResponse,
    UsersCreated,
    TahunAjaranResponse,
    TahunAjaranCreated,
    TahunAjaranUpdated,
)
from schemas.base_schema import APIResponse
from controllers import AuthController, TahunAjaranController
from core import get_current_user

router = APIRouter(prefix="/tahun-ajaran", tags=["Tahun Ajaran"])
auth_controller = AuthController()
tahun_ajaran_controller = TahunAjaranController()


@router.post(
    "/",
    response_model=APIResponse[TahunAjaranResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_tahun_ajaran(
    user_in: TahunAjaranCreated, current_user: UserResponse = Depends(get_current_user)
):
    return await tahun_ajaran_controller.create_tahun_ajaran(user_in.model_dump())


@router.patch(
    "/{id}/is-active",
    response_model=APIResponse[TahunAjaranResponse],
    status_code=status.HTTP_201_CREATED,
)
async def tahun_ajaran_is_active(
    id: str,
    user_in: TahunAjaranUpdated,
    current_user: UserResponse = Depends(get_current_user),
):
    return await tahun_ajaran_controller.tahun_ajaran_is_active(
        id, user_in.model_dump()
    )


@router.post(
    "/guru",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_guru(
    user_in: UsersCreated, current_user: UserResponse = Depends(get_current_user)
):
    return await auth_controller.create_guru(user_in.model_dump(), current_user)


@router.post(
    "/siswa",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_siswa(
    user_in: UsersCreated, current_user: UserResponse = Depends(get_current_user)
):
    return await auth_controller.create_siswa(user_in.model_dump(), current_user)
