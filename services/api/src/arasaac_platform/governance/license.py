from collections.abc import Sequence
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field

ARASAAC_ATTRIBUTION_ES = (
    "Los símbolos pictográficos utilizados son propiedad del Gobierno de Aragón "
    "y han sido creados por Sergio Palao para ARASAAC (https://arasaac.org), "
    "que los distribuye bajo licencia Creative Commons BY-NC-SA."
)


class PictogramUsage(Protocol):
    @property
    def origin(self) -> str: ...

    @property
    def author(self) -> str: ...

    @property
    def owner(self) -> str: ...

    @property
    def license(self) -> str: ...


class MaterialForCompliance(Protocol):
    @property
    def material_type(self) -> object: ...

    @property
    def pictograms(self) -> Sequence[PictogramUsage]: ...

    @property
    def attribution_visible(self) -> bool: ...

    @property
    def arasaac_logo_included(self) -> bool: ...

    @property
    def commercial_use(self) -> bool: ...


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
    if material.material_type == "signage" and material.arasaac_logo_included:
        errors.append("La señalética no debe incluir el logotipo ARASAAC embebido.")

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
