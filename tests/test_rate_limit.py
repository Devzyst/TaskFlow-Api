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
def test_task_service_create_update_delete_flow(task_service):
    task = task_service.create_task(TaskPayload(title="  Build API  "))

    assert task.title == "Build API"
    assert task.status == TaskStatus.TODO
    assert task_service.list_tasks() == [task]

    updated = task_service.update_task(
        task.id,
        TaskPayload(title="Ship API", description="Portfolio ready", status=TaskStatus.DONE),
    )

    assert updated.title == "Ship API"
    assert updated.description == "Portfolio ready"
    assert updated.status == TaskStatus.DONE

    task_service.delete_task(task.id)
    assert task_service.list_tasks() == []
