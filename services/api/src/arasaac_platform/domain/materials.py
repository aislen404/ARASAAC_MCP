from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)

from arasaac_platform.governance.license import ARASAAC_ATTRIBUTION_ES


class MaterialType(StrEnum):
    VISUAL_AGENDA = "visual_agenda"
    COMMUNICATION_BOARD = "communication_board"
    ACCESSIBLE_DOCUMENT = "accessible_document"
    SOCIAL_STORY = "social_story"
    SIGNAGE = "signage"  # Señalética: sin logo ARASAAC; validación en gobernanza.


class MaterialStatus(StrEnum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReviewOutcome(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"


class AuditAction(StrEnum):
    CREATED = "created"
    UPDATED = "updated"
    SUBMITTED = "submitted"
    REVIEWED = "reviewed"
    EXPORTED = "exported"
    AI_PLAN_REQUESTED = "ai_plan_requested"
    AI_PLAN_REJECTED_PRIVACY = "ai_plan_rejected_privacy"


class PictogramReference(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    pictogram_id: int = Field(gt=0)
    label: str = Field(min_length=1, max_length=120)
    source_url: HttpUrl
    origin: Literal["ARASAAC"] = "ARASAAC"
    author: Literal["Sergio Palao"] = "Sergio Palao"
    owner: Literal["Gobierno de Aragón"] = "Gobierno de Aragón"
    license: Literal["CC BY-NC-SA"] = "CC BY-NC-SA"
    retrieved_at: datetime

    @field_validator("source_url")
    @classmethod
    def require_arasaac_host(cls, value: HttpUrl) -> HttpUrl:
        host = value.host or ""
        if host != "arasaac.org" and not host.endswith(".arasaac.org"):
            raise ValueError("source_url debe pertenecer a arasaac.org")
        return value

    @field_validator("retrieved_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("retrieved_at debe incluir zona horaria")
        return value


class MaterialBlock(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    block_id: UUID = Field(default_factory=uuid4)
    position: int = Field(ge=0)
    text: str = Field(min_length=1, max_length=240)
    pictogram: PictogramReference | None = None


class ReviewDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    outcome: ReviewOutcome
    human_confirmed: Literal[True]
    note: str = Field(min_length=1, max_length=500)
    decided_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    event_id: UUID = Field(default_factory=uuid4)
    material_id: UUID
    action: AuditAction
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correlation_id: UUID = Field(default_factory=uuid4)
    detail: str = Field(min_length=1, max_length=500)


class Material(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    material_id: UUID = Field(default_factory=uuid4)
    material_type: MaterialType
    title: str = Field(min_length=1, max_length=120)
    version: int = Field(default=1, ge=1)
    status: MaterialStatus = MaterialStatus.DRAFT
    blocks: list[MaterialBlock] = Field(default_factory=list, max_length=64)
    attribution_text: str = ARASAAC_ATTRIBUTION_ES
    attribution_visible: bool = True
    arasaac_logo_included: bool = False
    commercial_use: Literal[False] = False
    review: ReviewDecision | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def require_review_for_final_state(self) -> "Material":
        if self.status == MaterialStatus.APPROVED:
            if self.review is None or self.review.outcome != ReviewOutcome.APPROVED:
                raise ValueError("Un material aprobado requiere decisión humana aprobada.")
        if self.status == MaterialStatus.REJECTED:
            if self.review is None or self.review.outcome != ReviewOutcome.REJECTED:
                raise ValueError("Un material rechazado requiere decisión humana rechazada.")
        return self

    @property
    def pictograms(self) -> list[PictogramReference]:
        return [block.pictogram for block in self.blocks if block.pictogram is not None]
