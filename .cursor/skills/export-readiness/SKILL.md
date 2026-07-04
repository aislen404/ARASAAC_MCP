---
name: export-readiness
description: Validar readiness global antes de exportar: PII, licencia, pictogramas, revisión.
metadata:
  type: workflow
  source_id: export_readiness
disable-model-invocation: true
---

# Workflow: export_readiness

## Pasos

1. **no_pii** — validate_no_personal_data
2. **real_ids** — validate_pictogram_ids_real
3. **no_modified_pictograms** — validate_no_modified_pictograms
4. **license_visible** — validate_license_notice_visible
5. **non_commercial** — validate_non_commercial_context
6. **plain_language** — validate_plain_language
7. **visual_density** — validate_visual_density
8. **human_review** — validate_human_review_approved
9. **manifest** — validate_manifest_complete

## Reglas transversales

- Solo pictogramas reales ARASAAC.
- Revisión humana obligatoria antes de exportar.
- Atribución visible en toda exportación.
- Sin datos personales en MVP.
- OpenSpec aprobada para cambios de producto/código.


