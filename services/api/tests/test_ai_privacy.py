import pytest

from arasaac_platform.ai.privacy import PrivacyViolation, validate_generic_text


@pytest.mark.parametrize(
    "unsafe",
    [
        "Escribe a maria@example.org para preparar la agenda",
        "Llama al +34 612 345 678 para confirmar la actividad",
        "El DNI es 12345678Z y necesita una agenda",
        "Consulta https://example.org para preparar la visita",
        "Genera un diagnóstico de esta situación",
        "Incluye su historial médico en el tablero",
    ],
)
def test_privacy_guard_rejects_sensitive_or_diagnostic_content(unsafe: str) -> None:
    with pytest.raises(PrivacyViolation):
        validate_generic_text(unsafe)


def test_privacy_guard_normalizes_generic_scenario() -> None:
    assert (
        validate_generic_text("  Preparar   una visita genérica a la biblioteca  ")
        == "Preparar una visita genérica a la biblioteca"
    )


def test_privacy_guard_rejects_whitespace_only_text() -> None:
    with pytest.raises(PrivacyViolation, match="texto genérico"):
        validate_generic_text("   ")
