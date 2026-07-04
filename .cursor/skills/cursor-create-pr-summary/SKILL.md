---
name: cursor-create-pr-summary
description: Skill cursor/create pr summary para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: cursor
  requires_openspec: true
---

# skill.cursor.create_pr_summary

## Propósito

Ejecutar la capacidad `skill.cursor.create_pr_summary` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `cursor/create_pr_summary`.

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

