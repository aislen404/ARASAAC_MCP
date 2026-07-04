---
name: docs-generate-arasaac-validation-dossier
description: Skill docs/generate arasaac validation dossier para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: docs
  requires_openspec: true
---

# skill.docs.generate_arasaac_validation_dossier

## Propósito

Ejecutar la capacidad `skill.docs.generate_arasaac_validation_dossier` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `docs/generate_arasaac_validation_dossier`.

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
