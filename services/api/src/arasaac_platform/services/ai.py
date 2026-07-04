from arasaac_platform.ai import AIPlanner, PlannerResponseError
from arasaac_platform.ai.privacy import PrivacyViolation, validate_generic_text
from arasaac_platform.arasaac.client import ArasaacClient
from arasaac_platform.schemas.ai import (
    AIPlanInput,
    AIPlanResult,
    AIResolvedItem,
)


async def build_ai_plan(
    request: AIPlanInput,
    planner: AIPlanner,
    arasaac: ArasaacClient,
) -> AIPlanResult:
    safe_objective = validate_generic_text(request.objective)
    if len(safe_objective) < 10:
        raise PrivacyViolation(
            "El escenario genérico debe contener al menos 10 caracteres."
        )
    safe_request = request.model_copy(update={"objective": safe_objective})
    plan = await planner.plan(safe_request)

    if len(plan.items) != request.item_count:
        raise PlannerResponseError(
            "La propuesta IA no respetó el número de elementos solicitado."
        )

    resolved: list[AIResolvedItem] = []
    for item in plan.items:
        safe_text = validate_generic_text(item.text)
        safe_term = validate_generic_text(item.search_term)
        candidates = await arasaac.search(
            safe_term,
            locale=request.locale,
            limit=3,
        )
        resolved.append(
            AIResolvedItem(
                text=safe_text,
                search_term=safe_term,
                candidates=candidates,
            )
        )

    status = planner.status
    if not status.model:
        raise PlannerResponseError("El proveedor IA no informó un modelo.")
    return AIPlanResult(
        summary=validate_generic_text(plan.summary),
        items=resolved,
        provider=status.provider,
        model=status.model,
    )
