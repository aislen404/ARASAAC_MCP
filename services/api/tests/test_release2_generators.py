from datetime import UTC, datetime

from arasaac_platform.domain.materials import PictogramReference
from arasaac_platform.repositories.memory import InMemoryRepository
from arasaac_platform.schemas.materials import (
    CreateDocumentInput,
    CreateSignageInput,
    CreateStoryInput,
    MaterialItemInput,
    ReviewMaterialInput,
)
from arasaac_platform.services.export import export_docx, export_zip_package
from arasaac_platform.services.materials import (
    create_document,
    create_signage,
    create_story,
    review,
    submit,
)


def pictogram(pictogram_id: int, label: str) -> PictogramReference:
    return PictogramReference(
        pictogram_id=pictogram_id,
        label=label,
        source_url=f"https://static.arasaac.org/pictograms/{pictogram_id}/{pictogram_id}_300.png",
        retrieved_at=datetime.now(UTC),
    )


def item(text: str, pictogram_id: int, label: str) -> MaterialItemInput:
    return MaterialItemInput(text=text, pictogram=pictogram(pictogram_id, label))


def approve(repository: InMemoryRepository, material_id) -> None:
    submit(material_id, repository)
    review(
        material_id,
        ReviewMaterialInput(
            outcome="approved",
            human_confirmed=True,
            note="Aprobado en test.",
        ),
        repository,
    )


def test_release2_generators_and_docx_export() -> None:
    repository = InMemoryRepository()
    document = create_document(
        CreateDocumentInput(
            title="Guía genérica",
            sections=[item("Entrada", 6964, "entrada")],
        ),
        repository,
    )
    story = create_story(
        CreateStoryInput(
            title="Historia genérica",
            scenes=[item("Saludo", 2280, "hola")],
        ),
        repository,
    )
    signage = create_signage(
        CreateSignageInput(
            title="Señalética genérica",
            signs=[
                item("Entrada", 6964, "entrada"),
                item("Salida", 2280, "salida"),
            ],
        ),
        repository,
    )
    assert document.material_type == "accessible_document"
    assert story.material_type == "social_story"
    assert signage.material_type == "signage"
    assert signage.arasaac_logo_included is False

    approve(repository, document.material_id)
    docx = export_docx(repository.get(document.material_id))
    assert docx.startswith(b"PK")
    zip_bytes = export_zip_package(repository.get(document.material_id))
    assert zip_bytes.startswith(b"PK")
