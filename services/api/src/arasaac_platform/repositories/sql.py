from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, String, create_engine, delete, func, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from arasaac_platform.domain.materials import AuditEvent, Material
from arasaac_platform.domain.workspaces import Workspace
from arasaac_platform.repositories.memory import MaterialNotFound, WorkspaceNotFound


class Base(DeclarativeBase):
    pass


class MaterialRow(Base):
    __tablename__ = "materials"

    material_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(String(36), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSON)


class WorkspaceRow(Base):
    __tablename__ = "workspaces"

    workspace_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    display_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSON)


class AuditRow(Base):
    __tablename__ = "audit_events"

    event_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(String(36), index=True)
    material_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict[str, object]] = mapped_column(JSON)


class SqlRepository:
    def __init__(self, database_url: str) -> None:
        self._engine = create_engine(database_url, pool_pre_ping=True)
        if database_url.startswith("sqlite"):
            Base.metadata.create_all(self._engine)

    def ping(self) -> None:
        with self._engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    def save_workspace(self, workspace: Workspace) -> Workspace:
        row = WorkspaceRow(
            workspace_id=str(workspace.workspace_id),
            slug=workspace.slug,
            display_name=workspace.display_name,
            created_at=workspace.created_at,
            updated_at=workspace.updated_at,
            payload=workspace.model_dump(mode="json"),
        )
        with Session(self._engine) as session:
            session.merge(row)
            session.commit()
        return workspace

    def get_workspace_by_slug(self, slug: str) -> Workspace:
        with Session(self._engine) as session:
            row = session.scalar(select(WorkspaceRow).where(WorkspaceRow.slug == slug))
            if row is None:
                raise WorkspaceNotFound(slug)
            return Workspace.model_validate(row.payload)

    def workspace_slug_exists(self, slug: str) -> bool:
        with Session(self._engine) as session:
            return session.scalar(select(WorkspaceRow.slug).where(WorkspaceRow.slug == slug)) is not None

    def save(self, material: Material) -> Material:
        row = MaterialRow(
            material_id=str(material.material_id),
            workspace_id=str(material.workspace_id),
            created_at=material.created_at,
            updated_at=material.updated_at,
            status=material.status,
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

    def list_materials(
        self,
        *,
        workspace_id: UUID | None = None,
        statuses: tuple[str, ...] | None = None,
        query: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Material], int]:
        with Session(self._engine) as session:
            statement = select(MaterialRow)
            if workspace_id is not None:
                statement = statement.where(MaterialRow.workspace_id == str(workspace_id))
            if statuses is not None:
                statement = statement.where(MaterialRow.status.in_(statuses))
            if query:
                statement = statement.where(func.lower(MaterialRow.payload["title"].as_string()).contains(query.lower()))
            total = session.scalar(select(func.count()).select_from(statement.subquery())) or 0
            rows = session.scalars(
                statement.order_by(MaterialRow.updated_at.desc(), MaterialRow.created_at.desc()).offset(offset).limit(limit)
            ).all()
            return [Material.model_validate(row.payload) for row in rows], total

    def append_event(self, event: AuditEvent) -> None:
        row = AuditRow(
            event_id=str(event.event_id),
            workspace_id=str(event.workspace_id),
            material_id=str(event.material_id) if event.material_id is not None else None,
            occurred_at=event.occurred_at,
            payload=event.model_dump(mode="json"),
        )
        with Session(self._engine) as session:
            session.add(row)
            session.commit()

    def events_for(self, material_id: UUID, *, workspace_id: UUID | None = None) -> list[AuditEvent]:
        with Session(self._engine) as session:
            statement = select(AuditRow).where(AuditRow.material_id == str(material_id))
            if workspace_id is not None:
                statement = statement.where(AuditRow.workspace_id == str(workspace_id))
            rows = session.scalars(statement.order_by(AuditRow.occurred_at)).all()
            return [AuditEvent.model_validate(row.payload) for row in rows]

    def clear(self) -> None:
        with Session(self._engine) as session:
            session.execute(delete(AuditRow))
            session.execute(delete(MaterialRow))
            session.execute(delete(WorkspaceRow))
            session.commit()
