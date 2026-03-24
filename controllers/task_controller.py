from repositories.task_repo import TaskRepository
from fastapi import HTTPException, status
from beanie import PydanticObjectId


class TaskController:
    def __init__(self):
        self.repo = TaskRepository()

    async def create_new_task(self, task_data: dict):
        task = await self.repo.insert(**task_data)
        return {
            "status": "success",
            "code": 201,
            "message": "Task berhasil dibuat secara modular",
            "data": task,
        }

    async def get_all_titles(self):
        tasks = await self.repo.get()
        return {
            "status": "success",
            "code": 200,
            "message": f"Ditemukan {len(tasks)} tugas",
            "data": tasks,
        }

    async def get_task_by_id(self, task_id: str):
        # Validasi format ID secara manual agar seragam 404
        if not PydanticObjectId.is_valid(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tugas tidak ada dalam sistem",
            )

        task = await self.repo.get(id=task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tugas tidak ada dalam sistem",
            )
        return {"status": "success", "code": 200, "data": task}
