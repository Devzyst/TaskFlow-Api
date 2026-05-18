from collections.abc import Generator

import pytest

from app.domain.repositories import TaskRepository
from app.services.task_service import TaskService


@pytest.fixture
def task_service() -> TaskService:
    return TaskService(TaskRepository())
