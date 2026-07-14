from datetime import UTC, datetime

import pytest

from arasaac_platform.domain.materials import Material, MaterialBlock, MaterialType, PictogramReference
from arasaac_platform.services.validation import ValidationContext, run_validators


def build_material(*, text: str = "Llegar", attribution_text: str | None = None) -> Material:
    pictogram = PictogramReference.model_validate(
        {
            "pictogram_id": 6964,
            "label": "casa",
            "source_url": "https://static.arasaac.org/pictograms/6964/6964_300.png",
            "retrieved_at": datetime.now(UTC),
        }
    )
    return Material(
        material_type=MaterialType.VISUAL_AGENDA,
        title="Agenda",
        blocks=[MaterialBlock(position=0, text=text, pictogram=pictogram)],
        attribution_text=attribution_text
        or (
            "Los símbolos pictográficos utilizados son propiedad del Gobierno de Aragón "
            "y han sido creados por Sergio Palao para ARASAAC "
            "(https://arasaac.org), que los distribuye bajo licencia CC BY-NC-SA."
        ),
    )


@pytest.mark.anyio
async def test_run_validators_returns_ok_findings_for_clean_material() -> None:
    report = await run_validators(build_material(), ValidationContext())

    assert report.is_blocking is False
    assert {finding.validator_id for finding in report.findings} == {
        "pictogram_ids_real",
        "license_notice_visible",
        "no_personal_data",
        "no_modified_pictograms",
        "non_commercial_context",
        "visual_density",
    }
    assert all(finding.detail for finding in report.findings)


@pytest.mark.anyio
async def test_run_validators_blocks_email_detection_without_echoing_pii() -> None:
    report = await run_validators(
        build_material(text="Escribe a persona@example.com"),
        ValidationContext(),
    )

    assert report.is_blocking is True
    finding = next(f for f in report.findings if f.validator_id == "no_personal_data")
    assert finding.severity == "blocker"
    assert "persona@example.com" not in finding.detail


@pytest.mark.anyio
async def test_run_validators_blocks_modified_pictogram_urls() -> None:
    material = build_material()
    pictogram = material.blocks[0].pictogram
    assert pictogram is not None
    material = material.model_copy(
        update={
            "blocks": [
                material.blocks[0].model_copy(
                    update={
                        "pictogram": pictogram.model_copy(
                            update={
                                "source_url": f"{pictogram.source_url}?bg=fff",
                            }
                        )
                    }
                )
            ]
        }
    )

    report = await run_validators(material, ValidationContext())

    finding = next(f for f in report.findings if f.validator_id == "no_modified_pictograms")
    assert finding.severity == "blocker"
