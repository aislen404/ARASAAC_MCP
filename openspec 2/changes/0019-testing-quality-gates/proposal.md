# Proposal — 0019-testing-quality-gates

## Problema

Quality gates y testing es necesario para cumplir el Plan Maestro y permitir una evolución trazable mediante OpenSpec y Codex.

## Solución propuesta

Configurar unit/integration/contract/E2E/accessibility/license tests.

## Alcance

- Implementar la capacidad descrita.
- Añadir pruebas y documentación.
- Respetar licencia ARASAAC, revisión humana y no PII cuando aplique.

## Fuera de alcance

No permite merges sin gates mínimos.

## Riesgos

- Incumplimiento de licencia.
- Falta de trazabilidad.
- Complejidad excesiva.
- Pérdida de accesibilidad.

## Métrica de éxito

CI ejecuta pruebas críticas y reporta fallos.
