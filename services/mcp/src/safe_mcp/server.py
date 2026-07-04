from mcp.server.fastmcp import FastMCP

from arasaac_platform.arasaac.client import ArasaacClient
from arasaac_platform.domain.materials import PictogramReference
from arasaac_platform.governance.license import ARASAAC_ATTRIBUTION_ES
from arasaac_platform.schemas.pictograms import (
    GetPictogramInput,
    PictogramSearchResult,
    PictogramSuggestionsResult,
    SearchPictogramsInput,
    SuggestPictogramsInput,
)
from arasaac_platform.services.pictograms import (
    get_pictogram as get_pictogram_service,
)
from arasaac_platform.services.pictograms import (
    search_pictograms as search_pictograms_service,
)
from arasaac_platform.services.pictograms import (
    suggest_pictograms as suggest_pictograms_service,
)


ALLOWED_TOOLS = frozenset(
    {
        "search_pictograms",
        "get_pictogram",
        "suggest_pictograms_for_text",
    }
)

GUARDRAILS = """\
- Solo pictogramas reales recuperados de ARASAAC.
- No generar, imitar ni modificar pictogramas.
- No usar datos personales ni realizar diagnóstico.
- Toda selección requiere revisión humana.
- No exportar sin aprobación humana.
- No ejecutar shell ni acceder a filesystem arbitrario.
"""

mcp = FastMCP(
    "ARASAAC Social MCP",
    instructions=(
        "Servidor social no comercial. Devuelve candidatos ARASAAC reales; "
        "la selección y cualquier material requieren revisión humana."
    ),
    json_response=True,
)


@mcp.resource("arasaac://license")
def license_resource() -> str:
    """Return the mandatory ARASAAC attribution and license policy."""
    return ARASAAC_ATTRIBUTION_ES


@mcp.resource("arasaac://guardrails")
def guardrails_resource() -> str:
    """Return non-negotiable safety and compliance constraints."""
    return GUARDRAILS


@mcp.tool()
async def search_pictograms(
    request: SearchPictogramsInput,
) -> PictogramSearchResult:
    """Search real ARASAAC pictograms; candidates require human selection."""
    return await search_pictograms_service(request, ArasaacClient())


@mcp.tool()
async def get_pictogram(request: GetPictogramInput) -> PictogramReference:
    """Get one real ARASAAC pictogram reference by official ID."""
    return await get_pictogram_service(request, ArasaacClient())


@mcp.tool()
async def suggest_pictograms_for_text(
    request: SuggestPictogramsInput,
) -> PictogramSuggestionsResult:
    """Deterministically search candidates per text term without generative AI."""
    return await suggest_pictograms_service(request, ArasaacClient())


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
