---
name: openspec-validate-acceptance-criteria
description: Skill openspec/validate acceptance criteria para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: openspec
  requires_openspec: true
---

# skill.openspec.validate_acceptance_criteria

## Propósito

Ejecutar la capacidad `skill.openspec.validate_acceptance_criteria` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `openspec/validate_acceptance_criteria`.

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

