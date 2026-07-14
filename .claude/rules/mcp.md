<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: b98e843216a6 -->
# Reglas MCP

- Allowlist estricta de tools.
- Schema Pydantic en input/output; tests contractuales.
- Sin ejecución arbitraria, shell ni filesystem libre.
- Sin export sin validadores de licencia y revisión humana.
- Audit log en tool calls relevantes.

**Globs sugeridos:** `apps/mcp-server/**`, `packages/mcp-contracts/**`
