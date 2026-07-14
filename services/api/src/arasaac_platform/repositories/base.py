from typing import Protocol
from uuid import UUID

from arasaac_platform.domain.materials import AuditEvent, Material
from arasaac_platform.domain.workspaces import Workspace


class Repository(Protocol):
    def ping(self) -> None: ...

    def save_workspace(self, workspace: Workspace) -> Workspace: ...

    def get_workspace_by_slug(self, slug: str) -> Workspace: ...

    def workspace_slug_exists(self, slug: str) -> bool: ...

    def save(self, material: Material) -> Material: ...

    def get(self, material_id: UUID) -> Material: ...

    def list_materials(
        self,
        *,
        workspace_id: UUID | None = None,
        statuses: tuple[str, ...] | None = None,
        query: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Material], int]: ...

    def append_event(self, event: AuditEvent) -> None: ...

    def events_for(self, material_id: UUID, *, workspace_id: UUID | None = None) -> list[AuditEvent]: ...

    def clear(self) -> None: ...
