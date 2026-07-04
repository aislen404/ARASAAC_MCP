---
name: editor-update-text-block
description: Skill editor/update text block para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: editor
  requires_openspec: true
---

# skill.editor.update_text_block

## Propósito

Ejecutar la capacidad `skill.editor.update_text_block` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `editor/update_text_block`.

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
