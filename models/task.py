from .timestamp import TimestampDocument
from schemas import TaskCreate


class TaskModel(TimestampDocument, TaskCreate):
    class Settings:
        name = "tasks"
        indexes = ["deleted_at"]
