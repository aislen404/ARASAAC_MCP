import json
import os
from typing import Protocol, cast
from urllib.parse import urlparse

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

ALLOWED_AZURE_HOST_SUFFIXES = (".openai.azure.com", ".services.ai.azure.com")
AZURE_OPENAI_API_PATH = "/openai/v1"
FOUNDRY_PROJECT_PATH_PREFIX = "/api/projects/"


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
        provider: str = "openai",
        base_url: str | None = None,
        client: _OpenAIClient | None = None,
    ) -> None:
        self._model = model
        self._provider = provider
        if client is None:
            from openai import AsyncOpenAI

            client_kwargs: dict[str, object] = {
                "api_key": api_key,
                "timeout": timeout_seconds,
                "max_retries": 1,
            }
            if base_url is not None:
                client_kwargs["base_url"] = base_url
            client = cast(_OpenAIClient, AsyncOpenAI(**client_kwargs))
        self._client = client

    @property
    def status(self) -> AIStatusResult:
        return AIStatusResult(
            available=True,
            provider=self._provider,
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
            raise _map_provider_error(exc) from exc

        parsed = response.output_parsed
        if parsed is None:
            raise PlannerResponseError(
                "El proveedor IA no devolvió un plan estructurado válido."
            )
        return cast(AITextPlan, parsed)


def create_planner(environ: dict[str, str] | None = None) -> AIPlanner:
    env = os.environ if environ is None else environ
    provider = env.get("AI_PROVIDER", "disabled").strip().lower()
    timeout = _safe_timeout(env.get("AI_TIMEOUT_SECONDS"))

    if provider == "disabled":
        return UnavailablePlanner(provider="disabled", reason="La capa IA está desactivada.")

    if provider == "openai":
        return _create_openai_planner(env, timeout_seconds=timeout)

    if provider == "azure":
        return _create_azure_planner(env, timeout_seconds=timeout)

    return UnavailablePlanner(
        provider=provider or "disabled",
        reason="AI_PROVIDER no está permitido.",
    )


def _create_openai_planner(env: dict[str, str], *, timeout_seconds: float) -> AIPlanner:
    api_key = env.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return UnavailablePlanner(
            provider="openai",
            reason="Falta OPENAI_API_KEY en el entorno del servidor.",
        )
    model = env.get("OPENAI_MODEL", "gpt-5.4-mini").strip() or "gpt-5.4-mini"
    return OpenAIPlanner(api_key=api_key, model=model, timeout_seconds=timeout_seconds)


def _create_azure_planner(env: dict[str, str], *, timeout_seconds: float) -> AIPlanner:
    endpoint_raw = env.get("AZURE_OPENAI_ENDPOINT", "").strip()
    if not endpoint_raw:
        return UnavailablePlanner(
            provider="azure",
            reason="Falta AZURE_OPENAI_ENDPOINT en el entorno del servidor.",
        )

    endpoint_error = _validate_azure_endpoint(endpoint_raw)
    if endpoint_error is not None:
        return UnavailablePlanner(provider="azure", reason=endpoint_error)

    api_key = env.get("AZURE_OPENAI_API_KEY", "").strip()
    if not api_key:
        return UnavailablePlanner(
            provider="azure",
            reason="Falta AZURE_OPENAI_API_KEY en el entorno del servidor.",
        )

    model = (
        env.get("AZURE_OPENAI_MODEL", env.get("OPENAI_MODEL", "gpt-5.4-mini")).strip()
        or "gpt-5.4-mini"
    )
    return OpenAIPlanner(
        api_key=api_key,
        model=model,
        timeout_seconds=timeout_seconds,
        provider="azure",
        base_url=normalize_azure_endpoint(endpoint_raw),
    )


def normalize_azure_endpoint(raw: str) -> str:
    endpoint = raw.strip().rstrip("/")
    if endpoint.endswith("/responses"):
        endpoint = endpoint[: -len("/responses")].rstrip("/")

    parsed = urlparse(endpoint)
    host = (parsed.hostname or "").lower()
    path = parsed.path.rstrip("/")

    if host.endswith(".services.ai.azure.com"):
        return endpoint

    if not path.endswith(AZURE_OPENAI_API_PATH):
        endpoint = f"{endpoint}{AZURE_OPENAI_API_PATH}"
    return endpoint


def _validate_azure_endpoint(raw: str) -> str | None:
    normalized = normalize_azure_endpoint(raw)
    parsed = urlparse(normalized)
    host = (parsed.hostname or "").lower()
    path = parsed.path.rstrip("/")

    if parsed.scheme != "https":
        return "AZURE_OPENAI_ENDPOINT debe usar HTTPS."
    if not any(host.endswith(suffix) for suffix in ALLOWED_AZURE_HOST_SUFFIXES):
        return (
            "AZURE_OPENAI_ENDPOINT debe pertenecer a un recurso "
            "*.openai.azure.com o *.services.ai.azure.com."
        )

    if host.endswith(".services.ai.azure.com"):
        if not path.startswith(FOUNDRY_PROJECT_PATH_PREFIX):
            return (
                "AZURE_OPENAI_ENDPOINT de Foundry debe incluir "
                "/api/projects/<id>/openai/v1."
            )
        if not path.endswith(AZURE_OPENAI_API_PATH):
            return f"AZURE_OPENAI_ENDPOINT debe terminar en {AZURE_OPENAI_API_PATH}."
        parts = [part for part in path.split("/") if part]
        if (
            len(parts) != 5
            or parts[0] != "api"
            or parts[1] != "projects"
            or not parts[2]
            or parts[3] != "openai"
            or parts[4] != "v1"
        ):
            return (
                "AZURE_OPENAI_ENDPOINT de Foundry debe tener la forma "
                "/api/projects/<id>/openai/v1."
            )
        return None

    if path != AZURE_OPENAI_API_PATH:
        return f"AZURE_OPENAI_ENDPOINT debe apuntar a {AZURE_OPENAI_API_PATH}."
    return None


def _map_provider_error(exc: Exception) -> PlannerError:
    from openai import APITimeoutError, RateLimitError

    if isinstance(exc, APITimeoutError):
        return PlannerTimeoutError(
            "El proveedor IA no respondió dentro del tiempo permitido."
        )
    if isinstance(exc, RateLimitError):
        return PlannerResponseError(
            "El proveedor IA rechazó la petición por límite de cuota o tasa. "
            "Comprueba la capacidad del despliegue y la facturación del recurso."
        )
    return PlannerResponseError(
        "No se pudo obtener una propuesta segura del proveedor IA."
    )


def _safe_timeout(raw: str | None) -> float:
    try:
        value = float(raw) if raw is not None else 20.0
    except ValueError:
        return 20.0
    return min(max(value, 2.0), 60.0)
