import sys

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from safe_mcp.server import ALLOWED_TOOLS, mcp


@pytest.mark.anyio
async def test_tool_allowlist_and_schemas_are_explicit() -> None:
    tools = await mcp.list_tools()

    assert {tool.name for tool in tools} == ALLOWED_TOOLS
    for tool in tools:
        assert tool.outputSchema is not None
        request_schema = tool.inputSchema["$defs"]
        strict_models = [
            definition
            for definition in request_schema.values()
            if definition.get("type") == "object"
        ]
        assert strict_models
        assert all(
            definition.get("additionalProperties") is False
            for definition in strict_models
        )


@pytest.mark.anyio
async def test_governance_resources_are_registered() -> None:
    resources = await mcp.list_resources()

    uris = {str(resource.uri) for resource in resources}
    assert uris == {"arasaac://guardrails", "arasaac://license"}

    license_contents = await mcp.read_resource("arasaac://license")
    assert "Sergio Palao" in str(license_contents)
    assert "Creative Commons BY-NC-SA" in str(license_contents)


@pytest.mark.anyio
async def test_stdio_protocol_initializes_and_lists_allowlist() -> None:
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "safe_mcp.server"],
    )

    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()

    assert {tool.name for tool in tools.tools} == ALLOWED_TOOLS
