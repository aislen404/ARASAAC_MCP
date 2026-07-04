import json
import os

import httpx
import pytest

from arasaac_platform.arasaac.client import ArasaacClient, ArasaacConnectorError


def payload(pictogram_id: int, label: str) -> dict[str, object]:
    return {"_id": pictogram_id, "keywords": [{"keyword": label}]}


@pytest.mark.anyio
async def test_search_normalizes_and_limits_results() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/pictograms/es/search/casa"
        return httpx.Response(
            200,
            json=[payload(1, "casa"), payload(2, "vivienda")],
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://api.arasaac.org/api",
    ) as http:
        results = await ArasaacClient(client=http).search("casa", limit=1)

    assert len(results) == 1
    assert results[0].pictogram_id == 1
    assert str(results[0].source_url).startswith("https://static.arasaac.org/")
    assert results[0].license == "CC BY-NC-SA"


@pytest.mark.anyio
async def test_get_normalizes_detail() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/pictograms/es/6964"
        return httpx.Response(200, json=payload(6964, "casa"))

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://api.arasaac.org/api",
    ) as http:
        result = await ArasaacClient(client=http).get(6964)

    assert result.label == "casa"
    assert result.origin == "ARASAAC"


@pytest.mark.anyio
async def test_connector_maps_http_failure_without_leaking_body() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(503, text="internal upstream detail")
    )
    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.arasaac.org/api",
    ) as http:
        with pytest.raises(ArasaacConnectorError) as caught:
            await ArasaacClient(client=http).search("casa")

    assert "internal upstream detail" not in str(caught.value)


@pytest.mark.anyio
async def test_connector_rejects_invalid_json() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            content=b"not-json",
            headers={"content-type": "application/json"},
        )
    )
    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.arasaac.org/api",
    ) as http:
        with pytest.raises(ArasaacConnectorError):
            await ArasaacClient(client=http).search("casa")


@pytest.mark.parametrize(
    ("query", "locale", "limit"),
    [
        ("", "es", 1),
        ("x" * 121, "es", 1),
        ("casa", "xx", 1),
        ("casa", "es", 0),
        ("casa", "es", 51),
    ],
)
@pytest.mark.anyio
async def test_connector_rejects_invalid_input_before_network(
    query: str,
    locale: str,
    limit: int,
) -> None:
    transport = httpx.MockTransport(
        lambda request: pytest.fail("No debe acceder a red con input inválido.")
    )
    async with httpx.AsyncClient(
        transport=transport,
        base_url="https://api.arasaac.org/api",
    ) as http:
        with pytest.raises(ValueError):
            await ArasaacClient(client=http).search(
                query,
                locale=locale,
                limit=limit,
            )


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("ARASAAC_LIVE_TEST") != "1",
    reason="Set ARASAAC_LIVE_TEST=1 to call the official API.",
)
@pytest.mark.anyio
async def test_official_api_contract() -> None:
    result = await ArasaacClient().search("casa", limit=1)

    assert result
    assert result[0].origin == "ARASAAC"
    json.dumps(result[0].model_dump(mode="json"))
