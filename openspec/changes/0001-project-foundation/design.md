# Design — 0001-project-foundation

## Arquitectura mínima

```text
apps/web          Next.js: pantalla de estado
services/api      FastAPI: GET /health
services/mcp      FastAPI: placeholder sin tools
tests/smoke       validación estática del fundamento
docs              notas de arquitectura y arranque
```

Cada servicio es independiente y se construye con su propio Dockerfile. Docker
Compose solo conecta los contenedores necesarios para comprobar el fundamento.
No se incorpora base de datos porque esta unidad no tiene estado.

## Contratos

### API

`GET /health` devuelve HTTP 200:

```json
{"status": "ok", "service": "api"}
```

### MCP placeholder

`GET /health` devuelve el estado del proceso. `GET /mcp/status` declara
explícitamente que el servidor no está operativo y que su allowlist de tools está
vacía. No implementa transporte MCP, ejecución de comandos, acceso al filesystem
ni llamadas de red.

### Web

La ruta `/` muestra nombre del proyecto, estado MVP-0 y límites actuales. No carga
datos externos ni incluye contenido generado o pictogramas.

## Seguridad y cumplimiento

- No hay secretos; `.env.example` contiene únicamente URLs locales no sensibles.
- No hay PII, identidades, ejemplos de personas o datos persistidos.
- No existen tools MCP.
- No existen conectores ni llamadas a ARASAAC.
- No existen rutas de generación o exportación.
- La interfaz establece una base semántica y navegable por teclado.

## Verificación

- Pytest para contratos HTTP de API y MCP.
- ESLint y TypeScript para el frontend.
- Smoke tests de estructura y límites de alcance.
- `docker compose config` para validar la orquestación cuando Docker esté
  disponible.
