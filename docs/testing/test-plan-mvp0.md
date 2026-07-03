# Plan de pruebas — MVP-0 project-foundation

## 1. Objetivo

Validar que el fundamento técnico puede presentarse como demo reproducible sin
incorporar capacidades fuera de `0001-project-foundation`. La suite verifica web,
API, placeholder MCP, orquestación y límites de cumplimiento.

## 2. Alcance

Incluye:

- pantalla de estado Next.js;
- healthcheck FastAPI;
- estado seguro del placeholder MCP;
- estructura y comandos de ciclo de vida;
- contratos HTTP nominales y errores;
- semántica básica, teclado y responsive;
- ausencia de pictogramas, PII, tools y llamadas externas en la demo;
- cobertura de código de backend y frontend.

Excluye ARASAAC, materiales, generación, exportación, autenticación, persistencia
y datos personales porque no existen en esta versión.

## 3. Estrategia y niveles

| Nivel | Herramienta | Propósito | Gate |
| --- | --- | --- | --- |
| Unitario/contrato Python | Pytest + pytest-cov | API y MCP | ≥75% por total |
| Unitario frontend | Vitest + V8 | renderizado de página/layout | ≥75% lines/functions/branches/statements |
| Smoke | Pytest | estructura, seguridad y Makefile | obligatorio |
| E2E | Playwright Chromium | flujos integrados y responsive | todos pasan |
| Calidad | Ruff, ESLint, mypy, TypeScript | estática | sin errores |

La cobertura no sustituye los casos funcionales. Los umbrales se aplican
separadamente a Python y frontend para impedir que un componente oculte la falta
de pruebas de otro.

## 4. Entorno

- Python 3.11+ con dependencias de `services/api` y `services/mcp`.
- Node.js 20+ y dependencias de `apps/web`.
- Chromium instalado mediante Playwright.
- Puertos libres: 3000, 8000 y 8001.
- Docker no es necesario para la suite; Playwright inicia procesos locales.

## 5. Casos de prueba

| ID | Área | Caso | Resultado esperado | Automatización |
| --- | --- | --- | --- | --- |
| WEB-001 | Web | Abrir `/` | HTTP 200 y título del proyecto | Playwright |
| WEB-002 | Web | Consultar estado MVP-0 | Estado visible “Base técnica disponible” | Playwright |
| WEB-003 | Web | Revisar límites | Se muestran los cuatro límites aprobados | Playwright |
| WEB-004 | Accesibilidad | Estructura semántica | Un `main`, un `h1`, idioma `es` | Playwright |
| WEB-005 | Accesibilidad | Navegación por teclado | Sin trampas ni foco oculto | Playwright |
| WEB-006 | Responsive | Vista móvil 375×667 | Contenido visible sin scroll horizontal | Playwright |
| WEB-007 | Cumplimiento | Recursos visuales | No se renderizan imágenes/pictogramas | Playwright |
| WEB-008 | Cumplimiento | Tráfico de página | No hay peticiones a hosts externos | Playwright |
| API-001 | API | `GET /health` | 200 y contrato exacto | Pytest + Playwright |
| API-002 | API | Método no permitido | 405 estructurado | Playwright |
| API-003 | API | Ruta inexistente | 404 estructurado | Playwright |
| MCP-001 | MCP | `GET /health` | 200 y servicio placeholder | Pytest + Playwright |
| MCP-002 | MCP | `GET /mcp/status` | `enabled=false`, `tools=[]` | Pytest + Playwright |
| MCP-003 | MCP | Método no permitido | 405 sin efectos | Playwright |
| MCP-004 | MCP | Ruta/tool inexistente | 404; no ejecución arbitraria | Playwright |
| FND-001 | Fundación | Archivos obligatorios | Estructura completa | Pytest smoke |
| FND-002 | Seguridad | Código MCP | Sin subprocess, shell ni tools | Pytest smoke |
| FND-003 | Operación | `make start/stop` | Comandos Compose seguros presentes | Pytest smoke |
| COV-001 | Cobertura | Backend/MCP | Total ≥75% | pytest-cov |
| COV-002 | Cobertura | Frontend | Cada métrica global ≥75% | Vitest V8 |

## 6. Comandos

```bash
make setup
make test-unit
make test-e2e
make test
make lint
make typecheck
```

`make test` es la suite completa y constituye el gate de la versión.

## 7. Criterios de entrada y salida

Entrada:

- OpenSpec 0001 disponible;
- dependencias instaladas;
- puertos requeridos libres.

Salida:

- todos los casos automatizados pasan;
- cobertura Python y frontend ≥75%;
- lint y typecheck sin errores;
- cualquier limitación ambiental queda documentada;
- no se detectan regresiones contra las reglas de `AGENTS.md`.

## 8. Riesgos

- Un puerto ocupado impide iniciar el entorno E2E: detener el proceso o usar la
  demo Compose existente con `reuseExistingServer`.
- La primera ejecución requiere descargar Chromium.
- Playwright valida esta versión mínima; nuevas capacidades requieren nuevos casos
  en su OpenSpec correspondiente.
