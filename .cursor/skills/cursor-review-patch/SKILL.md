---
name: cursor-review-patch
description: Skill cursor/review patch para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: cursor
  requires_openspec: true
---

# skill.cursor.review_patch

## Propósito

Ejecutar la capacidad `skill.cursor.review_patch` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `cursor/review_patch`.

## Salida esperada

```text
status: pass | warn | fail
summary: <resumen>
artifacts: <artefactos generados o modificados>
risks: <riesgos>
next_actions: <acciones>
```

## Gates

- Trabajar siempre contra OpenSpec aprobada.
- No generar ni modificar pictogramas ARASAAC.
- No exportar sin revisión humana aprobada.
- No introducir datos personales en MVP.
- Preservar atribución visible CC BY-NC-SA.

