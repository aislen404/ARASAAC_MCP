from datetime import UTC, datetime

from fastapi.testclient import TestClient

from arasaac_platform.api.materials import get_repository
from arasaac_platform.main import app
from arasaac_platform.repositories.memory import InMemoryRepository


def payload() -> dict[str, object]:
    return {
        "title": "Agenda de demostración",
        "steps": [
            {
                "text": "Llegar",
                "pictogram": {
                    "pictogram_id": 6964,
                    "label": "casa",
                    "source_url": (
                        "https://static.arasaac.org/pictograms/6964/6964_300.png"
                    ),
                    "retrieved_at": datetime.now(UTC).isoformat(),
                },
            }
        ],
    }


def create_workspace(client: TestClient, display_name: str | None = None) -> str:
    body = {} if display_name is None else {"display_name": display_name}
    response = client.post("/api/workspaces", json=body)
    assert response.status_code == 201
    return response.json()["workspace"]["slug"]


def test_full_agenda_review_and_html_export_flow() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    client = TestClient(app)
    app.state = getattr(app, "state", object())
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

    slug = create_workspace(client)

    created = client.post(f"/api/workspaces/{slug}/materials/agendas", json=payload())
    assert created.status_code == 201
    material_id = created.json()["material"]["material_id"]

    blocked = client.get(f"/api/workspaces/{slug}/materials/{material_id}/export?format=html")
    assert blocked.status_code == 409

    submitted = client.post(f"/api/workspaces/{slug}/materials/{material_id}/submit")
    assert submitted.json()["material"]["status"] == "in_review"

    reviewed = client.post(
        f"/api/workspaces/{slug}/materials/{material_id}/review",
        json={
            "outcome": "approved",
            "human_confirmed": True,
            "note": "Revisado para la demostración.",
        },
    )
    assert reviewed.json()["material"]["status"] == "approved"

    exported = client.get(f"/api/workspaces/{slug}/materials/{material_id}/export?format=html")
    assert exported.status_code == 200
    assert exported.json()["media_type"] == "text/html"
    assert exported.json()["manifest"]["license"] == "CC BY-NC-SA"
    assert exported.json()["manifest"]["human_review_approved"] is True
    assert exported.json()["manifest"]["pictograms"][0]["pictogram_id"] == 6964

    audit = client.get(f"/api/workspaces/{slug}/materials/{material_id}/audit").json()["events"]
    assert [event["action"] for event in audit] == [
        "created",
        "submitted",
        "reviewed",
        "exported",
    ]


def test_manifest_endpoint_requires_approved_material() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    client = TestClient(app)
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

    slug = create_workspace(client)
    material_id = client.post(f"/api/workspaces/{slug}/materials/agendas", json=payload()).json()["material"]["material_id"]

    blocked = client.get(f"/api/workspaces/{slug}/materials/{material_id}/export/manifest")
    assert blocked.status_code == 409

    client.post(f"/api/workspaces/{slug}/materials/{material_id}/submit")
    client.post(
        f"/api/workspaces/{slug}/materials/{material_id}/review",
        json={"outcome": "approved", "human_confirmed": True, "note": "OK"},
    )

    manifest = client.get(f"/api/workspaces/{slug}/materials/{material_id}/export/manifest")
    assert manifest.status_code == 200
    assert manifest.json()["material_id"] == material_id


def test_material_list_rejects_invalid_pagination() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    client = TestClient(app)
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

    slug = create_workspace(client)

    assert client.get(f"/api/workspaces/{slug}/materials?limit=0").status_code == 422
    assert client.get(f"/api/workspaces/{slug}/materials?limit=101").status_code == 422
    assert client.get(f"/api/workspaces/{slug}/materials?offset=-1").status_code == 422


def test_review_rejects_invalid_transition() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    client = TestClient(app)
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    slug = create_workspace(client)
    material_id = client.post(f"/api/workspaces/{slug}/materials/agendas", json=payload()).json()[
        "material"
    ]["material_id"]

    response = client.post(
        f"/api/workspaces/{slug}/materials/{material_id}/review",
        json={
            "outcome": "approved",
            "human_confirmed": True,
            "note": "No enviado a revisión.",
        },
    )

    assert response.status_code == 409


def test_workspace_cross_access_returns_404() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    client = TestClient(app)

    slug_a = create_workspace(client)
    slug_b = create_workspace(client)
    material_id = client.post(f"/api/workspaces/{slug_a}/materials/agendas", json=payload()).json()["material"]["material_id"]

    response = client.get(f"/api/workspaces/{slug_b}/materials/{material_id}")

    assert response.status_code == 404


def test_workspace_patch_updates_display_name() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    client = TestClient(app)

    slug = create_workspace(client)
    response = client.patch(
        f"/api/workspaces/{slug}",
        json={"display_name": "Centro comunitario"},
    )

    assert response.status_code == 200
    assert response.json()["workspace"]["display_name"] == "Centro comunitario"


def test_workspace_create_rejects_possible_personal_data() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    client = TestClient(app)

    response = client.post("/api/workspaces", json={"display_name": "Juan Pérez"})

    assert response.status_code == 422


def test_workspace_patch_rejects_possible_personal_data() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    __import__("os").environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    client = TestClient(app)

    slug = create_workspace(client)
    response = client.patch(
        f"/api/workspaces/{slug}",
        json={"display_name": "Ana Gómez"},
    )

    assert response.status_code == 422
