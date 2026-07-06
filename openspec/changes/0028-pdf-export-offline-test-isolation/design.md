# Design — 0028 PDF Export Offline Test Isolation

## Contexto

`services/api/src/arasaac_platform/services/export.py::export_pdf` ya acepta
un parámetro opcional `fetch_image: ImageFetcher | None`, usado internamente
así: `fetcher = fetch_image or _fetch_official_image`. El problema no está en
`export_pdf` (ya es inyectable a nivel de función) sino en que la ruta HTTP
`export_material` en `api/materials.py` nunca pasaba ese parámetro, por lo que
siempre resolvía el fetcher oficial real.

## Decisión

Aplicar el mismo patrón de Dependency Injection que ya usa el repositorio
(`get_repository` + `RepositoryDependency`):

```python
def get_image_fetcher() -> ImageFetcher | None:
    """None conserva el fetcher oficial de export_pdf; overridable en tests."""
    return None

ImageFetcherDependency = Annotated[ImageFetcher | None, Depends(get_image_fetcher)]
```

y añadir `fetch_image: ImageFetcherDependency` como parámetro de
`export_material`, pasándolo a `export_pdf(material, fetch_image=fetch_image)`.

Se eligió devolver `None` por defecto (en vez de importar
`_fetch_official_image`, símbolo privado del módulo `export.py`) para no
acoplar `api/materials.py` a un símbolo interno de otro módulo; `export_pdf`
ya sabe resolver su propio fetcher por defecto cuando recibe `None`.

## Alternativas consideradas

- **Monkeypatch de `httpx.AsyncClient.get` en el test**: más frágil, acopla el
  test a detalles de implementación de `_fetch_official_image` en lugar de al
  contrato público de `export_pdf`.
- **Marcar el test como `@pytest.mark.integration` y excluirlo por defecto**:
  perdería cobertura de la ruta HTTP completa en cada ejecución local/CI sin
  ganar nada, dado que la inyección de dependencias resuelve el problema sin
  sacrificar cobertura.

## Impacto

- Sin cambios de contrato público (mismo request/response de
  `/api/materials/{id}/export`).
- Sin cambios de comportamiento en producción (el fetcher por defecto sigue
  siendo `_fetch_official_image` cuando no hay override).
- Test suite de API pasa a ser 100% offline.
