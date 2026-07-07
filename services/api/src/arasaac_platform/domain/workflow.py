from datetime import UTC, datetime

from arasaac_platform.domain.materials import (
    Material,
    MaterialStatus,
    ReviewDecision,
    ReviewOutcome,
)


class InvalidMaterialTransition(ValueError):
    """Raised when a material workflow transition is not permitted."""


def submit_for_review(material: Material) -> Material:
    if material.status not in {MaterialStatus.DRAFT, MaterialStatus.REJECTED}:
        raise InvalidMaterialTransition("Solo un borrador o rechazo puede enviarse a revisión.")
    return material.model_copy(
        update={
            "status": MaterialStatus.IN_REVIEW,
            "review": None,
            "updated_at": datetime.now(UTC),
        }
    )


def decide_review(material: Material, decision: ReviewDecision) -> Material:
    if material.status != MaterialStatus.IN_REVIEW:
        raise InvalidMaterialTransition("Solo un material en revisión puede decidirse.")
    target = (
        MaterialStatus.APPROVED
        if decision.outcome == ReviewOutcome.APPROVED
        else MaterialStatus.REJECTED
    )
    return material.model_copy(
        update={
            "status": target,
            "review": decision,
            "updated_at": datetime.now(UTC),
        }
    )
