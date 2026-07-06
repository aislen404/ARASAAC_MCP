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
| MCP | <http://localhost:8001/mcp/status> | HTTP de estado y allowlist; protocolo MCP real por stdio (`make mcp-stdio`) |
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

Los iconos e ilustraciones Convergencia Serena viven en `apps/web/assets/` y se
copian a `apps/web/public/convergencia-serena/` durante `npm run build` (y
`npm run dev`). La imagen Docker del servicio web incluye esa carpeta `public/` en
el contenedor final. Si los SVG aparecen rotos tras un cambio de assets, reconstruye
el servicio web: `docker compose up --build -d web`.

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

En la Web App, la sección «Proponer estructura con IA» muestra el estado del
servidor, mensajes de carga y errores. Si la IA aparece como no configurada con
`make start`, comprueba `.env` y consulta
<http://localhost:3000/backend/api/ai/status> (proxy interno hacia la API).

## Desarrollo local

Requisitos: Python 3.11+, Node.js 20+ y npm.

```bash
make setup
make dev-api
make dev-mcp
make dev-web
```

Cada comando `dev-*` ocupa una terminal. `make dev-api` carga `.env` si existe.

Sin `DATABASE_URL` en entorno, la API usa un repositorio en memoria (los datos no
persisten). Para paridad con Docker, levanta solo PostgreSQL y configura la URL:

```bash
make dev-db    # Postgres Docker en :5433 (evita conflicto con Postgres local en :5432)
# Añade DATABASE_URL a .env (ver .env.example)
```

Para ejecutar las comprobaciones:

```bash
make test
make lint
make typecheck
make openspec-verify
make agent-packs-verify
```

`make agent-packs-verify` comprueba que los packs generados (`.cursor/`, `.codex/`,
`.claude/`, etc.) estén sincronizados con la fuente canónica `.agents/`. Tras
editar catálogos o contenido en `.agents/`, regenera con `make agent-packs-sync`.
Ver [docs/agents/multi-ide-agent-packs.md](docs/agents/multi-ide-agent-packs.md).

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

El servidor MCP local usa transporte **stdio** (protocolo MCP completo):

```bash
make mcp-stdio
```

En Docker, el contenedor `mcp` expone solo un endpoint HTTP informativo
(`/mcp/status`) con la allowlist de tools. Los clientes MCP (Cursor, Claude Code,
etc.) deben conectarse al servidor stdio con `make mcp-stdio` o el binario
`arasaac-mcp`.

## Bóveda de conocimiento Obsidian

La documentación, OpenSpecs y conocimiento canónico pueden mantenerse
sincronizados con la bóveda iCloud `ARASAAC_Project`:

```bash
make obsidian-sync
make obsidian-sync-check
make obsidian-hooks-install
```

La sincronización es unidireccional repositorio → Obsidian, no copia secretos ni
código y preserva notas manuales. Consulta
[docs/obsidian/knowledge-sync.md](docs/obsidian/knowledge-sync.md).

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
[openspec/changes/archive/0021-governed-ai-assistant](openspec/changes/archive/0021-governed-ai-assistant).
