from __future__ import annotations

from threading import RLock
from uuid import UUID

from arasaac_platform.domain.materials import AuditEvent, Material


class MaterialNotFound(KeyError):
    """Raised when a material does not exist."""


class InMemoryRepository:
    def __init__(self) -> None:
        self._materials: dict[UUID, Material] = {}
        self._events: tuple[AuditEvent, ...] = ()
        self._lock = RLock()

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

    def list_materials(self) -> list[Material]:
        with self._lock:
            return sorted(self._materials.values(), key=lambda item: item.created_at)

    def append_event(self, event: AuditEvent) -> None:
        with self._lock:
            self._events = (*self._events, event)

    def events_for(self, material_id: UUID) -> list[AuditEvent]:
        with self._lock:
            return [event for event in self._events if event.material_id == material_id]

    def clear(self) -> None:
        with self._lock:
            self._materials.clear()
            self._events = ()
