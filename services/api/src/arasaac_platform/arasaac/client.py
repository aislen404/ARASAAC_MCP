from datetime import UTC, datetime
from urllib.parse import quote

import httpx
from pydantic import BaseModel, ConfigDict, Field

from arasaac_platform.domain.materials import PictogramReference

ARASAAC_API_BASE = "https://api.arasaac.org/api"
ARASAAC_STATIC_BASE = "https://static.arasaac.org/pictograms"
ALLOWED_LOCALES = frozenset({"es", "en", "fr", "de", "it", "pt"})


class ArasaacConnectorError(RuntimeError):
    """Controlled failure from the approved ARASAAC connector."""


class _Keyword(BaseModel):
    model_config = ConfigDict(extra="ignore")

    keyword: str = Field(min_length=1)


class _PictogramPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    pictogram_id: int = Field(alias="_id", gt=0)
    keywords: list[_Keyword] = Field(min_length=1)


class ArasaacClient:
    def __init__(
        self,
        *,
        client: httpx.AsyncClient | None = None,
        timeout_seconds: float = 8.0,
    ) -> None:
        self._client = client
        self._timeout = timeout_seconds

    async def search(
        self,
        query: str,
        *,
        locale: str = "es",
        limit: int = 12,
    ) -> list[PictogramReference]:
        normalized_query = query.strip()
        self._validate(locale=locale, query=normalized_query, limit=limit)
        encoded = quote(normalized_query, safe="")
        payload = await self._get_json(f"/pictograms/{locale}/search/{encoded}")
        if not isinstance(payload, list):
            raise ArasaacConnectorError("Respuesta de búsqueda ARASAAC inválida.")
        return [
            self._normalize(_PictogramPayload.model_validate(item))
            for item in payload[:limit]
        ]

    async def get(self, pictogram_id: int, *, locale: str = "es") -> PictogramReference:
        if pictogram_id <= 0:
            raise ValueError("pictogram_id debe ser positivo.")
        self._validate(locale=locale)
        payload = await self._get_json(f"/pictograms/{locale}/{pictogram_id}")
        if not isinstance(payload, dict):
            raise ArasaacConnectorError("Respuesta de detalle ARASAAC inválida.")
        return self._normalize(_PictogramPayload.model_validate(payload))

    async def _get_json(self, path: str) -> object:
        try:
            if self._client is not None:
                response = await self._client.get(path, timeout=self._timeout)
            else:
                async with httpx.AsyncClient(
                    base_url=ARASAAC_API_BASE,
                    follow_redirects=False,
                ) as client:
                    response = await client.get(path, timeout=self._timeout)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ArasaacConnectorError("No se pudo consultar la API oficial ARASAAC.") from exc

    @staticmethod
    def _validate(
        *,
        locale: str,
        query: str | None = None,
        limit: int | None = None,
    ) -> None:
        if locale not in ALLOWED_LOCALES:
            raise ValueError("Locale no permitido.")
        if query is not None and (not query or len(query) > 120):
            raise ValueError("La búsqueda debe contener entre 1 y 120 caracteres.")
        if limit is not None and not 1 <= limit <= 50:
            raise ValueError("El límite debe estar entre 1 y 50.")

    @staticmethod
    def _normalize(payload: _PictogramPayload) -> PictogramReference:
        label = payload.keywords[0].keyword
        pictogram_id = payload.pictogram_id
        return PictogramReference.model_validate(
            {
                "pictogram_id": pictogram_id,
                "label": label,
                "source_url": (
                    f"{ARASAAC_STATIC_BASE}/{pictogram_id}/{pictogram_id}_300.png"
                ),
                "retrieved_at": datetime.now(UTC),
            }
        )
