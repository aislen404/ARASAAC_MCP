import httpx
import pytest

from arasaac_platform.arasaac.client import ArasaacClient
from arasaac_platform.schemas.pictograms import (
    SearchPictogramsInput,
    SuggestPictogramsInput,
)
from arasaac_platform.services.pictograms import (
    search_pictograms,
    suggest_pictograms,
)


def handler(request: httpx.Request) -> httpx.Response:
    term = request.url.path.rsplit("/", 1)[-1]
    return httpx.Response(
        200,
        json=[{"_id": len(term) + 100, "keywords": [{"keyword": term}]}],
    )


@pytest.mark.anyio
async def test_search_requires_human_selection() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://api.arasaac.org/api",
    ) as http:
        result = await search_pictograms(
            SearchPictogramsInput(query="casa", limit=1),
            ArasaacClient(client=http),
        )

    assert result.requires_human_selection is True
    assert result.candidates[0].label == "casa"


@pytest.mark.anyio
async def test_suggestions_are_deterministic_and_unique() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://api.arasaac.org/api",
    ) as http:
        result = await suggest_pictograms(
            SuggestPictogramsInput(
                text="Casa casa descanso",
                max_terms=2,
                results_per_term=1,
            ),
            ArasaacClient(client=http),
        )

    assert [item.term for item in result.suggestions] == ["casa", "descanso"]
    assert result.requires_human_selection is True
