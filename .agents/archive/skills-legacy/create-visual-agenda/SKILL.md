---
name: create-visual-agenda
description: Crear agenda visual accesible con pictogramas ARASAAC reales, desde intake guiado hasta exportación con revisión humana.
metadata:
  type: workflow
  source_id: create_visual_agenda
---

# Workflow: create_visual_agenda

## Pasos

1. **guided_intake** — Intake guiado: objetivo, contexto, nivel, idioma
2. **privacy_check** — Validar ausencia de PII
3. **caasaac_strategy** — Definir estrategia CAA/SAAC
4. **draft_steps** — Generar borrador de pasos
5. **search_pictograms** — Buscar pictogramas reales ARASAAC
6. **edit** — Edición por usuario/profesional
7. **validate** — Ejecutar validadores de material
8. **human_review** — Revisión humana obligatoria
9. **export** — Exportar con créditos y manifiesto

## Reglas transversales

- Solo pictogramas reales ARASAAC.
- Revisión humana obligatoria antes de exportar.
- Atribución visible en toda exportación.
- Sin datos personales en MVP.
- OpenSpec aprobada para cambios de producto/código.


