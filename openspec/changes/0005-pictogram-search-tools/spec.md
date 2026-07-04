# Spec — 0005-pictogram-search-tools

## Escenarios

- `search_pictograms` devuelve como máximo el límite solicitado.
- `get_pictogram` devuelve una referencia oficial por ID.
- `suggest_pictograms_for_text` devuelve candidatos deterministas por término.
- Inputs extra, vacíos, excesivos o locales no permitidos se rechazan.
- Todas las respuestas incluyen atribución y requieren selección humana.
