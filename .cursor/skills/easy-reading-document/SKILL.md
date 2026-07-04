---
name: easy-reading-document
description: Adaptar documento a lectura fácil con apoyo pictográfico y revisión humana.
metadata:
  type: workflow
  source_id: easy_reading_document
---

# Workflow: easy_reading_document

## Pasos

1. **source_intake** — Ingesta de documento fuente
2. **privacy_check** — Validar ausencia de PII
3. **extract_key_messages** — Extraer mensajes clave
4. **simplify** — Simplificar lenguaje
5. **map_concepts** — Mapear conceptos pictografiables
6. **search_pictograms** — Buscar pictogramas reales ARASAAC
7. **edit** — Edición por usuario/profesional
8. **validate** — Ejecutar validadores de material
9. **review** — Revisión humana o profesional antes de exportar
10. **export** — Exportar con créditos y manifiesto

## Reglas transversales

- Solo pictogramas reales ARASAAC.
- Revisión humana obligatoria antes de exportar.
- Atribución visible en toda exportación.
- Sin datos personales en MVP.
- OpenSpec aprobada para cambios de producto/código.

