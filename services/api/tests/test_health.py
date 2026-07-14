from fastapi.testclient import TestClient

from arasaac_platform.api.materials import get_repository
from arasaac_platform.main import app
from arasaac_platform.repositories.memory import InMemoryRepository


def test_healthcheck() -> None:
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    app.dependency_overrides[get_repository] = lambda: InMemoryRepository()
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "api"}
    app.dependency_overrides.clear()


def test_healthcheck_returns_503_without_database() -> None:
    os_environ = __import__("os").environ
    previous = os_environ.pop("DATABASE_URL", None)

    response = TestClient(app).get("/health")

    assert response.status_code == 503
    if previous is not None:
        os_environ["DATABASE_URL"] = previous
