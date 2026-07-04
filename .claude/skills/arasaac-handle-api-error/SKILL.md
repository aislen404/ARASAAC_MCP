---
name: arasaac-handle-api-error
description: Skill arasaac/handle api error para ARASAAC Social MCP Platform. Gates críticos: license, privacy, human_review. Requiere OpenSpec aprobada.
metadata:
  domain: arasaac
  requires_openspec: true
  critical_gates: ['license', 'privacy', 'human_review']
---

# skill.arasaac.handle_api_error

## Propósito

Ejecutar la capacidad `skill.arasaac.handle_api_error` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `arasaac/handle_api_error`.

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
