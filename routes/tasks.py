from fastapi import APIRouter, status
from controllers.task_controller import TaskController
from models.task import TaskCreate, TaskTitleOnly
from schemas.base_schema import APIResponse
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])
task_ctrl = TaskController()


@router.post(
    "/", response_model=APIResponse[TaskTitleOnly], status_code=status.HTTP_201_CREATED
)
async def create_task(task_in: TaskCreate):
    return await task_ctrl.create_new_task(task_in.model_dump())


@router.get(
    "/titles",
    response_model=APIResponse[List[TaskTitleOnly]],
    status_code=status.HTTP_200_OK,
)
async def list_task_titles():
    return await task_ctrl.get_all_titles()


@router.get(
    "/{id}", response_model=APIResponse[TaskTitleOnly], status_code=status.HTTP_200_OK
)
async def get_task(id: str):
    return await task_ctrl.get_task_by_id(id)
