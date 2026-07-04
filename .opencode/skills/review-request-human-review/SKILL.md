---
name: review-request-human-review
description: Skill review/request human review para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: review
  requires_openspec: true
---

# skill.review.request_human_review

## Propósito

Ejecutar la capacidad `skill.review.request_human_review` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `review/request_human_review`.

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
