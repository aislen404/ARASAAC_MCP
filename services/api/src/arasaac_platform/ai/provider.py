import json
import os
from typing import Protocol, cast

from arasaac_platform.schemas.ai import AIPlanInput, AIStatusResult, AITextPlan


SYSTEM_INSTRUCTIONS = """\
Eres un asistente de planificación de materiales accesibles no comerciales.
Tu única tarea es convertir una situación GENÉRICA en una secuencia breve de
conceptos cotidianos. No diagnostiques, no personalices para individuos, no
incluyas nombres ni datos personales y no des consejo médico, psicológico,
educativo o de CAA. No generes, describas ni imites pictogramas. Para cada elemento
devuelve solo un texto visible claro y un término breve que posteriormente se
buscará en el catálogo oficial ARASAAC. No afirmes que un término corresponde a un
pictograma concreto. Sigue exactamente el schema y el número solicitado.
"""


class PlannerError(RuntimeError):
    """Controlled AI provider failure."""


class PlannerUnavailableError(PlannerError):
    """AI provider is intentionally unavailable."""


class PlannerTimeoutError(PlannerError):
    """AI provider exceeded the configured deadline."""


class PlannerResponseError(PlannerError):
    """AI provider returned an invalid or rejected response."""


class AIPlanner(Protocol):
    @property
    def status(self) -> AIStatusResult: ...

    async def plan(self, request: AIPlanInput) -> AITextPlan: ...


class _ParsedResponse(Protocol):
    output_parsed: object | None


class _ResponsesAPI(Protocol):
    async def parse(self, **kwargs: object) -> _ParsedResponse: ...


class _OpenAIClient(Protocol):
    responses: _ResponsesAPI


class UnavailablePlanner:
    def __init__(
        self,
        *,
        provider: str = "disabled",
        reason: str = "La capa IA no está configurada.",
    ) -> None:
        self._provider = provider
        self._reason = reason

    @property
    def status(self) -> AIStatusResult:
        return AIStatusResult(
            available=False,
            provider=self._provider,
            model=None,
            reason=self._reason,
        )

    async def plan(self, request: AIPlanInput) -> AITextPlan:
        del request
        raise PlannerUnavailableError(self._reason)


class OpenAIPlanner:
    def __init__(
        self,
        *,
        api_key: str,
        model: str = "gpt-5.4-mini",
        timeout_seconds: float = 20.0,
        client: _OpenAIClient | None = None,
    ) -> None:
        self._model = model
        if client is None:
            from openai import AsyncOpenAI

            client = cast(
                _OpenAIClient,
                AsyncOpenAI(
                    api_key=api_key,
                    timeout=timeout_seconds,
                    max_retries=1,
                ),
            )
        self._client = client

    @property
    def status(self) -> AIStatusResult:
        return AIStatusResult(
            available=True,
            provider="openai",
            model=self._model,
            reason=None,
        )

    async def plan(self, request: AIPlanInput) -> AITextPlan:
        user_payload = json.dumps(
            {
                "material_type": request.material_type,
                "generic_scenario": request.objective,
                "item_count": request.item_count,
                "locale": request.locale,
            },
            ensure_ascii=False,
        )
        try:
            response = await self._client.responses.parse(
                model=self._model,
                instructions=SYSTEM_INSTRUCTIONS,
                input=user_payload,
                text_format=AITextPlan,
                store=False,
            )
        except Exception as exc:
            from openai import APITimeoutError

            if isinstance(exc, APITimeoutError):
                raise PlannerTimeoutError(
                    "El proveedor IA no respondió dentro del tiempo permitido."
                ) from exc
            raise PlannerResponseError(
                "No se pudo obtener una propuesta segura del proveedor IA."
            ) from exc

        parsed = response.output_parsed
        if parsed is None:
            raise PlannerResponseError(
                "El proveedor IA no devolvió un plan estructurado válido."
            )
        return cast(AITextPlan, parsed)


def create_planner(environ: dict[str, str] | None = None) -> AIPlanner:
    env = os.environ if environ is None else environ
    provider = env.get("AI_PROVIDER", "disabled").strip().lower()
    if provider != "openai":
        reason = (
            "La capa IA está desactivada."
            if provider == "disabled"
            else "AI_PROVIDER no está permitido."
        )
        return UnavailablePlanner(provider=provider or "disabled", reason=reason)

    api_key = env.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return UnavailablePlanner(
            provider="openai",
            reason="Falta OPENAI_API_KEY en el entorno del servidor.",
        )
    model = env.get("OPENAI_MODEL", "gpt-5.4-mini").strip() or "gpt-5.4-mini"
    timeout = _safe_timeout(env.get("AI_TIMEOUT_SECONDS"))
    return OpenAIPlanner(api_key=api_key, model=model, timeout_seconds=timeout)


def _safe_timeout(raw: str | None) -> float:
    try:
        value = float(raw) if raw is not None else 20.0
    except ValueError:
        return 20.0
    return min(max(value, 2.0), 60.0)
