from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from safe_mcp.server import ALLOWED_TOOLS


class HealthResponse(BaseModel):
    status: str
    service: str


class McpStatusResponse(BaseModel):
    status: Literal["active"]
    enabled: Literal[True]
    tools: list[str]


app = FastAPI(
    title="Safe ARASAAC MCP Status",
    description="Status endpoint for the allowlisted ARASAAC MCP stdio server.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="mcp-server")


@app.get("/mcp/status", response_model=McpStatusResponse, tags=["system"])
def mcp_status() -> McpStatusResponse:
    return McpStatusResponse(
        status="active",
        enabled=True,
        tools=sorted(ALLOWED_TOOLS),
    )
