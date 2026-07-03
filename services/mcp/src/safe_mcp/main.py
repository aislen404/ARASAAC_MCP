from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class McpStatusResponse(BaseModel):
    status: Literal["placeholder"]
    enabled: Literal[False]
    tools: list[str]


app = FastAPI(
    title="Safe MCP Placeholder",
    description="No MCP tools, command execution, filesystem access, or network connectors.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="mcp-placeholder")


@app.get("/mcp/status", response_model=McpStatusResponse, tags=["system"])
def mcp_status() -> McpStatusResponse:
    return McpStatusResponse(status="placeholder", enabled=False, tools=[])
