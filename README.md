# ARASAAC Social MCP Platform

Fundamento técnico del MVP-0 para una futura plataforma social no comercial de
materiales accesibles. Esta unidad no integra ARASAAC, no contiene pictogramas y
no genera ni exporta materiales.

## Servicios

| Servicio | URL | Función actual |
| --- | --- | --- |
| Web | <http://localhost:3000> | Pantalla estática de estado |
| API | <http://localhost:8000/health> | Healthcheck |
| MCP | <http://localhost:8001/mcp/status> | Estado de allowlist; servidor real por stdio |
| PostgreSQL | interno | Persistencia de materiales y auditoría |

## Arranque con Docker

Requisito: Docker con Compose v2.

```bash
make start
```

Para detener los servicios:

```bash
make stop
```

`make start` construye y levanta en segundo plano la web, la API y el placeholder
MCP, y muestra las tres URLs de la demo. Si indica que Docker no está iniciado,
abre Docker Desktop y vuelve a ejecutarlo. La configuración puede validarse sin
construir imágenes mediante `docker compose config --quiet`.

PostgreSQL conserva materiales y auditoría al ejecutar `make stop`. Para eliminar
deliberadamente todos los datos locales:

```bash
make reset-data
```

No uses `reset-data` si necesitas conservar materiales de una demostración.

## Desarrollo local

Requisitos: Python 3.11+, Node.js 20+ y npm.

```bash
make setup
make dev-api
make dev-mcp
make dev-web
```

Cada comando `dev-*` ocupa una terminal. Para ejecutar las comprobaciones:

```bash
make test
make lint
make typecheck
make openspec-verify
```

`make test` ejecuta cobertura unitaria y todos los flujos Playwright. Backend y
frontend aplican por separado un umbral mínimo del 75%. Para aislar fallos:

```bash
make test-unit
make test-e2e
```

El plan y la matriz de casos están en
[`docs/testing/test-plan-mvp0.md`](docs/testing/test-plan-mvp0.md).
El último resultado registrado está en
[`docs/testing/test-report-mvp0.md`](docs/testing/test-report-mvp0.md).

El servidor MCP local usa transporte stdio:

```bash
make mcp-stdio
```

Su allowlist actual contiene únicamente búsqueda, consulta por ID y sugerencia
determinista de pictogramas ARASAAC.

## Límites de MVP-0

- Sin conexión ni consultas a ARASAAC.
- Sin pictogramas o contenido generado.
- Sin creación, revisión o exportación de materiales.
- Sin autenticación, perfiles, PII ni persistencia.
- Sin tools MCP, shell, acceso arbitrario a archivos o llamadas externas.

Las reglas vinculantes del proyecto están en [AGENTS.md](AGENTS.md) y la unidad de
trabajo actual en
[openspec/changes/0001-project-foundation](openspec/changes/0001-project-foundation).
