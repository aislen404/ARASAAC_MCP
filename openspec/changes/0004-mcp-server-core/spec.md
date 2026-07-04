# Spec — 0004-mcp-server-core

## Escenarios

- El cliente MCP inicializa por stdio y lista solo tools allowlisted.
- Cada tool tiene inputSchema cerrado y output estructurado.
- `arasaac://license` y `arasaac://guardrails` son legibles.
- Nombres de tool desconocidos se rechazan.
- No hay shell, acceso arbitrario a archivos ni conectores no aprobados.
