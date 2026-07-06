from datetime import UTC, datetime


def pictogram_payload(pictogram_id: int = 6964, label: str = "casa") -> dict[str, object]:
    return {
        "pictogram_id": pictogram_id,
        "label": label,
        "source_url": f"https://static.arasaac.org/pictograms/{pictogram_id}/{pictogram_id}_300.png",
        "retrieved_at": datetime.now(UTC).isoformat(),
    }


def agenda_payload() -> dict[str, object]:
    return {
        "title": "Agenda de demostración",
        "steps": [{"text": "Llegar", "pictogram": pictogram_payload()}],
    }


def board_payload() -> dict[str, object]:
    return {
        "title": "Tablero de demostración",
        "cells": [
            {"text": "Hola", "pictogram": pictogram_payload(6964, "hola")},
            {"text": "Adiós", "pictogram": pictogram_payload(2280, "adiós")},
        ],
    }


def approve_material(client, material_id: str) -> None:
    client.post(f"/api/materials/{material_id}/submit")
    client.post(
        f"/api/materials/{material_id}/review",
        json={
            "outcome": "approved",
            "human_confirmed": True,
            "note": "Revisado para la demostración.",
        },
    )


def test_board_creation_and_listing(client) -> None:
    created = client.post("/api/materials/boards", json=board_payload())
    assert created.status_code == 201
    material_id = created.json()["material"]["material_id"]

    listing = client.get("/api/materials")
    assert listing.status_code == 200
    ids = [item["material_id"] for item in listing.json()["materials"]]
    assert material_id in ids


def test_export_pdf_after_approval(client) -> None:
    created = client.post("/api/materials/agendas", json=agenda_payload())
    material_id = created.json()["material"]["material_id"]
    approve_material(client, material_id)

    exported = client.get(f"/api/materials/{material_id}/export?format=pdf")
    assert exported.status_code == 200
    assert exported.json()["media_type"] == "application/pdf"


def test_get_material_returns_404(client) -> None:
    response = client.get("/api/materials/00000000-0000-0000-0000-000000000099")
    assert response.status_code == 404


def test_submit_unknown_material_returns_404(client) -> None:
    response = client.post("/api/materials/00000000-0000-0000-0000-000000000099/submit")
    assert response.status_code == 404


def test_review_before_submit_returns_409(client) -> None:
    created = client.post("/api/materials/agendas", json=agenda_payload())
    material_id = created.json()["material"]["material_id"]
    response = client.post(
        f"/api/materials/{material_id}/review",
        json={
            "outcome": "approved",
            "human_confirmed": True,
            "note": "Intento inválido.",
        },
    )
    assert response.status_code == 409
