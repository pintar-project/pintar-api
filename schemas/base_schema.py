from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(exclude_none=True)
    message: Optional[str] = None
    data: Optional[T] = None
    token: Optional[dict] = None
    statistik_pemetaan: Optional[dict] = None
    header_kelas: Optional[dict] = None
