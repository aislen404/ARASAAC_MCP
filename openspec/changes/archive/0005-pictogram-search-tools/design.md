# Design — 0005-pictogram-search-tools

REST y MCP comparten el mismo servicio. Los resultados son candidatos: ninguna
selección se considera definitiva sin intervención humana. Query, locale, límites
y longitud se validan con Pydantic `extra=forbid`.

La sugerencia textual usa tokenización determinista, preserva orden y limita el
número de términos. No llama a modelos ni crea recursos gráficos.
