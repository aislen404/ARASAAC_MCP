import pytest
from fastapi.testclient import TestClient

from arasaac_platform.api.materials import get_repository
from arasaac_platform.main import app
from arasaac_platform.repositories.memory import InMemoryRepository


@pytest.fixture
def repository() -> InMemoryRepository:
    return InMemoryRepository()


@pytest.fixture
def client(repository: InMemoryRepository) -> TestClient:
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
