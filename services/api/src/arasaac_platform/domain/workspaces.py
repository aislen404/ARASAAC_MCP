from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Workspace(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    workspace_id: UUID = Field(default_factory=uuid4)
    slug: str = Field(pattern=r"^[a-z]+(?:-[a-z]+){2,4}$")
    display_name: str | None = Field(default=None, min_length=1, max_length=120)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class WorkspaceSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    workspace_id: UUID
    slug: str
    display_name: str | None = None