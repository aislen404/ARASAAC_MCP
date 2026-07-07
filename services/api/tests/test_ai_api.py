from datetime import UTC, datetime

from fastapi.testclient import TestClient

from arasaac_platform.ai.provider import UnavailablePlanner
from arasaac_platform.api.ai import get_ai_planner
from arasaac_platform.api.pictograms import get_arasaac_client
from arasaac_platform.domain.materials import PictogramReference
from arasaac_platform.main import app
from arasaac_platform.schemas.ai import (
    AIPlanInput,
    AIStatusResult,
    AITextPlan,
)


class StubPlanner:
    calls = 0

    @property
    def status(self) -> AIStatusResult:
        return AIStatusResult(
            available=True,
            provider="test-ai",
            model="test-model",
            reason=None,
        )

    async def plan(self, request: AIPlanInput) -> AITextPlan:
        type(self).calls += 1
        return AITextPlan(
            summary="Propuesta para una visita genérica",
            items=[
                {
                    "text": f"Paso {index + 1}",
                    "search_term": "biblioteca",
                }
                for index in range(request.item_count)
            ],
        )


class StubArasaac:
    async def search(
        self,
        query: str,
        *,
        locale: str = "es",
        limit: int = 12,
    ) -> list[PictogramReference]:
        del query, locale, limit
        return [
            PictogramReference.model_validate(
                {
                    "pictogram_id": 6964,
                    "label": "biblioteca",
                    "source_url": (
                        "https://static.arasaac.org/pictograms/6964/6964_300.png"
                    ),
                    "retrieved_at": datetime.now(UTC),
                }
            )
        ]


def client() -> TestClient:
    app.dependency_overrides[get_ai_planner] = StubPlanner
    app.dependency_overrides[get_arasaac_client] = StubArasaac
    return TestClient(app)


def payload() -> dict[str, object]:
    return {
        "material_type": "visual_agenda",
        "objective": "Preparar una visita genérica a una biblioteca",
        "item_count": 2,
        "locale": "es",
        "no_personal_data_confirmed": True,
    }


def test_ai_status_has_safe_public_contract() -> None:
    body = client().get("/api/ai/status").json()

    assert body == {
        "available": True,
        "provider": "test-ai",
        "model": "test-model",
        "reason": None,
        "generates_pictograms": False,
        "requires_human_selection": True,
        "stores_input": False,
    }
    assert "key" not in str(body).lower()


def test_ai_plan_returns_candidate_groups_without_creating_material() -> None:
    response = client().post("/api/ai/plan", json=payload())

    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 2
    assert body["requires_human_selection"] is True
    assert body["creates_material"] is False
    assert body["stores_input"] is False
    assert body["items"][0]["candidates"][0]["origin"] == "ARASAAC"


def test_ai_plan_rejects_extra_fields_and_missing_confirmation() -> None:
    extra = payload() | {"arbitrary_url": "https://example.org"}
    missing_confirmation = payload()
    del missing_confirmation["no_personal_data_confirmed"]

    assert client().post("/api/ai/plan", json=extra).status_code == 422
    assert (
        client().post("/api/ai/plan", json=missing_confirmation).status_code == 422
    )


def test_ai_plan_blocks_sensitive_input_before_provider_call() -> None:
    StubPlanner.calls = 0
    unsafe = payload() | {"objective": "Escribe a demo para test@example.org"}

    response = client().post("/api/ai/plan", json=unsafe)

    assert response.status_code == 422
    assert StubPlanner.calls == 0
    assert "correo" in response.json()["detail"]


def test_ai_plan_returns_503_when_provider_is_not_configured() -> None:
    app.dependency_overrides[get_ai_planner] = lambda: UnavailablePlanner(
        reason="IA no configurada para esta demo."
    )
    test_client = TestClient(app)

    response = test_client.post("/api/ai/plan", json=payload())

    assert response.status_code == 503
    assert response.json()["detail"] == "IA no configurada para esta demo."
    app.dependency_overrides[get_ai_planner] = StubPlanner
