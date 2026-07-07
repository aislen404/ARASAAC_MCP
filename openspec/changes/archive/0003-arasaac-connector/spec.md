# Spec — 0003-arasaac-connector

## Escenarios

- Una búsqueda válida devuelve referencias ARASAAC normalizadas y limitadas.
- Una consulta por ID devuelve metadatos completos y URL oficial.
- Locale, texto o ID inválido se rechazan antes de acceder a red.
- Timeout, error HTTP o JSON inválido produce un error controlado.
- El conector nunca acepta una URL arbitraria ni modifica un pictograma.
