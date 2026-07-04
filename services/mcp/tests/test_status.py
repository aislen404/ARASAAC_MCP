from fastapi.testclient import TestClient

from safe_mcp.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "mcp-server"}


def test_status_exposes_only_allowlisted_tools() -> None:
    response = client.get("/mcp/status")

    assert response.status_code == 200
    assert response.json() == {
        "status": "active",
        "enabled": True,
        "tools": [
            "get_pictogram",
            "search_pictograms",
            "suggest_pictograms_for_text",
        ],
    }
