from __future__ import annotations

import inspect
import re
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from arasaac_platform.arasaac.client import ArasaacClient, ArasaacConnectorError
from arasaac_platform.domain.materials import Material, MaterialType
from arasaac_platform.schemas.validation import Severity, ValidationFinding, ValidationReport

ValidatorResult = Iterable[ValidationFinding] | Awaitable[Iterable[ValidationFinding]]
Validator = Callable[[Material, "ValidationContext"], ValidatorResult]

EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", re.UNICODE)
PHONE_RE = re.compile(r"\b(?:\+34|0034)?[\s-]?(?:6|7|8|9)\d(?:[\s-]?\d){7}\b")
DNI_RE = re.compile(r"\b\d{8}[A-HJ-NP-TV-Z]\b|\b[XYZ]\d{7}[A-HJ-NP-TV-Z]\b", re.IGNORECASE)
ADDRESS_RE = re.compile(r"\b(?:c/|calle|avda\.?|avenida|plaza)\s+[^,.;:]{3,}\b", re.IGNORECASE)
PROPER_NAME_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b")

OFFICIAL_ARASAAC_STATIC_PREFIX = "https://static.arasaac.org/pictograms/"

TYPE_LIMITS: dict[MaterialType, tuple[int, int]] = {
    MaterialType.VISUAL_AGENDA: (1, 12),
    MaterialType.COMMUNICATION_BOARD: (2, 24),
    MaterialType.ACCESSIBLE_DOCUMENT: (1, 20),
    MaterialType.SOCIAL_STORY: (1, 16),
    MaterialType.SIGNAGE: (2, 12),
}


@dataclass(frozen=True)
class ValidationContext:
    arasaac_client: ArasaacClient | None = None
    allow_online_lookup: bool = False
    online_lookup_timeout_seconds: float = 3.0


def default_validators() -> tuple[Validator, ...]:
    return (
        validate_pictogram_ids_real,
        validate_license_notice_visible,
        validate_no_personal_data,
        validate_no_modified_pictograms,
        validate_non_commercial_context,
        validate_visual_density,
    )


async def run_validators(
    material: Material,
    ctx: ValidationContext,
    validators: Iterable[Validator] | None = None,
) -> ValidationReport:
    selected_validators = tuple(validators or default_validators())
    findings: list[ValidationFinding] = []
    for validator in selected_validators:
        result = validator(material, ctx)
        if inspect.isawaitable(result):
            findings.extend(await result)
            continue
        findings.extend(result)

    return ValidationReport(
        material_id=str(material.material_id),
        material_version=material.version,
        validators_run=[validator.__name__.removeprefix("validate_") for validator in selected_validators],
        findings=findings,
        generated_at=datetime.now(UTC),
        is_blocking=any(finding.severity == Severity.BLOCKER for finding in findings),
    )


def validate_license_notice_visible(
    material: Material,
    ctx: ValidationContext,
) -> Iterable[ValidationFinding]:
    del ctx
    required_terms = ("Sergio Palao", "ARASAAC", "Gobierno de Aragón", "CC BY-NC-SA")
    if all(term in material.attribution_text for term in required_terms):
        return [_ok_finding("license_notice_visible", "Atribución visible", "La atribución obligatoria ARASAAC está presente.")]
    return [
        ValidationFinding(
            validator_id="license_notice_visible",
            severity=Severity.BLOCKER,
            title="Falta atribución obligatoria",
            detail="El material debe mostrar la atribución completa a Sergio Palao, ARASAAC, Gobierno de Aragón y CC BY-NC-SA.",
        )
    ]


def validate_no_personal_data(
    material: Material,
    ctx: ValidationContext,
) -> Iterable[ValidationFinding]:
    del ctx
    findings: list[ValidationFinding] = []
    proper_name_warning_emitted = False
    for block in material.blocks:
        text = block.text
        if EMAIL_RE.search(text):
            findings.append(_pii_finding("Se detectó un correo electrónico en un texto del material.", block.block_id, Severity.BLOCKER))
        if PHONE_RE.search(text):
            findings.append(_pii_finding("Se detectó un teléfono en un texto del material.", block.block_id, Severity.BLOCKER))
        if DNI_RE.search(text):
            findings.append(_pii_finding("Se detectó un identificador nacional en un texto del material.", block.block_id, Severity.BLOCKER))
        if ADDRESS_RE.search(text):
            findings.append(_pii_finding("Se detectó una dirección postal en un texto del material.", block.block_id, Severity.WARNING))
        if PROPER_NAME_RE.search(text) and not proper_name_warning_emitted:
            findings.append(_pii_finding("Se ha detectado un posible nombre propio; revisa que el material siga siendo genérico.", block.block_id, Severity.WARNING))
            proper_name_warning_emitted = True

    if findings:
        return findings
    return [_ok_finding("no_personal_data", "Sin datos personales", "No se detectaron patrones de datos personales en los textos del material.")]


def validate_no_modified_pictograms(
    material: Material,
    ctx: ValidationContext,
) -> Iterable[ValidationFinding]:
    del ctx
    findings: list[ValidationFinding] = []
    for pictogram in material.pictograms:
        source_url = str(pictogram.source_url)
        expected_prefix = f"{OFFICIAL_ARASAAC_STATIC_PREFIX}{pictogram.pictogram_id}/"
        if not source_url.startswith(expected_prefix) or "?" in source_url:
            findings.append(
                ValidationFinding(
                    validator_id="no_modified_pictograms",
                    severity=Severity.BLOCKER,
                    title="Pictograma con origen no válido",
                    detail="Cada pictograma debe mantener la URL oficial ARASAAC sin parámetros de transformación.",
                    subject="pictogram",
                    subject_ref=str(pictogram.pictogram_id),
                )
            )
    if findings:
        return findings
    return [_ok_finding("no_modified_pictograms", "Pictogramas oficiales intactos", "Las referencias de pictogramas mantienen la URL oficial sin transformaciones.")]


def validate_non_commercial_context(
    material: Material,
    ctx: ValidationContext,
) -> Iterable[ValidationFinding]:
    del ctx
    if material.usage_context == "non_commercial" and material.commercial_use is False:
        return [_ok_finding("non_commercial_context", "Contexto no comercial confirmado", "El material mantiene el contexto no comercial exigido por el proyecto.")]
    return [
        ValidationFinding(
            validator_id="non_commercial_context",
            severity=Severity.BLOCKER,
            title="Contexto de uso no permitido",
            detail="El material debe declararse explícitamente como de uso no comercial.",
        )
    ]


def validate_visual_density(
    material: Material,
    ctx: ValidationContext,
) -> Iterable[ValidationFinding]:
    del ctx
    minimum, maximum = TYPE_LIMITS[material.material_type]
    total_blocks = len(material.blocks)
    if total_blocks < minimum:
        return [
            ValidationFinding(
                validator_id="visual_density",
                severity=Severity.WARNING,
                title="Densidad visual insuficiente",
                detail="El material tiene menos elementos de los recomendados para su tipo.",
            )
        ]
    if total_blocks >= max(minimum, int(maximum * 0.8)):
        return [
            ValidationFinding(
                validator_id="visual_density",
                severity=Severity.WARNING,
                title="Densidad visual alta",
                detail="El material está cerca del límite recomendado de elementos; revisa si conviene simplificarlo.",
            )
        ]
    return [_ok_finding("visual_density", "Densidad visual adecuada", "El número de elementos está dentro del rango recomendado para este tipo de material.")]


async def validate_pictogram_ids_real(
    material: Material,
    ctx: ValidationContext,
) -> Iterable[ValidationFinding]:
    if not material.pictograms:
        return [_ok_finding("pictogram_ids_real", "Sin pictogramas que validar", "El material no contiene pictogramas y no requiere validación de IDs.")]

    if not ctx.allow_online_lookup or ctx.arasaac_client is None:
        return [
            ValidationFinding(
                validator_id="pictogram_ids_real",
                severity=Severity.WARNING,
                title="Verificación degradada de IDs",
                detail="No hay un catálogo local activo ni verificación online habilitada; los IDs no se pudieron contrastar automáticamente.",
            )
        ]

    findings: list[ValidationFinding] = []
    for pictogram in material.pictograms:
        try:
            remote = await ctx.arasaac_client.get(pictogram.pictogram_id)
        except ArasaacConnectorError:
            findings.append(
                ValidationFinding(
                    validator_id="pictogram_ids_real",
                    severity=Severity.WARNING,
                    title="Verificación degradada de IDs",
                    detail="No se pudo verificar un pictograma contra la API oficial dentro del tiempo permitido.",
                    subject="pictogram",
                    subject_ref=str(pictogram.pictogram_id),
                )
            )
            continue
        if remote.pictogram_id != pictogram.pictogram_id:
            findings.append(
                ValidationFinding(
                    validator_id="pictogram_ids_real",
                    severity=Severity.BLOCKER,
                    title="ID de pictograma no válido",
                    detail="Se ha encontrado una referencia de pictograma que no coincide con un identificador ARASAAC válido.",
                    subject="pictogram",
                    subject_ref=str(pictogram.pictogram_id),
                )
            )

    if findings:
        return findings
    return [_ok_finding("pictogram_ids_real", "IDs de pictogramas verificados", "Todos los pictogramas del material se han validado contra ARASAAC.")]


def validation_summary_counts(report: ValidationReport) -> dict[str, int]:
    return {
        "blocker": sum(1 for finding in report.findings if finding.severity == Severity.BLOCKER),
        "warning": sum(1 for finding in report.findings if finding.severity == Severity.WARNING),
        "ok": sum(1 for finding in report.findings if finding.severity == Severity.OK),
    }


def _ok_finding(validator_id: str, title: str, detail: str) -> ValidationFinding:
    return ValidationFinding(
        validator_id=validator_id,
        severity=Severity.OK,
        title=title,
        detail=detail,
    )


def _pii_finding(detail: str, block_id: UUID, severity: Severity) -> ValidationFinding:
    return ValidationFinding(
        validator_id="no_personal_data",
        severity=severity,
        title="Posible dato personal detectado",
        detail=detail,
        subject="item",
        subject_ref=str(block_id),
    )