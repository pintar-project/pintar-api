from fastapi import APIRouter, status
from controllers import TaskController
from schemas import TaskResponse, TaskCreate, TaskUpdate, TaskTitleOnly, APIResponse
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])
task_controller = TaskController()


@router.get(
    "/",
    response_model=APIResponse[List[TaskResponse]],
    status_code=status.HTTP_200_OK,
)
async def index():
    return await task_controller.get_all_tasks()


@router.post(
    "/", response_model=APIResponse[TaskResponse], status_code=status.HTTP_201_CREATED
)
async def create(task: TaskCreate):
    return await task_controller.create_task(task.model_dump())


@router.get(
    "/{task_id}",
    response_model=APIResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
)
async def show(task_id: str):
    return await task_controller.get_task(task_id)


@router.patch(
    "/{task_id}",
    response_model=APIResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
)
async def patch(task_id: str, task: TaskUpdate):
    return await task_controller.update_task_partial(
        task_id, task.model_dump(exclude_unset=True)
    )


@router.put(
    "/{task_id}",
    response_model=APIResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
)
async def update(task_id: str, task: TaskCreate):
    return await task_controller.update_task_full(task_id, task.model_dump())


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: str):
    return await task_controller.delete_task(task_id)


@router.patch(
    "/{task_id}/title",
    response_model=APIResponse[TaskResponse],
    status_code=status.HTTP_200_OK,
)
async def update_title(task_id: str, task: TaskTitleOnly):
    return await task_controller.update_task_title_only(task_id, task.title)
