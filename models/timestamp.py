from datetime import datetime, timezone
from typing import Optional
from beanie import before_event, Insert, Replace, Save, SaveChanges, Document
from pydantic import Field


def current_timestamp() -> float:
    return datetime.now(timezone.utc).timestamp()


class TimestampDocument(Document):
    created_at: float = Field(default_factory=current_timestamp)
    updated_at: float = Field(default_factory=current_timestamp)
    deleted_at: Optional[float] = None

    @before_event(Insert)
    def sync_timestamps(self):
        self.created_at = self.updated_at = current_timestamp()

    @before_event(Replace, Save, SaveChanges)
    def update_updated_at(self):
        self.updated_at = current_timestamp()
