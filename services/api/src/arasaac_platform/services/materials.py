from uuid import UUID

from arasaac_platform.domain.materials import (
    AuditAction,
    AuditEvent,
    Material,
    MaterialBlock,
    MaterialType,
    ReviewDecision,
)
from arasaac_platform.domain.workflow import decide_review, submit_for_review
from arasaac_platform.governance.license import validate_material_license
from arasaac_platform.repositories.base import Repository
from arasaac_platform.schemas.materials import (
    CreateAgendaInput,
    CreateBoardInput,
    ReviewMaterialInput,
)


class MaterialComplianceError(ValueError):
    """Raised when a generated material violates governance."""


def create_agenda(
    request: CreateAgendaInput,
    repository: Repository,
) -> Material:
    material = Material(
        material_type=MaterialType.VISUAL_AGENDA,
        title=request.title,
        blocks=[
            MaterialBlock(
                position=position,
                text=item.text,
                pictogram=item.pictogram,
            )
            for position, item in enumerate(request.steps)
        ],
    )
    return _save_created(material, repository)


def create_board(
    request: CreateBoardInput,
    repository: Repository,
) -> Material:
    material = Material(
        material_type=MaterialType.COMMUNICATION_BOARD,
        title=request.title,
        blocks=[
            MaterialBlock(
                position=position,
                text=item.text,
                pictogram=item.pictogram,
            )
            for position, item in enumerate(request.cells)
        ],
    )
    return _save_created(material, repository)


def submit(material_id: UUID, repository: Repository) -> Material:
    material = submit_for_review(repository.get(material_id))
    repository.save(material)
    _audit(repository, material, AuditAction.SUBMITTED, "Enviado a revisión humana.")
    return material


def review(
    material_id: UUID,
    request: ReviewMaterialInput,
    repository: Repository,
) -> Material:
    decision = ReviewDecision(
        outcome=request.outcome,
        human_confirmed=request.human_confirmed,
        note=request.note,
    )
    material = decide_review(repository.get(material_id), decision)
    repository.save(material)
    _audit(repository, material, AuditAction.REVIEWED, f"Decisión: {request.outcome}.")
    return material


def _save_created(
    material: Material,
    repository: Repository,
) -> Material:
    compliance = validate_material_license(material)
    if not compliance.valid:
        raise MaterialComplianceError("; ".join(compliance.errors))
    repository.save(material)
    _audit(repository, material, AuditAction.CREATED, "Borrador creado.")
    return material


def _audit(
    repository: Repository,
    material: Material,
    action: AuditAction,
    detail: str,
) -> None:
    repository.append_event(
        AuditEvent(
            material_id=material.material_id,
            action=action,
            detail=detail,
        )
    )
