# Proposal — 0005-pictogram-search-tools

## Problema

Tools MCP de búsqueda pictográfica es necesario para cumplir el Plan Maestro y permitir una evolución trazable mediante OpenSpec y Codex.

## Solución propuesta

Implementar search_pictograms, get_pictogram, suggest_pictograms_for_text.

## Alcance

- Implementar la capacidad descrita.
- Añadir pruebas y documentación.
- Respetar licencia ARASAAC, revisión humana y no PII cuando aplique.

## Fuera de alcance

No inventa pictogramas; no genera imágenes.

## Riesgos

- Incumplimiento de licencia.
- Falta de trazabilidad.
- Complejidad excesiva.
- Pérdida de accesibilidad.

## Métrica de éxito

Tool calls devuelven resultados reales o vacío con error estructurado.
