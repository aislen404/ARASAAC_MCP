---
name: validate-license-notice-visible
description: Skill validate/license notice visible para ARASAAC Social MCP Platform. Gates críticos: license, privacy, human_review. Requiere OpenSpec aprobada.
disable-model-invocation: true
metadata:
  domain: validate
  requires_openspec: true
  critical_gates: ['license', 'privacy', 'human_review']
---

# skill.validate.license_notice_visible

## Propósito

Ejecutar la capacidad `skill.validate.license_notice_visible` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `validate/license_notice_visible`.

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

## Gates críticos adicionales

- `license`
- `privacy`
- `human_review`
