from pydantic import BaseModel, ConfigDict, Field

from arasaac_platform.domain.materials import PictogramReference


class SearchPictogramsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1, max_length=120)
    locale: str = Field(default="es", pattern="^(es|en|fr|de|it|pt)$")
    limit: int = Field(default=12, ge=1, le=50)


class GetPictogramInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pictogram_id: int = Field(gt=0)
    locale: str = Field(default="es", pattern="^(es|en|fr|de|it|pt)$")


class SuggestPictogramsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=240)
    locale: str = Field(default="es", pattern="^(es|en|fr|de|it|pt)$")
    max_terms: int = Field(default=8, ge=1, le=12)
    results_per_term: int = Field(default=3, ge=1, le=5)


class PictogramSearchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    locale: str
    candidates: list[PictogramReference]
    requires_human_selection: bool = True


class PictogramSuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    term: str
    candidates: list[PictogramReference]


class PictogramSuggestionsResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suggestions: list[PictogramSuggestion]
    requires_human_selection: bool = True
