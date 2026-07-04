---
name: editor-replace-pictogram
description: Skill editor/replace pictogram para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: editor
  requires_openspec: true
---

# skill.editor.replace_pictogram

## Propósito

Ejecutar la capacidad `skill.editor.replace_pictogram` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `editor/replace_pictogram`.

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

