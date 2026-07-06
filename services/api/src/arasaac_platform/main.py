import json
import logging
import os

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from arasaac_platform.api.ai import router as ai_router
from arasaac_platform.api.materials import router as materials_router
from arasaac_platform.api.pictograms import router as pictograms_router
from arasaac_platform.api.preferences import router as preferences_router
from arasaac_platform.observability.metrics import export_counter, mcp_tool_counter, review_counter
from arasaac_platform.observability.middleware import RateLimitMiddleware, RequestLoggingMiddleware

logging.basicConfig(level=logging.INFO, format="%(message)s")


class HealthResponse(BaseModel):
    status: str
    service: str


def _cors_origins() -> list[str]:
    raw = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    )
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="ARASAAC Social MCP Platform API",
    description=(
        "API gobernada para materiales con pictogramas reales ARASAAC y "
        "planificación IA opcional."
    ),
    version="0.3.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Request-ID"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(pictograms_router)
app.include_router(materials_router)
app.include_router(preferences_router)
app.include_router(ai_router)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="api")


@app.get("/metrics", tags=["system"])
def metrics() -> Response:
    payload = {
        "exports": dict(export_counter),
        "reviews": dict(review_counter),
        "mcp_tools": dict(mcp_tool_counter),
    }
    return Response(content=json.dumps(payload), media_type="application/json")
