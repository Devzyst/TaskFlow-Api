from app.domain.repositories import TaskRepository
from app.services.task_service import TaskService

_task_repository = TaskRepository()
_task_service = TaskService(_task_repository)


def get_task_service() -> TaskService:
    return _task_service
