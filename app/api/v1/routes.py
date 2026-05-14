from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.core.config import settings
from app.dependencies import get_task_service
from app.schemas import HealthRead, TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()
TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]


@router.get("/health", response_model=HealthRead, tags=["System"])
def health_check() -> HealthRead:
    """Expose a lightweight readiness probe for uptime monitors."""

    return HealthRead(
        status="ok",
        service=settings.app_name,
        version="v1",
        environment=settings.environment,
    )


@router.get("/tasks", response_model=list[TaskRead], tags=["Tasks"])
def list_tasks(service: TaskServiceDependency) -> list[TaskRead]:
    """Return all tasks ordered by creation time."""

    return [TaskRead.model_validate(task) for task in service.list_tasks()]


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(payload: TaskCreate, service: TaskServiceDependency) -> TaskRead:
    """Create a task."""

    return TaskRead.model_validate(service.create_task(payload))


@router.get("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
def get_task(task_id: UUID, service: TaskServiceDependency) -> TaskRead:
    """Return one task by ID."""

    return TaskRead.model_validate(service.get_task(task_id))


@router.put("/tasks/{task_id}", response_model=TaskRead, tags=["Tasks"])
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    service: TaskServiceDependency,
) -> TaskRead:
    """Replace an existing task."""

    return TaskRead.model_validate(service.update_task(task_id, payload))


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: UUID, service: TaskServiceDependency) -> Response:
    """Delete a task by ID."""

    service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
