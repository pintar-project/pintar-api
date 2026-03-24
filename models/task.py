from beanie import Document
from .timestamp import TimestampDocument
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str


class TaskTitleOnly(BaseModel):
    title: str = Field(serialization_alias="nama_tugas")

    class Config:
        populate_by_name = True


class TaskModel(TimestampDocument, TaskCreate):
    is_completed: bool = False

    class Settings:
        name = "tasks"
        indexes = ["deleted_at"]
