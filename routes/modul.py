from fastapi import APIRouter, status, Depends, Form, UploadFile, File
from models import UserResponse, ModulResponse
from schemas.base_schema import APIResponse
from controllers import AuthController, ModulController
from core import get_current_user
from typing import Annotated

router = APIRouter(prefix="/modul", tags=["Modul"])
auth_controller = AuthController()
modul_controller = ModulController()


@router.post(
    "/file",
    response_model=APIResponse[ModulResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_modul_by_file(
    judul: Annotated[str, Form()],
    file_modul: Annotated[UploadFile, File()],
    current_user: UserResponse = Depends(get_current_user),
):
    modul_data = {"judul": judul, "file_modul": file_modul}
    return await modul_controller.create_modul(modul_data, current_user)
