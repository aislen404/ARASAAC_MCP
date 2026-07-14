import re
from random import Random

from arasaac_platform.domain.slug_generator import generate_workspace_slug


def test_generate_workspace_slug_format_and_retry() -> None:
    existing = {"zorro-alegre-piedra"}
    rng = Random(1)

    slug = generate_workspace_slug(existing.__contains__, rng=rng)

    assert re.fullmatch(r"^[a-z]+(-[a-z]+){2,4}$", slug)
    assert slug != "zorro-alegre-piedra"


def test_slug_dictionaries_do_not_include_pii_terms() -> None:
    slug = generate_workspace_slug(lambda _: False, rng=Random(2))
    assert "juan" not in slug
    assert "maria" not in slug