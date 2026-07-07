import re


class PrivacyViolation(ValueError):
    """Raised before external processing when input appears unsafe."""


_PROHIBITED_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", re.IGNORECASE),
        "direcciones de correo",
    ),
    (
        re.compile(r"(?:\+?\d[\d .()-]{7,}\d)"),
        "números de teléfono o identificadores",
    ),
    (
        re.compile(r"\b(?:\d{8}[A-Z]|[XYZ]\d{7}[A-Z])\b", re.IGNORECASE),
        "documentos de identidad",
    ),
    (
        re.compile(r"https?://|www\.", re.IGNORECASE),
        "enlaces",
    ),
    (
        re.compile(
            r"\b(?:diagn[oó]stic(?:o|a|ar)|historial\s+m[eé]dic[oa]|"
            r"expediente\s+cl[ií]nico|medicaci[oó]n|prescripci[oó]n)\b",
            re.IGNORECASE,
        ),
        "información clínica o diagnóstica",
    ),
)


def validate_generic_text(value: str) -> str:
    normalized = " ".join(value.split())
    if not normalized:
        raise PrivacyViolation("El escenario debe contener texto genérico.")
    for pattern, description in _PROHIBITED_PATTERNS:
        if pattern.search(normalized):
            raise PrivacyViolation(
                f"El escenario no puede contener {description}. "
                "Usa una situación genérica y no personal."
            )
    return normalized
