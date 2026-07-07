from datetime import UTC, datetime

import pytest

from arasaac_platform.ai.provider import PlannerResponseError
from arasaac_platform.domain.materials import PictogramReference
from arasaac_platform.schemas.ai import (
    AIPlanInput,
    AIStatusResult,
    AITextPlan,
)
from arasaac_platform.services.ai import build_ai_plan


def reference(label: str, pictogram_id: int) -> PictogramReference:
    return PictogramReference.model_validate(
        {
            "pictogram_id": pictogram_id,
            "label": label,
            "source_url": (
                f"https://static.arasaac.org/pictograms/"
                f"{pictogram_id}/{pictogram_id}_300.png"
            ),
            "retrieved_at": datetime.now(UTC),
        }
    )


class StubPlanner:
    def __init__(self, plan: AITextPlan) -> None:
        self._plan = plan
        self.received: AIPlanInput | None = None

    @property
    def status(self) -> AIStatusResult:
        return AIStatusResult(
            available=True,
            provider="test-ai",
            model="structured-test-model",
            reason=None,
        )

    async def plan(self, request: AIPlanInput) -> AITextPlan:
        self.received = request
        return self._plan


class StubArasaac:
    def __init__(self) -> None:
        self.queries: list[str] = []

    async def search(
        self,
        query: str,
        *,
        locale: str = "es",
        limit: int = 12,
    ) -> list[PictogramReference]:
        del locale
        self.queries.append(query)
        return [reference(query, 100 + len(self.queries))][:limit]


def input_for(count: int = 2) -> AIPlanInput:
    return AIPlanInput(
        material_type="visual_agenda",
        objective="Preparar una actividad genérica en la biblioteca",
        item_count=count,
        no_personal_data_confirmed=True,
    )


@pytest.mark.anyio
async def test_ai_plan_resolves_terms_to_real_arasaac_candidates() -> None:
    planner = StubPlanner(
        AITextPlan(
            summary="Secuencia para una actividad genérica",
            items=[
                {"text": "Entrar", "search_term": "entrada"},
                {"text": "Leer", "search_term": "leer"},
            ],
        )
    )
    arasaac = StubArasaac()

    result = await build_ai_plan(input_for(), planner, arasaac)  # type: ignore[arg-type]

    assert arasaac.queries == ["entrada", "leer"]
    assert result.requires_human_selection is True
    assert result.creates_material is False
    assert result.stores_input is False
    assert result.items[0].candidates[0].origin == "ARASAAC"


@pytest.mark.anyio
async def test_ai_plan_rejects_wrong_item_count_without_arasaac_calls() -> None:
    planner = StubPlanner(
        AITextPlan(
            summary="Plan incompleto",
            items=[{"text": "Entrar", "search_term": "entrada"}],
        )
    )
    arasaac = StubArasaac()

    with pytest.raises(PlannerResponseError, match="número de elementos"):
        await build_ai_plan(input_for(2), planner, arasaac)  # type: ignore[arg-type]

    assert arasaac.queries == []


@pytest.mark.anyio
async def test_ai_plan_revalidates_model_output_for_sensitive_content() -> None:
    planner = StubPlanner(
        AITextPlan(
            summary="Plan genérico",
            items=[
                {
                    "text": "Enviar correo a test@example.org",
                    "search_term": "correo",
                }
            ],
        )
    )

    with pytest.raises(ValueError, match="correo"):
        await build_ai_plan(input_for(1), planner, StubArasaac())  # type: ignore[arg-type]
