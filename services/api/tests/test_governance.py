from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from arasaac_platform.domain.materials import (
    Material,
    MaterialBlock,
    MaterialType,
    PictogramReference,
)
from arasaac_platform.governance.license import validate_material_license


def pictogram() -> PictogramReference:
    return PictogramReference(
        pictogram_id=123,
        label="actividad",
        source_url="https://static.arasaac.org/pictograms/123/123_300.png",
        retrieved_at=datetime.now(UTC),
    )


def test_compliant_material_is_valid() -> None:
    material = Material(
        material_type=MaterialType.VISUAL_AGENDA,
        title="Agenda de ejemplo",
        blocks=[MaterialBlock(position=0, text="Actividad", pictogram=pictogram())],
    )

    result = validate_material_license(material)

    assert result.valid is True
    assert result.errors == []


def test_signage_requires_arasaac_logo() -> None:
    material = Material(
        material_type=MaterialType.SIGNAGE,
        title="Señal de ejemplo",
        blocks=[MaterialBlock(position=0, text="Entrada", pictogram=pictogram())],
    )

    result = validate_material_license(material)

    assert result.valid is False
    assert "logotipo ARASAAC" in result.errors[0]


def test_pictogram_rejects_non_arasaac_source() -> None:
    with pytest.raises(ValidationError, match="arasaac.org"):
        PictogramReference(
            pictogram_id=123,
            label="actividad",
            source_url="https://example.com/123.png",
            retrieved_at=datetime.now(UTC),
        )
