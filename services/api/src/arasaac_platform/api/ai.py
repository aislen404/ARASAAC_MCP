from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from arasaac_platform.ai import (
    AIPlanner,
    PlannerResponseError,
    PlannerTimeoutError,
    PlannerUnavailableError,
    create_planner,
)
from arasaac_platform.ai.privacy import PrivacyViolation
from arasaac_platform.api.pictograms import get_arasaac_client
from arasaac_platform.arasaac.client import ArasaacClient, ArasaacConnectorError
from arasaac_platform.schemas.ai import AIPlanInput, AIPlanResult, AIStatusResult
from arasaac_platform.services.ai import build_ai_plan

router = APIRouter(prefix="/api/ai", tags=["ai-assistant"])


@lru_cache(maxsize=1)
def get_ai_planner() -> AIPlanner:
    return create_planner()


PlannerDependency = Annotated[AIPlanner, Depends(get_ai_planner)]
ArasaacDependency = Annotated[ArasaacClient, Depends(get_arasaac_client)]


@router.get("/status", response_model=AIStatusResult)
def status(planner: PlannerDependency) -> AIStatusResult:
    return planner.status


@router.post("/plan", response_model=AIPlanResult)
async def plan(
    request: AIPlanInput,
    planner: PlannerDependency,
    arasaac: ArasaacDependency,
) -> AIPlanResult:
    try:
        return await build_ai_plan(request, planner, arasaac)
    except PrivacyViolation as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except PlannerUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except PlannerTimeoutError as exc:
        raise HTTPException(status_code=504, detail=str(exc)) from exc
    except (PlannerResponseError, ArasaacConnectorError) as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
