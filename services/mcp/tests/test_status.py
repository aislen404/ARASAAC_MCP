from fastapi.testclient import TestClient

from safe_mcp.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "mcp-placeholder"}


def test_placeholder_has_no_tools() -> None:
    response = client.get("/mcp/status")

    assert response.status_code == 200
    assert response.json() == {
        "status": "placeholder",
        "enabled": False,
        "tools": [],
    }
