import os
from datetime import UTC, datetime

import pytest

from arasaac_platform.domain.materials import PictogramReference
from arasaac_platform.repositories.sql import SqlRepository
from arasaac_platform.schemas.materials import CreateAgendaInput, MaterialItemInput
from arasaac_platform.services.materials import create_agenda


@pytest.mark.integration
def test_postgres_repository_persists_material() -> None:
    database_url = os.getenv("POSTGRES_TEST_URL")
    if not database_url:
        pytest.skip("POSTGRES_TEST_URL no configurada")

    repository = SqlRepository(database_url)
    repository.clear()
    pictogram = PictogramReference(
        pictogram_id=6964,
        label="casa",
        source_url="https://static.arasaac.org/pictograms/6964/6964_300.png",
        retrieved_at=datetime.now(UTC),
    )
    material = create_agenda(
        CreateAgendaInput(
            title="Persistencia Postgres",
            steps=[MaterialItemInput(text="Entrar", pictogram=pictogram)],
        ),
        repository,
    )
    loaded = repository.get(material.material_id)
    assert loaded.title == "Persistencia Postgres"
