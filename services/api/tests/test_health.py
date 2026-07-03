from fastapi.testclient import TestClient

from arasaac_platform.main import app


def test_healthcheck() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "api"}
