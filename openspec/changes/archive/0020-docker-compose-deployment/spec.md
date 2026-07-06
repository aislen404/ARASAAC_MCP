# Spec — 0020-docker-compose-deployment

- `make start` espera a PostgreSQL y levanta todos los servicios.
- Materiales y auditoría persisten tras reiniciar API.
- Payload corrupto no se devuelve sin validación.
- `make stop` no elimina datos; reset requiere comando explícito documentado.
- No hay secretos ni PII en imágenes, logs o variables.
