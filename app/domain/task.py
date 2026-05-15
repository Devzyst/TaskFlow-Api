from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

class TaskStatus(StrEnum):
    """Allowed lifecycle states for a task."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass(slots=True)
class Task:
    """Task aggregate used internally by services and repositories."""

    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def rename(self, title: str) -> None:
        self.title = title
        self.touch()

    def update_details(self, description: str | None, status: TaskStatus) -> None:
        self.description = description
        self.status = status
        self.touch()

    def touch(self) -> None:
        self.updated_at = datetime.now(UTC)
