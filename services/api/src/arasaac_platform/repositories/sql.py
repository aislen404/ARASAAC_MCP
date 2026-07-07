from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, String, create_engine, delete, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from arasaac_platform.domain.materials import AuditEvent, Material
from arasaac_platform.repositories.memory import MaterialNotFound


class Base(DeclarativeBase):
    pass


class MaterialRow(Base):
    __tablename__ = "materials"

    material_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSON)


class AuditRow(Base):
    __tablename__ = "audit_events"

    event_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    material_id: Mapped[str] = mapped_column(String(36), index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSON)


class SqlRepository:
    def __init__(self, database_url: str) -> None:
        self._engine = create_engine(database_url, pool_pre_ping=True)
        if database_url.startswith("sqlite"):
            Base.metadata.create_all(self._engine)

    def save(self, material: Material) -> Material:
        row = MaterialRow(
            material_id=str(material.material_id),
            created_at=material.created_at,
            payload=material.model_dump(mode="json"),
        )
        with Session(self._engine) as session:
            session.merge(row)
            session.commit()
        return material

    def get(self, material_id: UUID) -> Material:
        with Session(self._engine) as session:
            row = session.get(MaterialRow, str(material_id))
            if row is None:
                raise MaterialNotFound(str(material_id))
            return Material.model_validate(row.payload)

    def list_materials(self) -> list[Material]:
        with Session(self._engine) as session:
            rows = session.scalars(
                select(MaterialRow).order_by(MaterialRow.created_at)
            ).all()
            return [Material.model_validate(row.payload) for row in rows]

    def append_event(self, event: AuditEvent) -> None:
        row = AuditRow(
            event_id=str(event.event_id),
            material_id=str(event.material_id),
            occurred_at=event.occurred_at,
            payload=event.model_dump(mode="json"),
        )
        with Session(self._engine) as session:
            session.add(row)
            session.commit()

    def events_for(self, material_id: UUID) -> list[AuditEvent]:
        with Session(self._engine) as session:
            rows = session.scalars(
                select(AuditRow)
                .where(AuditRow.material_id == str(material_id))
                .order_by(AuditRow.occurred_at)
            ).all()
            return [AuditEvent.model_validate(row.payload) for row in rows]

    def clear(self) -> None:
        with Session(self._engine) as session:
            session.execute(delete(AuditRow))
            session.execute(delete(MaterialRow))
            session.commit()
