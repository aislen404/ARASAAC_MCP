# Spec — 0001-project-foundation

## Capability

Fundamento técnico ejecutable del MVP-0.

## Escenarios

### Escenario 1 — healthcheck del backend

**Dado** que el backend está iniciado
**Cuando** se solicita `GET /health`
**Entonces** responde HTTP 200 con `status=ok` y `service=api`.

### Escenario 2 — estado mínimo del frontend

**Dado** que el frontend está iniciado
**Cuando** se visita `/`
**Entonces** muestra una página semántica con el nombre del proyecto, el estado
MVP-0 y los límites de funcionalidad actuales.

### Escenario 3 — placeholder MCP seguro

**Dado** que el servicio placeholder MCP está iniciado
**Cuando** se solicita `GET /mcp/status`
**Entonces** declara `enabled=false`, devuelve una lista `tools` vacía y no
ejecuta comandos ni realiza acceso arbitrario a red o filesystem.

### Escenario 4 — orquestación local

**Dado** que Docker y Docker Compose están disponibles
**Cuando** se ejecuta `make start`
**Entonces** se construyen los servicios `api`, `web` y `mcp`, y publican sus
healthchecks o pantalla de estado en puertos locales documentados. Al ejecutar
`make stop`, los servicios se detienen y se eliminan los recursos efímeros de
Compose.

### Escenario 5 — límites de cumplimiento

**Dado** el contenido implementado por esta unidad
**Cuando** se ejecutan los smoke tests
**Entonces** no se detectan secretos, PII, pictogramas, integración ARASAAC,
generación, exportación, autenticación ni tools MCP.

### Escenario 6 — automatización integral

**Dado** un entorno local con Python, Node.js y Chromium de Playwright
**Cuando** se ejecuta `make test`
**Entonces** se ejecutan pruebas unitarias, smoke y Playwright de los tres
servicios, y la ejecución falla si la cobertura de backend o frontend es inferior
al 75%.

## Criterios de aceptación

- La estructura separa backend, frontend, MCP, docs, tests y OpenSpec.
- Los contratos de salud tienen pruebas automatizadas.
- Los flujos MVP-0 tienen casos Playwright automatizados.
- Backend y frontend aplican un umbral de cobertura de código del 75%.
- El frontend tiene lint y typecheck.
- Docker Compose es válido o su validación queda documentada si Docker no existe.
- El README contiene comandos de arranque local.
- Solo se marcan como completadas tareas verificadas.
