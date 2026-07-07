from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from arasaac_platform.arasaac.client import ArasaacClient, ArasaacConnectorError
from arasaac_platform.domain.materials import PictogramReference
from arasaac_platform.schemas.pictograms import (
    GetPictogramInput,
    PictogramSearchResult,
    PictogramSuggestionsResult,
    SearchPictogramsInput,
    SuggestPictogramsInput,
)
from arasaac_platform.services.pictograms import (
    get_pictogram,
    search_pictograms,
    suggest_pictograms,
)

router = APIRouter(prefix="/api/pictograms", tags=["pictograms"])


def get_arasaac_client() -> ArasaacClient:
    return ArasaacClient()


@router.post("/search", response_model=PictogramSearchResult)
async def search(
    request: SearchPictogramsInput,
    client: Annotated[ArasaacClient, Depends(get_arasaac_client)],
) -> PictogramSearchResult:
    try:
        return await search_pictograms(request, client)
    except ArasaacConnectorError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/{pictogram_id}", response_model=PictogramReference)
async def detail(
    pictogram_id: Annotated[int, Path(gt=0)],
    client: Annotated[ArasaacClient, Depends(get_arasaac_client)],
    locale: Annotated[
        str,
        Query(pattern="^(es|en|fr|de|it|pt)$"),
    ] = "es",
) -> PictogramReference:
    try:
        request = GetPictogramInput(pictogram_id=pictogram_id, locale=locale)
        return await get_pictogram(request, client)
    except ArasaacConnectorError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/suggest", response_model=PictogramSuggestionsResult)
async def suggest(
    request: SuggestPictogramsInput,
    client: Annotated[ArasaacClient, Depends(get_arasaac_client)],
) -> PictogramSuggestionsResult:
    try:
        return await suggest_pictograms(request, client)
    except ArasaacConnectorError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
