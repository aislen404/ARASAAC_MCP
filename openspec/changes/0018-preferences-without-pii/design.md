# Preferencias sin PII — API mínima

Almacena plantillas genéricas de entidad (nombre, idioma, densidad visual) sin datos personales.

Endpoints:

- `GET /api/preferences/templates` — listado
- `POST /api/preferences/templates` — crear plantilla genérica

Validación: rechaza campos que parezcan PII (email, teléfono, nombres propios en título).
