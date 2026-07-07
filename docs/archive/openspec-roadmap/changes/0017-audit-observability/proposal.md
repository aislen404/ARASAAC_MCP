# Proposal — 0017-audit-observability

## Problema

Auditoría y observabilidad es necesario para cumplir el Plan Maestro y permitir una evolución trazable mediante OpenSpec y Codex.

## Solución propuesta

Registrar generación, tool calls, pictogramas usados, exportaciones, errores y métricas.

## Alcance

- Implementar la capacidad descrita.
- Añadir pruebas y documentación.
- Respetar licencia ARASAAC, revisión humana y no PII cuando aplique.

## Fuera de alcance

No guarda prompts con PII; sanitiza datos.

## Riesgos

- Incumplimiento de licencia.
- Falta de trazabilidad.
- Complejidad excesiva.
- Pérdida de accesibilidad.

## Métrica de éxito

AuditEvent disponible para trazabilidad y métricas.
