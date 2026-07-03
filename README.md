# ARASAAC Social MCP Platform

Fundamento técnico del MVP-0 para una futura plataforma social no comercial de
materiales accesibles. Esta unidad no integra ARASAAC, no contiene pictogramas y
no genera ni exporta materiales.

## Servicios

| Servicio | URL | Función actual |
| --- | --- | --- |
| Web | <http://localhost:3000> | Pantalla estática de estado |
| API | <http://localhost:8000/health> | Healthcheck |
| MCP placeholder | <http://localhost:8001/mcp/status> | Estado seguro, sin tools |

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

## Límites de MVP-0

- Sin conexión ni consultas a ARASAAC.
- Sin pictogramas o contenido generado.
- Sin creación, revisión o exportación de materiales.
- Sin autenticación, perfiles, PII ni persistencia.
- Sin tools MCP, shell, acceso arbitrario a archivos o llamadas externas.

Las reglas vinculantes del proyecto están en [AGENTS.md](AGENTS.md) y la unidad de
trabajo actual en
[openspec/changes/0001-project-foundation](openspec/changes/0001-project-foundation).
