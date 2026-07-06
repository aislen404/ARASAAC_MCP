# MCP — arquitectura dual HTTP / stdio

## Superficies

| Superficie | Puerto / transporte | Función |
|------------|---------------------|---------|
| HTTP status | `:8001` (Docker `mcp`) | `GET /health`, `GET /mcp/status` — allowlist informativa |
| MCP stdio | `arasaac-mcp` / `make mcp-stdio` | Protocolo MCP real con tools ejecutables |

Los clientes IDE (Cursor, Claude Code, Codex) deben usar **stdio**. El contenedor Docker no expone stdio; documenta `make mcp-stdio` para integración local.

## Tools allowlisted

- `search_pictograms`
- `get_pictogram`
- `suggest_pictograms_for_text`

## Evolución futura

Cualquier tool de materiales o exportación requiere: schema estricto (`additionalProperties: false`), tests de contrato, revisión de seguridad y OpenSpec aprobada según `AGENTS.md`.
