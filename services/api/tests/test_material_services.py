import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from io import BytesIO

import pytest
from pydantic import ValidationError
from pypdf import PdfReader

from arasaac_platform.domain.materials import (
    MaterialStatus,
    PictogramReference,
    ReviewOutcome,
)
from arasaac_platform.repositories.memory import InMemoryRepository
from arasaac_platform.schemas.materials import (
    CreateAgendaInput,
    CreateBoardInput,
    MaterialItemInput,
    ReviewMaterialInput,
)
from arasaac_platform.services.export import ExportBlockedError, export_html, export_pdf
from arasaac_platform.services.materials import create_agenda, create_board, review, submit


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk"
    "+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def item(text: str = "Actividad") -> MaterialItemInput:
    pictogram = PictogramReference.model_validate(
        {
            "pictogram_id": 6964,
            "label": text.lower(),
            "source_url": "https://static.arasaac.org/pictograms/6964/6964_300.png",
            "retrieved_at": datetime.now(UTC),
        }
    )
    return MaterialItemInput(text=text, pictogram=pictogram)


def approve(material_id, repository: InMemoryRepository):
    submit(material_id, repository)
    return review(
        material_id,
        ReviewMaterialInput(
            outcome=ReviewOutcome.APPROVED,
            human_confirmed=True,
            note="Revisión humana completada.",
        ),
        repository,
    )


def test_generators_create_attributed_drafts_and_audit() -> None:
    repository = InMemoryRepository()
    agenda = create_agenda(
        CreateAgendaInput(title="Agenda genérica", steps=[item()]),
        repository,
    )
    board = create_board(
        CreateBoardInput(title="Tablero genérico", cells=[item("Sí"), item("No")]),
        repository,
    )

    assert agenda.status == MaterialStatus.DRAFT
    assert board.status == MaterialStatus.DRAFT
    assert agenda.attribution_visible is True
    assert [event.action for event in repository.events_for(agenda.material_id)] == [
        "created"
    ]


def test_repository_preserves_concurrent_creations() -> None:
    repository = InMemoryRepository()

    def create(index: int) -> None:
        create_agenda(
            CreateAgendaInput(title=f"Agenda {index}", steps=[item()]),
            repository,
        )

    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(create, range(20)))

    assert len(repository.list_materials()) == 20


def test_board_rejects_too_few_cells_and_extra_pii() -> None:
    with pytest.raises(ValidationError):
        CreateBoardInput(title="Tablero", cells=[item()])
    with pytest.raises(ValidationError):
        CreateAgendaInput.model_validate(
            {
                "title": "Agenda",
                "steps": [item().model_dump(mode="json")],
                "person_name": "No permitido",
            }
        )


def test_export_blocks_draft_and_escapes_html_after_approval() -> None:
    repository = InMemoryRepository()
    draft = create_agenda(
        CreateAgendaInput(title="<Agenda>", steps=[item("<Actividad>")]),
        repository,
    )
    with pytest.raises(ExportBlockedError):
        export_html(draft)

    approved = approve(draft.material_id, repository)
    output = export_html(approved).decode()

    assert "&lt;Agenda&gt;" in output
    assert "&lt;Actividad&gt;" in output
    assert "Sergio Palao" in output
    assert "static.arasaac.org" in output


@pytest.mark.anyio
async def test_pdf_contains_attribution_after_approval() -> None:
    repository = InMemoryRepository()
    draft = create_agenda(
        CreateAgendaInput(title="Agenda", steps=[item()]),
        repository,
    )
    approved = approve(draft.material_id, repository)

    async def fetch_image(url: str) -> bytes:
        assert url.startswith("https://static.arasaac.org/")
        return PNG_1X1

    output = await export_pdf(approved, fetch_image=fetch_image)

    assert output.startswith(b"%PDF")
    text = "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(output)).pages)
    assert "Sergio Palao" in text
    assert "ARASAAC" in text
