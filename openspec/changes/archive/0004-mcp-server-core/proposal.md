# Proposal — 0004-mcp-server-core

## Objetivo

Sustituir el placeholder por un servidor MCP local basado en el SDK oficial,
manteniendo allowlist explícita, schemas estrictos y ausencia de ejecución
arbitraria.

## Alcance

Transporte stdio para desarrollo, resources de licencia/guardrails y registro
explícito de tools aprobadas. Sin shell, filesystem genérico ni URLs arbitrarias.
