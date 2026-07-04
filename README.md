# ARASAAC Social MCP Platform

Plataforma social no comercial para preparar materiales accesibles con
pictogramas reales de ARASAAC. Incluye búsqueda oficial, agendas y tableros,
editor, revisión humana obligatoria, exportación atribuida, auditoría y un
asistente IA textual opcional.

La IA nunca genera, imita ni modifica pictogramas. Solo propone una estructura y
términos de búsqueda; una persona debe elegir cada candidato real de ARASAAC,
revisar el material y aprobarlo antes de exportar.

## Servicios

| Servicio | URL | Función |
| --- | --- | --- |
| Web | <http://localhost:3000> | Flujo guiado manual y asistido por IA |
| API | <http://localhost:8000/health> | ARASAAC, materiales, revisión, exportación e IA |
| Estado IA | <http://localhost:8000/api/ai/status> | Disponibilidad y límites públicos |
| MCP | <http://localhost:8001/mcp/status> | Allowlist segura; servidor real por stdio |
| PostgreSQL | interno | Persistencia de materiales y auditoría |

## Arranque con Docker

Requisito: Docker con Compose v2. El flujo completo manual funciona sin claves.

```bash
make start
```

Para detener los servicios:

```bash
make stop
```

`make start` construye y levanta en segundo plano web, API, MCP y PostgreSQL. Si
indica que Docker no está iniciado, abre Docker Desktop y vuelve a ejecutarlo. La
configuración puede validarse mediante `docker compose config --quiet`.

PostgreSQL conserva materiales y auditoría al ejecutar `make stop`. Para eliminar
deliberadamente todos los datos locales:

```bash
make reset-data
```

No uses `reset-data` si necesitas conservar materiales de una demostración.

## Activar la capa IA

La integración usa Responses API con salida estructurada y la clave permanece
exclusivamente en el servidor. Para una demo con IA real:

```bash
cp .env.example .env
```

Edita `.env` localmente:

```dotenv
AI_PROVIDER=openai
OPENAI_API_KEY=tu_clave_local
OPENAI_MODEL=gpt-5.4-mini
```

Después ejecuta `make start`. `.env` está ignorado por Git. No pegues la clave en
capturas, incidencias, materiales ni logs. Sin clave, `/api/ai/status` informa que
la función está desactivada y el flujo manual sigue disponible.

La elección de `gpt-5.4-mini` prioriza latencia y coste para una tarea estructurada;
puede cambiarse desde entorno. El proveedor recibe únicamente el escenario
genérico confirmado, no recibe pictogramas ni dispone de tools.

## Desarrollo local

Requisitos: Python 3.11+, Node.js 20+ y npm.

```bash
make setup
make dev-api
make dev-mcp
make dev-web
```

Cada comando `dev-*` ocupa una terminal. `make dev-api` carga `.env` si existe.
Para ejecutar las comprobaciones:

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

Su allowlist contiene únicamente búsqueda, consulta por ID y sugerencia
determinista de pictogramas ARASAAC. La IA no añade tools MCP.

## Límites vinculantes

- Solo pictogramas reales obtenidos desde ARASAAC.
- Sin generación, imitación o modificación de pictogramas mediante IA.
- Sin nombres, contacto, diagnósticos ni datos personales sensibles.
- Sin vinculación de materiales a personas concretas.
- Sin creación, aprobación o exportación automática.
- Sin autenticación en esta versión.
- Sin ejecución arbitraria, filesystem o shell en MCP.

Las reglas vinculantes están en [AGENTS.md](AGENTS.md). La capa IA está
especificada en
[openspec/changes/0021-governed-ai-assistant](openspec/changes/0021-governed-ai-assistant).
