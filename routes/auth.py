from fastapi import APIRouter, status, Depends
from schemas import UserLogin, UserResponse, APIResponse
from controllers.auth import AuthController
from core import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"], redirect_slashes=False)
auth_controller = AuthController()


@router.post(
    "/login",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def user_login(login_in: UserLogin):
    return await auth_controller.user_login(login_in.model_dump())


@router.get(
    "/@me",
    response_model=APIResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def user_me(current_user: UserResponse = Depends(get_current_user)):
    return await auth_controller.user_me(current_user)
