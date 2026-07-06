from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from arasaac_platform.domain.materials import (
    AuditEvent,
    Material,
    PictogramReference,
    ReviewOutcome,
)


class MaterialItemInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=240)
    pictogram: PictogramReference


class CreateAgendaInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)
    steps: list[MaterialItemInput] = Field(min_length=1, max_length=20)


class CreateBoardInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)
    cells: list[MaterialItemInput] = Field(min_length=2, max_length=24)


class CreateDocumentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)
    sections: list[MaterialItemInput] = Field(min_length=1, max_length=20)


class CreateStoryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)
    scenes: list[MaterialItemInput] = Field(min_length=1, max_length=16)


class CreateSignageInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=120)
    signs: list[MaterialItemInput] = Field(min_length=2, max_length=12)


class ReviewMaterialInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    outcome: ReviewOutcome
    human_confirmed: Literal[True]
    note: str = Field(min_length=1, max_length=500)


class MaterialResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    material: Material


class MaterialListResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    materials: list[Material]


class AuditEventsResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    events: list[AuditEvent]


class ExportManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    material_id: str
    version: int
    license: Literal["CC BY-NC-SA"] = "CC BY-NC-SA"
    attribution: str
    pictograms: list[PictogramReference]
    human_review_approved: Literal[True]


class ExportResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filename: str
    media_type: str
    content_base64: str
    manifest: ExportManifest
