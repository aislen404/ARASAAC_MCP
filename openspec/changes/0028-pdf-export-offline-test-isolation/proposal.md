# Proposal — 0028 PDF Export Offline Test Isolation

## Problema

`GET /api/materials/{id}/export?format=pdf` resuelve cada pictograma llamando
siempre a `_fetch_official_image`, que hace una petición HTTP real a
`static.arasaac.org`. El test de integración de API
`test_export_pdf_after_approval` (en `test_material_api_extended.py`) ejercita
esta ruta sin ningún mecanismo de sustitución, por lo que depende de acceso a
internet real hacia ARASAAC para pasar.

Esto contradice el principio del propio plan de pruebas
(`docs/testing/test-plan-mvp0.md`, sección 9): "CI no valida credenciales ni
coste del proveedor real; usa dobles estructurales" — ese principio ya se
aplica a IA y al conector ARASAAC de búsqueda, pero no se aplicaba a la
generación de PDF. En entornos sin salida a internet (detectado durante un
UAT ejecutado en un sandbox aislado) el test falla con 409, enmascarado como
"exportación bloqueada", cuando la causa real es un fallo de red.

## Cambio propuesto

1. Añadir una dependencia FastAPI `get_image_fetcher` en
   `arasaac_platform.api.materials`, análoga a `get_repository`, que expone el
   fetcher de imágenes usado por `export_pdf` y es sobrescribible mediante
   `app.dependency_overrides` en tests.
2. Actualizar `export_material` para inyectar `fetch_image` en lugar de dejar
   que `export_pdf` resuelva siempre su fetcher por defecto.
3. Actualizar `test_export_pdf_after_approval` para sobrescribir la
   dependencia con una imagen en memoria (PNG 1x1), eliminando la llamada de
   red real y haciendo el test determinista y offline.

## Fuera de alcance

- Cambios en el conector de búsqueda ARASAAC (ya tiene test opt-in
  `ARASAAC_LIVE_TEST=1`).
- Cambios en el formato o contenido del PDF generado.
- Nuevas pruebas de humo con red real (ya cubiertas de forma opt-in en otros
  módulos).

## Valor

El test suite de API queda 100% ejecutable sin acceso a internet, consistente
con el resto de la política de dobles estructurales del proyecto, sin perder
cobertura sobre la lógica de exportación ni sobre el contrato HTTP.
