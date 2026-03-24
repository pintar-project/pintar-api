from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import FileResponse
from controllers import UsersConroller
from models import UsersCreated
from schemas.base_schema import APIResponse

router = APIRouter(prefix="/users", tags=["Users"])
users_controller = UsersConroller()


@router.post(
    "/siswa",
    response_model=APIResponse[UsersCreated],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_in: UsersCreated, request: Request):
    return await users_controller.create_user(user_in.model_dump(), request, "siswa")


@router.get("/avatar")
async def get_avatar():
    return FileResponse("assets/avatar.webp")
