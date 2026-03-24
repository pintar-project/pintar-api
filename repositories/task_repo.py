from typing import Optional, List
from models import TaskModel as Task
from datetime import datetime, timezone
from .database import Database


class TaskRepository(Database):
    async def insert(self, **kwargs) -> Task:
        new_task = Task(**kwargs)
        await new_task.insert()
        return new_task

    async def get(self, id: Optional[str] = None) -> List[Task] | Optional[Task]:
        if id:
            return await Task.get(id)
        return await Task.find(Task.deleted_at == None).to_list()

    async def update(self, id: str, **kwargs) -> Optional[Task]:
        task = await Task.get(id)
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            await task.save()
            return task
        return None

    async def delete_permanent(self, id: str) -> bool:
        task = await Task.get(id)
        if task:
            await task.delete()
            return True
        return False
