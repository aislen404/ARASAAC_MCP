# Arquitectura de la plataforma

La plataforma separa Web, API, servidor MCP y PostgreSQL. La Web solo consume la
API mediante un proxy same-origin. La API concentra conectores externos,
gobernanza, materiales, revisión, exportación y planificación IA opcional.

El servidor MCP usa transporte stdio y una allowlist de tres tools con schemas
cerrados para búsqueda y consulta ARASAAC. No expone shell, filesystem ni
ejecución arbitraria. Cualquier tool futura requiere OpenSpec, schema estricto,
tests y revisión.

PostgreSQL persiste materiales y auditoría. Los prompts y planes IA no se
persisten. Los pictogramas se referencian por metadatos y URL oficial; no se
almacenan ni modifican como assets del repositorio.
