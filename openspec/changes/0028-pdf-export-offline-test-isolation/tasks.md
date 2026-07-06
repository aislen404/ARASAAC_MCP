# Tasks — 0028

## 1. OpenSpec

- [x] Crear `proposal.md`, `design.md`, `tasks.md`, `spec.md`.
- [x] Ejecutar `make openspec-verify`.

## 2. Backend

- [x] Añadir `get_image_fetcher` e `ImageFetcherDependency` en
      `arasaac_platform/api/materials.py`.
- [x] Inyectar `fetch_image` en `export_material` y pasarlo a `export_pdf`.

## 3. Tests

- [x] Actualizar `test_export_pdf_after_approval` para usar
      `app.dependency_overrides[get_image_fetcher]` con una imagen en
      memoria, eliminando la dependencia de red real.
- [x] Ejecutar `pytest services/api/tests -q` y confirmar 0 fallos sin acceso
      a internet.

## 4. Verificación

- [x] `ruff check services` sin errores.
- [x] Cobertura Python ≥75% (medida: 88.30%).
- [ ] `mypy services/api/src` — no verificable en el entorno de QA por
      ausencia de Python 3.11 (ver limitación en test-report); sin cambios de
      tipado nuevos más allá de los ya existentes en el módulo.
