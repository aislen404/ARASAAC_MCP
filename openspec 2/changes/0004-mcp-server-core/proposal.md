# Proposal — 0004-mcp-server-core

## Problema

Servidor MCP core es necesario para cumplir el Plan Maestro y permitir una evolución trazable mediante OpenSpec y Codex.

## Solución propuesta

Exponer servidor MCP local con tools/resources/prompts, schemas estrictos y allowlist.

## Alcance

- Implementar la capacidad descrita.
- Añadir pruebas y documentación.
- Respetar licencia ARASAAC, revisión humana y no PII cuando aplique.

## Fuera de alcance

No shell execution; no tools no aprobadas.

## Riesgos

- Incumplimiento de licencia.
- Falta de trazabilidad.
- Complejidad excesiva.
- Pérdida de accesibilidad.

## Métrica de éxito

Cliente MCP puede listar tools/resources/prompts y ejecutar health/tool básica.
