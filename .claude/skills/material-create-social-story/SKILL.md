---
name: material-create-social-story
description: Skill material/create social story para ARASAAC Social MCP Platform. Gates críticos: license, privacy, human_review. Requiere OpenSpec aprobada.
metadata:
  domain: material
  requires_openspec: true
  critical_gates: ['license', 'privacy', 'human_review']
---

# skill.material.create_social_story

## Propósito

Ejecutar la capacidad `skill.material.create_social_story` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `material/create_social_story`.

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
