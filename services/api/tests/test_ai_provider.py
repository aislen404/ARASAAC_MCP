from types import SimpleNamespace

import httpx
import pytest

from arasaac_platform.ai.provider import (
    OpenAIPlanner,
    PlannerResponseError,
    PlannerTimeoutError,
    PlannerUnavailableError,
    UnavailablePlanner,
    create_planner,
)
from arasaac_platform.schemas.ai import AIPlanInput, AITextPlan


def request() -> AIPlanInput:
    return AIPlanInput(
        material_type="visual_agenda",
        objective="Preparar una visita genérica a una biblioteca",
        item_count=2,
        no_personal_data_confirmed=True,
    )


class FakeResponses:
    def __init__(self) -> None:
        self.arguments: dict[str, object] = {}

    async def parse(self, **kwargs: object) -> object:
        self.arguments = kwargs
        return SimpleNamespace(
            output_parsed=AITextPlan(
                summary="Secuencia genérica",
                items=[
                    {"text": "Entrar", "search_term": "entrar"},
                    {"text": "Leer", "search_term": "leer"},
                ],
            )
        )


class FakeOpenAI:
    def __init__(self) -> None:
        self.responses = FakeResponses()


class RaisingResponses:
    def __init__(self, error: Exception) -> None:
        self._error = error

    async def parse(self, **kwargs: object) -> object:
        del kwargs
        raise self._error


class RaisingOpenAI:
    def __init__(self, error: Exception) -> None:
        self.responses = RaisingResponses(error)


@pytest.mark.anyio
async def test_openai_planner_uses_structured_text_without_tools_or_storage() -> None:
    fake = FakeOpenAI()
    planner = OpenAIPlanner(
        api_key="test-only",
        model="gpt-5.4-mini",
        client=fake,
    )

    result = await planner.plan(request())

    assert len(result.items) == 2
    assert fake.responses.arguments["text_format"] is AITextPlan
    assert fake.responses.arguments["store"] is False
    assert "tools" not in fake.responses.arguments
    assert "image" not in str(fake.responses.arguments).lower()


@pytest.mark.anyio
async def test_unavailable_planner_fails_closed() -> None:
    planner = UnavailablePlanner(reason="Sin configuración.")

    assert planner.status.available is False
    with pytest.raises(PlannerUnavailableError, match="Sin configuración"):
        await planner.plan(request())


@pytest.mark.anyio
async def test_openai_planner_maps_timeout_without_retrying_in_application() -> None:
    from openai import APITimeoutError

    planner = OpenAIPlanner(
        api_key="test-only",
        client=RaisingOpenAI(
            APITimeoutError(request=httpx.Request("POST", "https://api.openai.com"))
        ),
    )

    with pytest.raises(PlannerTimeoutError, match="tiempo"):
        await planner.plan(request())


@pytest.mark.anyio
async def test_openai_planner_maps_invalid_provider_response() -> None:
    planner = OpenAIPlanner(
        api_key="test-only",
        client=RaisingOpenAI(RuntimeError("invalid structured response")),
    )

    with pytest.raises(PlannerResponseError, match="propuesta segura"):
        await planner.plan(request())


def test_planner_factory_never_exposes_or_requires_key_when_disabled() -> None:
    disabled = create_planner({"AI_PROVIDER": "disabled"})
    missing_key = create_planner({"AI_PROVIDER": "openai"})
    missing_azure_key = create_planner(
        {
            "AI_PROVIDER": "azure",
            "AZURE_OPENAI_ENDPOINT": (
                "https://example.openai.azure.com/openai/v1"
            ),
        }
    )

    assert disabled.status.provider == "disabled"
    assert disabled.status.available is False
    assert missing_key.status.provider == "openai"
    assert missing_key.status.available is False
    assert "OPENAI_API_KEY" in (missing_key.status.reason or "")
    assert missing_azure_key.status.provider == "azure"
    assert missing_azure_key.status.available is False
    assert "AZURE_OPENAI_API_KEY" in (missing_azure_key.status.reason or "")


def test_azure_endpoint_is_normalized_and_validated() -> None:
    from arasaac_platform.ai.provider import normalize_azure_endpoint

    assert (
        normalize_azure_endpoint("https://example.openai.azure.com")
        == "https://example.openai.azure.com/openai/v1"
    )
    assert (
        normalize_azure_endpoint(
            "https://example.services.ai.azure.com/api/projects/proj-test/openai/v1/responses"
        )
        == "https://example.services.ai.azure.com/api/projects/proj-test/openai/v1"
    )

    invalid_host = create_planner(
        {
            "AI_PROVIDER": "azure",
            "AZURE_OPENAI_ENDPOINT": "https://evil.example.com/openai/v1",
            "AZURE_OPENAI_API_KEY": "test-only",
        }
    )
    assert invalid_host.status.available is False
    assert "services.ai.azure.com" in (invalid_host.status.reason or "")

    ready = create_planner(
        {
            "AI_PROVIDER": "azure",
            "AZURE_OPENAI_ENDPOINT": (
                "https://es-fasttrackdevelopment-delta-eu-llm.services.ai.azure.com/"
                "api/projects/proj-ES_FastTrackDevelopment_DELTA_EU_LLM/openai/v1"
            ),
            "AZURE_OPENAI_API_KEY": "test-only",
            "AZURE_OPENAI_MODEL": "FFD_DELTA_JSBV_gpt-5.4-mini",
        }
    )
    assert ready.status.available is True
    assert ready.status.provider == "azure"


@pytest.mark.anyio
async def test_openai_planner_maps_rate_limit_to_clear_message() -> None:
    from openai import RateLimitError

    planner = OpenAIPlanner(
        api_key="test-only",
        client=RaisingOpenAI(
            RateLimitError(
                "quota exceeded",
                response=httpx.Response(429, request=httpx.Request("POST", "https://api.openai.com")),
                body=None,
            )
        ),
    )

    with pytest.raises(PlannerResponseError, match="cuota o tasa"):
        await planner.plan(request())


@pytest.mark.anyio
async def test_openai_live_smoke_when_enabled() -> None:
    import os

    if os.getenv("OPENAI_LIVE_TEST") != "1":
        pytest.skip("OPENAI_LIVE_TEST no activado")
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        pytest.skip("OPENAI_API_KEY no configurada")

    planner = create_planner(
        {
            "AI_PROVIDER": "openai",
            "OPENAI_API_KEY": api_key,
            "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        }
    )
    assert planner.status.available is True
    result = await planner.plan(request())
    assert len(result.items) >= 1
    assert result.requires_human_selection is True
