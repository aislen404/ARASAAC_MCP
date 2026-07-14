---
name: material-pipeline
description: >-
  Pipeline unificado de materiales: intake → search pictograms → edit →
  validate → human-review → export. Absorbe todas las skills create-* y editor-*.
inputs:
  - material_type   # agenda | board | story | signage | easy-reading | cee-kit | cermi-kit
  - intake          # dict con campos del intake guiado
outputs:
  - MaterialDraft (in DB) con estado según fase
  - Exportables (tras aprobación humana)
invoked_by_agents: [build]
gates: [license, privacy, human_review]
---

# Skill: material-pipeline

## Cuándo usarla
- Un usuario (persona) crea, edita o exporta un material desde la Web App.
- Un workflow de negocio (`create-visual-agenda`, `create-communication-board`, `create-easy-reading`) delega la construcción a este pipeline.

## Estados del material

```
draft → in_review → approved → exported
                 ↘ rejected → draft
```

## Procedimiento paso a paso

1. **Intake guiado** (por tipo de material):
   - Recoger título, propósito, audiencia, contexto de uso.
   - Validar ausencia de PII (gate `privacy`): nombres reales, DNI, direcciones, fotos identificables → rechazar.
2. **Búsqueda de pictogramas** vía skill [`arasaac-fetch`](../arasaac-fetch/SKILL.md):
   - Sugerir por keyword.
   - Permitir búsqueda manual.
   - **Nunca** generar pictogramas con IA (regla absoluta #1).
3. **Edición**:
   - Reemplazo, reorden, ajuste de layout, actualización de bloques de texto.
   - Cada acción registra evento (audit log).
   - No modificar el SVG/PNG del pictograma (regla absoluta #3).
4. **Validación automática** vía skill [`compliance-scan`](../compliance-scan/SKILL.md):
   - Pictogram IDs reales (contra cache/API).
   - Densidad visual dentro de límites CAA/SAAC.
   - Lenguaje llano (si el material tiene texto).
   - Contexto no comercial verificado.
5. **Human review** vía skill [`human-review-gate`](../human-review-gate/SKILL.md):
   - Estado pasa a `in_review`.
   - Reviewer humano aprueba o rechaza con motivo.
   - Aprobación registra: reviewer, fecha, versión (hash).
6. **Export** vía skill [`export-with-manifest`](../export-with-manifest/SKILL.md):
   - Solo si `approved`.
   - Formatos: HTML/PDF/DOCX/PPTX/ZIP.
   - Manifest de atribución adjunto (gate `license`).
   - Estado pasa a `exported`.

## Gates aplicados

| Gate | Fase que lo verifica |
|---|---|
| `license` | intake (no pictogramas IA) + arasaac-fetch + export |
| `privacy` | intake (no PII) + validación |
| `human_review` | transición `in_review` → `approved` |

## Errores comunes

- ❌ Saltar `human_review` "porque es urgente" → viola regla absoluta #5.
- ❌ Editar el binario del pictograma → viola regla absoluta #3.
- ❌ Aceptar intake con foto de un menor → viola gate `privacy`.
- ❌ Exportar sin manifest → viola gate `license`.
- ❌ Reactivar `exported` → crea nueva versión, no editar la aprobada.

## Ver también

- Skills: [`arasaac-fetch`](../arasaac-fetch/SKILL.md), [`compliance-scan`](../compliance-scan/SKILL.md), [`human-review-gate`](../human-review-gate/SKILL.md), [`export-with-manifest`](../export-with-manifest/SKILL.md)
- Reglas: `.agents/rules/mandatory-gates.md`
- Workflows: `create-visual-agenda`, `create-communication-board`, `create-easy-reading`
