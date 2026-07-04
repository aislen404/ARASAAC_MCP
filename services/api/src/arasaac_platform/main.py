from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from arasaac_platform.api.pictograms import router as pictograms_router
from arasaac_platform.api.materials import router as materials_router


class HealthResponse(BaseModel):
    status: str
    service: str


app = FastAPI(
    title="ARASAAC Social MCP Platform API",
    description="MVP-0 foundation API; no ARASAAC integration or material processing.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.include_router(pictograms_router)
app.include_router(materials_router)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="api")
