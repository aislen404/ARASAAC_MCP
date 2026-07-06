from pydantic import BaseModel, ConfigDict, Field, field_validator

from arasaac_platform.domain.materials import MaterialType


class EntityTemplateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3, max_length=80)
    default_material_type: MaterialType = MaterialType.VISUAL_AGENDA
    locale: str = Field(default="es", pattern=r"^[a-z]{2}$")
    visual_density: str = Field(default="medium", pattern=r"^(low|medium|high)$")

    @field_validator("name")
    @classmethod
    def reject_personal_patterns(cls, value: str) -> str:
        lowered = value.lower()
        if "@" in lowered or any(token in lowered for token in ("dni", "teléfono", "telefono")):
            raise ValueError("La plantilla no puede contener datos personales.")
        return value


class EntityTemplate(EntityTemplateInput):
    model_config = ConfigDict(extra="forbid", frozen=True)

    template_id: str


class EntityTemplateList(BaseModel):
    model_config = ConfigDict(extra="forbid")

    templates: list[EntityTemplate]
