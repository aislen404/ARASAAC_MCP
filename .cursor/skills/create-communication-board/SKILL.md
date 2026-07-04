---
name: create-communication-board
description: Crear tablero de comunicación con categorías, pictogramas reales y validación CAA/SAAC.
metadata:
  type: workflow
  source_id: create_communication_board
---

# Workflow: create_communication_board

## Pasos

1. **guided_intake** — Intake guiado: objetivo, contexto, nivel, idioma
2. **domain_categories** — Seleccionar dominio y categorías
3. **caasaac_balance** — Revisar equilibrio de vocabulario CAA/SAAC
4. **search_pictograms** — Buscar pictogramas reales ARASAAC
5. **edit_grid** — Editar grid del tablero
6. **validate** — Ejecutar validadores de material
7. **human_review** — Revisión humana obligatoria
8. **export** — Exportar con créditos y manifiesto

## Reglas transversales

- Solo pictogramas reales ARASAAC.
- Revisión humana obligatoria antes de exportar.
- Atribución visible en toda exportación.
- Sin datos personales en MVP.
- OpenSpec aprobada para cambios de producto/código.


