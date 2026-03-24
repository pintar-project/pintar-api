from typing import Optional, List, Any
from models import TaskModel as Task
from datetime import datetime, timezone
from .database import Database


class TaskRepository(Database):
    async def insert(self, **kwargs) -> Task:
        # kwargs berisi data dari model_dump()
        new_task = Task(**kwargs)
        await new_task.insert()
        return new_task

    async def get(self, **kwargs) -> List[Task]:
        # Jika ada 'id' di kwargs, ambil satu, jika tidak ambil semua yang belum dihapus
        task_id = kwargs.get("id")
        if task_id:
            return await Task.get(task_id)
        return await Task.find(Task.deleted_at == None).to_list()

    async def update(self, **kwargs) -> Optional[Task]:
        task_id = kwargs.pop("id", None)
        if not task_id:
            return None

        task = await Task.get(task_id)
        if task:
            # Update field yang dikirim di kwargs
            await task.set(kwargs)
            return task
        return None

    async def delete(self, **kwargs) -> bool:
        task_id = kwargs.get("id")
        task = await Task.get(task_id)
        if task:
            # Kita gunakan Soft Delete sesuai TimestampDocument sebelumnya
            task.deleted_at = datetime.now(timezone.utc)
            await task.save()
            return True
        return False
