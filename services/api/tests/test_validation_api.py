from datetime import UTC, datetime


def payload(text: str = "Llegar") -> dict[str, object]:
    return {
        "title": "Agenda de validación",
        "steps": [
            {
                "text": text,
                "pictogram": {
                    "pictogram_id": 6964,
                    "label": "casa",
                    "source_url": "https://static.arasaac.org/pictograms/6964/6964_300.png",
                    "retrieved_at": datetime.now(UTC).isoformat(),
                },
            }
        ],
    }


def _create_workspace(client) -> str:
    response = client.post("/api/workspaces", json={})
    assert response.status_code == 201
    return response.json()["workspace"]["slug"]


def test_validate_material_returns_report_and_audit_event(client) -> None:
    slug = _create_workspace(client)
    created = client.post(f"/api/workspaces/{slug}/materials/agendas", json=payload())
    material_id = created.json()["material"]["material_id"]

    validated = client.post(f"/api/workspaces/{slug}/materials/{material_id}/validate")

    assert validated.status_code == 200
    body = validated.json()
    assert body["material_id"] == material_id
    assert body["material_version"] == 1
    assert isinstance(body["validators_run"], list)
    assert isinstance(body["findings"], list)

    audit = client.get(f"/api/workspaces/{slug}/materials/{material_id}/audit").json()["events"]
    assert [event["action"] for event in audit] == ["created", "material_accessed", "validated"]
    assert "blocker=" in audit[-1]["detail"]


def test_validate_material_returns_404_for_unknown_material(client) -> None:
    slug = _create_workspace(client)
    response = client.post(f"/api/workspaces/{slug}/materials/00000000-0000-0000-0000-000000000099/validate")

    assert response.status_code == 404


def test_validate_material_is_idempotent_for_same_version(client) -> None:
    slug = _create_workspace(client)
    created = client.post(f"/api/workspaces/{slug}/materials/agendas", json=payload("Hola"))
    material_id = created.json()["material"]["material_id"]

    first = client.post(f"/api/workspaces/{slug}/materials/{material_id}/validate")
    second = client.post(f"/api/workspaces/{slug}/materials/{material_id}/validate")

    first_json = first.json()
    second_json = second.json()
    assert first_json["material_id"] == second_json["material_id"]
    assert first_json["material_version"] == second_json["material_version"]
    assert sorted(first_json["validators_run"]) == sorted(second_json["validators_run"])
    assert sorted(first_json["findings"], key=lambda item: item["validator_id"]) == sorted(
        second_json["findings"], key=lambda item: item["validator_id"]
    )