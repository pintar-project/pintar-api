from models import TaskModel
from models.timestamp import current_timestamp
from fastapi import HTTPException, status
from beanie import PydanticObjectId
from repositories.task_repo import TaskRepository


class TaskController:
    def __init__(self):
        self.repo = TaskRepository()

    async def get_all_tasks(self):
        tasks = await self.repo.get()
        return {
            "message": "success",
            "data": tasks,
        }

    async def create_task(self, task_data: dict):
        task = await self.repo.insert(**task_data)
        return {
            "message": "success",
            "data": task,
        }

    async def get_task(self, task_id: str):
        if not PydanticObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tugas tidak ditemukan",
            )
        task = await self.repo.get(id=task_id)
        if not task or task.deleted_at:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tugas tidak ditemukan",
            )
        return {"message": "success", "data": task}

    async def update_task_partial(self, task_id: str, task_data: dict):
        if not PydanticObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tugas tidak ditemukan",
            )
        task = await self.repo.update(task_id, **task_data)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tugas tidak ditemukan",
            )
        return {"message": "success", "data": task}

    async def update_task_full(self, task_id: str, task_data: dict):
        return await self.update_task_partial(task_id, task_data)

    async def update_task_title_only(self, task_id: str, title: str):
        return await self.update_task_partial(task_id, {"title": title})

    async def delete_task(self, task_id: str):
        if not PydanticObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tugas tidak ditemukan",
            )
        # Soft delete is just an update to deleted_at
        task = await self.repo.update(task_id, deleted_at=current_timestamp())
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tugas tidak ditemukan",
            )
        return None  # No content response
