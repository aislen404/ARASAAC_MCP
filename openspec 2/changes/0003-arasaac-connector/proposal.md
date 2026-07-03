# Proposal — 0003-arasaac-connector

## Problema

Conector API ARASAAC es necesario para cumplir el Plan Maestro y permitir una evolución trazable mediante OpenSpec y Codex.

## Solución propuesta

Consultar API ARASAAC, normalizar resultados y metadatos, cachear referencias con trazabilidad.

## Alcance

- Implementar la capacidad descrita.
- Añadir pruebas y documentación.
- Respetar licencia ARASAAC, revisión humana y no PII cuando aplique.

## Fuera de alcance

No descarga masiva sin control; no modifica pictogramas.

## Riesgos

- Incumplimiento de licencia.
- Falta de trazabilidad.
- Complejidad excesiva.
- Pérdida de accesibilidad.

## Métrica de éxito

search/get devuelven IDs reales y metadatos normalizados.
