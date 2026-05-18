from dataclasses import dataclass
from uuid import uuid4

import pytest

from app.core.errors import ApiError
from app.domain.task import TaskStatus


@dataclass(frozen=True)
class TaskPayload:
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
