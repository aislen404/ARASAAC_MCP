---
name: cee-conacee-kit
description: Generar kit CEE/CONACEE: PRL, rutinas, señalética y pack exportable.
metadata:
  type: workflow
  source_id: cee_conacee_kit
---

# Workflow: cee_conacee_kit

## Pasos

1. **select_process** — Seleccionar proceso CEE
2. **domain_template** — Aplicar plantilla de dominio NGO/CEE
3. **caasaac_review** — Revisión metodológica CAA/SAAC
4. **search_pictograms** — Buscar pictogramas reales ARASAAC
5. **generate_pack** — Generar pack de materiales
6. **expert_review_flag** — Marcar contenido que requiere revisión experta
7. **validate** — Ejecutar validadores de material
8. **export** — Exportar con créditos y manifiesto

## Reglas transversales

- Solo pictogramas reales ARASAAC.
- Revisión humana obligatoria antes de exportar.
- Atribución visible en toda exportación.
- Sin datos personales en MVP.
- OpenSpec aprobada para cambios de producto/código.


