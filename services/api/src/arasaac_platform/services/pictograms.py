import re

from arasaac_platform.arasaac.client import ArasaacClient
from arasaac_platform.domain.materials import PictogramReference
from arasaac_platform.schemas.pictograms import (
    GetPictogramInput,
    PictogramSearchResult,
    PictogramSuggestion,
    PictogramSuggestionsResult,
    SearchPictogramsInput,
    SuggestPictogramsInput,
)


async def search_pictograms(
    request: SearchPictogramsInput,
    client: ArasaacClient,
) -> PictogramSearchResult:
    candidates = await client.search(
        request.query,
        locale=request.locale,
        limit=request.limit,
    )
    return PictogramSearchResult(
        query=request.query,
        locale=request.locale,
        candidates=candidates,
    )


async def get_pictogram(
    request: GetPictogramInput,
    client: ArasaacClient,
) -> PictogramReference:
    return await client.get(request.pictogram_id, locale=request.locale)


async def suggest_pictograms(
    request: SuggestPictogramsInput,
    client: ArasaacClient,
) -> PictogramSuggestionsResult:
    terms = _unique_terms(request.text)[: request.max_terms]
    suggestions: list[PictogramSuggestion] = []
    for term in terms:
        candidates = await client.search(
            term,
            locale=request.locale,
            limit=request.results_per_term,
        )
        suggestions.append(PictogramSuggestion(term=term, candidates=candidates))
    return PictogramSuggestionsResult(suggestions=suggestions)


def _unique_terms(text: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for term in re.findall(r"[^\W\d_]{2,}", text.lower(), flags=re.UNICODE):
        if term not in seen:
            seen.add(term)
            result.append(term)
    return result
