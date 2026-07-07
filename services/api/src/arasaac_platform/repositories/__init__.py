"""Material and audit repositories."""

from arasaac_platform.repositories.base import Repository
from arasaac_platform.repositories.memory import InMemoryRepository
from arasaac_platform.repositories.sql import SqlRepository


def create_repository(database_url: str | None = None) -> Repository:
    if database_url:
        return SqlRepository(database_url)
    return InMemoryRepository()


__all__ = ["InMemoryRepository", "Repository", "SqlRepository", "create_repository"]
