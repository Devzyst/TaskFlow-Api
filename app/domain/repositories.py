from uuid import UUID

from app.domain.task import Task

class TaskRepository:
    """In-memory task repository suitable for tests and local demos."""

    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}

    def list(self) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda task: task.created_at)

    def get(self, task_id: UUID) -> Task | None:
        return self._tasks.get(task_id)

    def save(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: UUID) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def clear(self) -> None:
        self._tasks.clear()
