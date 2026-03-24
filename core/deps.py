from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core import JwtToken
from models import UsersModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token tidak valid atau sudah kadaluarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = JwtToken.verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await UsersModel.get(user_id)
    if user is None:
        raise credentials_exception

    return user
