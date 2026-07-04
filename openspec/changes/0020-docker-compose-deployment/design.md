# Design — 0020-docker-compose-deployment

Compose incluye PostgreSQL 17 con volumen y healthcheck. La API usa SQLAlchemy y
crea únicamente las tablas mínimas de materiales/eventos. Los payloads se
revalidan con Pydantic al leer. Sin `DATABASE_URL`, tests usan memoria.

No hay credenciales reales: el compose local usa valores de desarrollo no
sensibles y `.env.example` documenta overrides.
