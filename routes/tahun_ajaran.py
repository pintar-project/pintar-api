from fastapi import APIRouter, status, Depends
from models import UserResponse, TahunAjaranResponse
from schemas.base_schema import APIResponse
from controllers import TahunAjaranController
from core import get_current_user

router = APIRouter(prefix="/tahun-ajaran", tags=["Tahun Ajaran"])
tahun_ajaran_controller = TahunAjaranController()


@router.get(
    "/",
    response_model=APIResponse[TahunAjaranResponse],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_tahun_ajaran(current_user: UserResponse = Depends(get_current_user)):
    return await tahun_ajaran_controller.get_tahun_ajaran()
