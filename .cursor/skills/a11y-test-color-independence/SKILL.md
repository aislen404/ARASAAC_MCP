---
name: a11y-test-color-independence
description: Skill a11y/test color independence para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: a11y
  requires_openspec: true
---

# skill.a11y.test_color_independence

## Propósito

Ejecutar la capacidad `skill.a11y.test_color_independence` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `a11y/test_color_independence`.

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

