from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field


ARASAAC_ATTRIBUTION_ES = (
    "Los símbolos pictográficos utilizados son propiedad del Gobierno de Aragón "
    "y han sido creados por Sergio Palao para ARASAAC (https://arasaac.org), "
    "que los distribuye bajo licencia Creative Commons BY-NC-SA."
)


class PictogramUsage(Protocol):
    origin: str
    author: str
    owner: str
    license: str


class MaterialForCompliance(Protocol):
    material_type: str
    pictograms: list[PictogramUsage]
    attribution_visible: bool
    arasaac_logo_included: bool
    commercial_use: bool


class AttributionNotice(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    text: str = ARASAAC_ATTRIBUTION_ES
    license: str = "CC BY-NC-SA"
    commercial_use: bool = False
    share_alike_required: bool = True


class ComplianceResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    valid: bool
    errors: list[str] = Field(default_factory=list)


def validate_material_license(material: MaterialForCompliance) -> ComplianceResult:
    errors: list[str] = []

    if material.commercial_use:
        errors.append("El uso comercial está prohibido en el MVP.")
    if material.pictograms and not material.attribution_visible:
        errors.append("La atribución ARASAAC debe ser visible.")
    if material.material_type == "signage" and not material.arasaac_logo_included:
        errors.append("La señalética debe incluir el logotipo ARASAAC.")

    for pictogram in material.pictograms:
        if pictogram.origin != "ARASAAC":
            errors.append("El origen del pictograma debe ser ARASAAC.")
        if pictogram.author != "Sergio Palao":
            errors.append("El autor del pictograma debe ser Sergio Palao.")
        if pictogram.owner != "Gobierno de Aragón":
            errors.append("El propietario debe ser Gobierno de Aragón.")
        if pictogram.license != "CC BY-NC-SA":
            errors.append("La licencia debe ser CC BY-NC-SA.")

    return ComplianceResult(valid=not errors, errors=errors)
