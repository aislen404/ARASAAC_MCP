from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Severity(StrEnum):
    BLOCKER = "blocker"
    WARNING = "warning"
    OK = "ok"


class ValidationFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    validator_id: str = Field(min_length=1, max_length=80)
    severity: Severity
    title: str = Field(min_length=1, max_length=160)
    detail: str = Field(min_length=1, max_length=500)
    subject: Literal["material", "item", "pictogram"] = "material"
    subject_ref: str | None = Field(default=None, max_length=120)


class ValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    material_id: str
    material_version: int = Field(ge=1)
    validators_run: list[str] = Field(default_factory=list)
    findings: list[ValidationFinding] = Field(default_factory=list)
    generated_at: datetime
    is_blocking: bool