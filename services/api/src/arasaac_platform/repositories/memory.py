from __future__ import annotations

from threading import RLock
from uuid import UUID

from arasaac_platform.domain.materials import AuditEvent, Material
from arasaac_platform.domain.workspaces import Workspace


class MaterialNotFound(KeyError):
    """Raised when a material does not exist."""


class WorkspaceNotFound(KeyError):
    """Raised when a workspace does not exist."""


class InMemoryRepository:
    def __init__(self) -> None:
        self._workspaces: dict[UUID, Workspace] = {}
        self._workspaces_by_slug: dict[str, UUID] = {}
        self._materials: dict[UUID, Material] = {}
        self._events: tuple[AuditEvent, ...] = ()
        self._lock = RLock()

    def ping(self) -> None:
        return None

    def save_workspace(self, workspace: Workspace) -> Workspace:
        with self._lock:
            self._workspaces[workspace.workspace_id] = workspace
            self._workspaces_by_slug[workspace.slug] = workspace.workspace_id
        return workspace

    def get_workspace_by_slug(self, slug: str) -> Workspace:
        with self._lock:
            workspace_id = self._workspaces_by_slug.get(slug)
            if workspace_id is None:
                raise WorkspaceNotFound(slug)
            return self._workspaces[workspace_id]

    def workspace_slug_exists(self, slug: str) -> bool:
        with self._lock:
            return slug in self._workspaces_by_slug

    def save(self, material: Material) -> Material:
        with self._lock:
            self._materials[material.material_id] = material
        return material

    def get(self, material_id: UUID) -> Material:
        with self._lock:
            try:
                return self._materials[material_id]
            except KeyError as exc:
                raise MaterialNotFound(str(material_id)) from exc

    def list_materials(
        self,
        *,
        workspace_id: UUID | None = None,
        statuses: tuple[str, ...] | None = None,
        query: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Material], int]:
        with self._lock:
            materials = sorted(self._materials.values(), key=lambda item: item.created_at)
            if workspace_id is not None:
                materials = [item for item in materials if item.workspace_id == workspace_id]
            if statuses is not None:
                materials = [item for item in materials if item.status in statuses]
            if query:
                lowered = query.lower()
                materials = [item for item in materials if lowered in item.title.lower()]
            total = len(materials)
            return materials[offset : offset + limit], total

    def append_event(self, event: AuditEvent) -> None:
        with self._lock:
            self._events = (*self._events, event)

    def events_for(self, material_id: UUID, *, workspace_id: UUID | None = None) -> list[AuditEvent]:
        with self._lock:
            events = [event for event in self._events if event.material_id == material_id]
            if workspace_id is not None:
                events = [event for event in events if event.workspace_id == workspace_id]
            return events

    def clear(self) -> None:
        with self._lock:
            self._workspaces.clear()
            self._workspaces_by_slug.clear()
            self._materials.clear()
            self._events = ()
