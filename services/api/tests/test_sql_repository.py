from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine, text

from arasaac_platform.domain.materials import AuditAction, AuditEvent
from arasaac_platform.repositories.sql import SqlRepository
from arasaac_platform.schemas.materials import CreateAgendaInput, MaterialItemInput
from arasaac_platform.services.materials import create_agenda
from arasaac_platform.domain.materials import PictogramReference


def request() -> CreateAgendaInput:
    pictogram = PictogramReference.model_validate(
        {
            "pictogram_id": 6964,
            "label": "casa",
            "source_url": "https://static.arasaac.org/pictograms/6964/6964_300.png",
            "retrieved_at": datetime.now(UTC),
        }
    )
    return CreateAgendaInput(
        title="Agenda persistente",
        steps=[MaterialItemInput(text="Llegar", pictogram=pictogram)],
    )


def test_material_and_audit_survive_repository_restart(tmp_path) -> None:
    url = f"sqlite+pysqlite:///{tmp_path / 'mvp.db'}"
    first = SqlRepository(url)
    material = create_agenda(request(), first)
    first.append_event(
        AuditEvent(
            material_id=material.material_id,
            action=AuditAction.UPDATED,
            detail="Evento persistente.",
        )
    )

    restarted = SqlRepository(url)
    restored = restarted.get(material.material_id)
    events = restarted.events_for(material.material_id)

    assert restored == material
    assert [event.action for event in events] == ["created", "updated"]


def test_corrupt_payload_is_rejected_on_read(tmp_path) -> None:
    url = f"sqlite+pysqlite:///{tmp_path / 'corrupt.db'}"
    repository = SqlRepository(url)
    material = create_agenda(request(), repository)
    engine = create_engine(url)
    with engine.begin() as connection:
        connection.execute(
            text("UPDATE materials SET payload = :payload WHERE material_id = :id"),
            {"payload": '{"title":"missing required fields"}', "id": str(material.material_id)},
        )

    with pytest.raises(ValidationError):
        repository.get(material.material_id)
