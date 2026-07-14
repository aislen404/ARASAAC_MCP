from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from arasaac_platform.domain.materials import (
    Material,
    MaterialBlock,
    MaterialStatus,
    MaterialType,
    PictogramReference,
    ReviewDecision,
    ReviewOutcome,
)
from arasaac_platform.domain.workspaces import Workspace
from arasaac_platform.domain.workflow import (
    InvalidMaterialTransition,
    decide_review,
    submit_for_review,
)


def test_material_rejects_extra_personal_fields() -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        Material.model_validate(
            {
                "material_type": "visual_agenda",
                "title": "Agenda genérica",
                "person_name": "Dato no permitido",
            }
        )


def test_pictogram_metadata_is_immutable() -> None:
    reference = PictogramReference(
        pictogram_id=456,
        label="descanso",
        source_url="https://static.arasaac.org/pictograms/456/456_300.png",
        retrieved_at=datetime.now(UTC),
    )

    with pytest.raises(ValidationError):
        reference.label = "modificado"  # type: ignore[misc]


def test_human_review_controls_approval() -> None:
    workspace = Workspace(slug="tortuga-ligero-sendero")
    draft = Material(
        workspace_id=workspace.workspace_id,
        material_type=MaterialType.COMMUNICATION_BOARD,
        title="Tablero genérico",
        blocks=[MaterialBlock(position=0, text="Sí")],
    )
    in_review = submit_for_review(draft)
    approved = decide_review(
        in_review,
        ReviewDecision(
            outcome=ReviewOutcome.APPROVED,
            human_confirmed=True,
            note="Contenido revisado por una persona responsable.",
        ),
    )

    assert in_review.status == MaterialStatus.IN_REVIEW
    assert approved.status == MaterialStatus.APPROVED
    assert approved.review is not None
    assert approved.review.human_confirmed is True


def test_approval_cannot_skip_review() -> None:
    workspace = Workspace(slug="ciervo-vivo-brisa")
    draft = Material(
        workspace_id=workspace.workspace_id,
        material_type=MaterialType.VISUAL_AGENDA,
        title="Agenda genérica",
    )

    with pytest.raises(InvalidMaterialTransition):
        decide_review(
            draft,
            ReviewDecision(
                outcome=ReviewOutcome.APPROVED,
                human_confirmed=True,
                note="Intento inválido.",
            ),
        )
