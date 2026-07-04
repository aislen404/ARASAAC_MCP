from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from arasaac_platform.domain.materials import PictogramReference


class AIPlanInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    material_type: Literal["visual_agenda", "communication_board"]
    objective: str = Field(min_length=10, max_length=500)
    item_count: int = Field(default=6, ge=1, le=12)
    locale: Literal["es", "en", "fr", "de", "it", "pt"] = "es"
    no_personal_data_confirmed: Literal[True]

    @model_validator(mode="after")
    def board_requires_two_items(self) -> "AIPlanInput":
        if self.material_type == "communication_board" and self.item_count < 2:
            raise ValueError("Un tablero requiere al menos dos elementos.")
        return self


class AIPlannedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=120)
    search_term: str = Field(min_length=1, max_length=60)


class AITextPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str = Field(min_length=1, max_length=240)
    items: list[AIPlannedItem] = Field(min_length=1, max_length=12)


class AIResolvedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    search_term: str
    candidates: list[PictogramReference]


class AIPlanResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    items: list[AIResolvedItem]
    provider: str
    model: str
    requires_human_selection: Literal[True] = True
    creates_material: Literal[False] = False
    stores_input: Literal[False] = False
    warning: str = (
        "Propuesta de IA no vinculante. Revisa el texto y selecciona manualmente "
        "cada pictograma real de ARASAAC."
    )


class AIStatusResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    available: bool
    provider: str
    model: str | None
    reason: str | None
    generates_pictograms: Literal[False] = False
    requires_human_selection: Literal[True] = True
    stores_input: Literal[False] = False
