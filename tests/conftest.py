from collections.abc import Generator

import pytest

from app.domain.repositories import TaskRepository
from app.services.task_service import TaskService


@pytest.fixture
def task_service() -> TaskService:
    return TaskService(TaskRepository())

@pytest.fixture
def client() -> Generator[object, None, None]:
    fastapi_testclient = pytest.importorskip("fastapi.testclient")

    from app.dependencies import get_task_service
    from app.main import create_app

    service = TaskService(TaskRepository())
    app = create_app()
    app.dependency_overrides[get_task_service] = lambda: service

    with fastapi_testclient.TestClient(app) as test_client:
        yield test_client
