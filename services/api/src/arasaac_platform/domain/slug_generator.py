from __future__ import annotations

from collections.abc import Callable
from random import Random

ANIMALS = (
    "zorro",
    "lince",
    "nutria",
    "garza",
    "tejon",
    "ciervo",
    "koala",
    "tortuga",
    "halcon",
    "delfin",
)

ADJECTIVES = (
    "alegre",
    "sereno",
    "claro",
    "amable",
    "ligero",
    "calmo",
    "firme",
    "suave",
    "noble",
    "vivo",
)

NATURE_NOUNS = (
    "piedra",
    "brisa",
    "bosque",
    "rio",
    "luna",
    "nube",
    "hoja",
    "mar",
    "valle",
    "sendero",
)


def generate_workspace_slug(
    exists: Callable[[str], bool],
    *,
    rng: Random | None = None,
    max_attempts: int = 32,
) -> str:
    generator = rng or Random()
    for _ in range(max_attempts):
        parts = [
            generator.choice(ANIMALS),
            generator.choice(ADJECTIVES),
            generator.choice(NATURE_NOUNS),
        ]
        if generator.random() < 0.35:
            parts.append(generator.choice(ADJECTIVES))
        slug = "-".join(parts)
        if not exists(slug):
            return slug
    raise RuntimeError("No se pudo generar un slug de workspace único.")