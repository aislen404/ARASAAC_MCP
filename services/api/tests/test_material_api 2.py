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


def test_full_agenda_review_and_html_export_flow() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    client = TestClient(app)

    created = client.post("/api/materials/agendas", json=payload())
    assert created.status_code == 201
    material_id = created.json()["material"]["material_id"]

    blocked = client.get(f"/api/materials/{material_id}/export?format=html")
    assert blocked.status_code == 409

    submitted = client.post(f"/api/materials/{material_id}/submit")
    assert submitted.json()["material"]["status"] == "in_review"

    reviewed = client.post(
        f"/api/materials/{material_id}/review",
        json={
            "outcome": "approved",
            "human_confirmed": True,
            "note": "Revisado para la demostración.",
        },
    )
    assert reviewed.json()["material"]["status"] == "approved"

    exported = client.get(f"/api/materials/{material_id}/export?format=html")
    assert exported.status_code == 200
    assert exported.json()["media_type"] == "text/html"
    assert exported.json()["manifest"]["license"] == "CC BY-NC-SA"
    assert exported.json()["manifest"]["human_review_approved"] is True
    assert exported.json()["manifest"]["pictograms"][0]["pictogram_id"] == 6964

    audit = client.get(f"/api/materials/{material_id}/audit").json()["events"]
    assert [event["action"] for event in audit] == [
        "created",
        "submitted",
        "reviewed",
        "exported",
    ]


def test_review_rejects_invalid_transition() -> None:
    repository = InMemoryRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    client = TestClient(app)
    material_id = client.post("/api/materials/agendas", json=payload()).json()[
        "material"
    ]["material_id"]

    response = client.post(
        f"/api/materials/{material_id}/review",
        json={
            "outcome": "approved",
            "human_confirmed": True,
            "note": "No enviado a revisión.",
        },
    )

    assert response.status_code == 409
