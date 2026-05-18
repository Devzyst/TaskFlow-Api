from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.task import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, examples=["Plan sprint"])
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus = TaskStatus.TODO


class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus = TaskStatus.TODO


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

class HealthRead(BaseModel):
    status: str
    service: str
    version: str
    environment: str
