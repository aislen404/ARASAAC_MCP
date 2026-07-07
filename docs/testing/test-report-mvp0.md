# Informe de ejecución — MVP gobernado con asistente IA

Fecha: 2026-07-07

## Resultado

**PASS en GitHub Actions Quality (`make test-uat`)** — El workflow Quality
vuelve a pasar en la PR `codex/project-foundation` tras la reparación documentada
en [openspec/changes/archive/0029-ci-quality-gate-repair](../../openspec/changes/archive/0029-ci-quality-gate-repair).
Run de referencia: [28885303177](https://github.com/aislen404/ARASAAC_MCP/actions/runs/28885303177).

| Comprobación | Resultado |
| --- | --- |
| GitHub Actions Quality (`make test-uat`) | **pasa** (lint, types, unit, 58/58 E2E, OpenSpec, agent-packs, build, audit low, compose) |
| Agent packs (`pyyaml` en venv) | pasa; sin `ModuleNotFoundError: yaml` |
| Playwright visual (linux snapshots) | 6/6 pasan en `ubuntu-latest` |
| Branch protection `main` | configurada exigiendo check `test` |

La ronda anterior (2026-07-06) quedó como **PASS parcial en sandbox local**; ver
sección histórica al final del informe.

## Reparación CI/CD (0029)

| Problema | Corrección |
| --- | --- |
| `agent-packs-verify` sin PyYAML en Quality | `pyyaml` en `make setup`; scripts con `.venv/bin/python3` |
| Paridad CI vs `make test-uat` incompleta | Quality ejecuta `make test-uat` único |
| Snapshots visuales solo macOS | Baselines `*-chromium-linux.png` + workflow `update-linux-snapshots.yml` |
| Flaky dark screenshots | Toggle accesible de tema + `animations: "disabled"` |

## Resultado histórico (2026-07-06, sandbox local)

**PASS con ejecución parcial por limitaciones del entorno de QA** — Se
ejecutó una ronda de UAT no solo happy-path (backend completo, contratos API
vía HTTP real, y ampliación de la suite Playwright con rutas negativas,
límites, gobernanza IA adversa, teclado completo y tipos de material sin
cobertura previa). Se encontró y corrigió un bug real (export PDF dependía de
red real a ARASAAC en los tests). La ejecución de Playwright con navegador
(`page`) no pudo completarse en el sandbox de QA por ausencia de librerías de
sistema de Chromium y de `root`; los specs quedan listos y se validó su
sintaxis y sus contrapartes basadas en `request` contra los servicios reales.

| Comprobación | Resultado |
| --- | --- |
| Pytest API, IA, MCP, SQL y smoke | 74 pasan, 3 opt-in/no configurados omitidos (antes: 1 fallo real) |
| Cobertura Python | 88,30% |
| Vitest frontend | 16/16 pasan |
| Cobertura frontend | 84,24% statements; 80,29% branches; 80,8% functions; 86,31% lines |
| Ruff | pasa |
| ESLint | pasa (5 warnings preexistentes de `<img>` sin `next/image`, no bloqueantes) |
| TypeScript (`tsc --noEmit`) | pasa |
| mypy | no verificable en este entorno (Python 3.10 disponible; el proyecto exige 3.11 por `enum.StrEnum`/`datetime.UTC`); ver limitación |
| Next.js build | pasa |
| Playwright — specs basados en `request` (contratos HTTP, API, MCP, límites, gobernanza IA negativa, ciclo de revisión) | 27/27 pasan contra servicios reales en ejecución |
| Playwright — specs basados en `page` (navegador: flujo manual/IA feliz, teclado, axe, visual, responsive) | no ejecutables en este sandbox (falta `libXdamage.so.1`, sin `root`); pendientes de ejecución en máquina con Chromium instalable |
| OpenSpec | pasa; se añadió el cambio 0028 (verificado con `make openspec-verify`) |
| Agent packs | en sincronía (`make agent-packs-verify`) |
| Docker Compose | no verificable en este sandbox (sin Docker); sintaxis de `docker-compose.yml` sin cambios |

## Bug encontrado y corregido

**PDF export dependía de red real a ARASAAC en los tests.**
`GET /api/materials/{id}/export?format=pdf` llamaba siempre a
`_fetch_official_image`, que hace una petición HTTP real a
`static.arasaac.org`, sin ningún mecanismo de sustitución a nivel de API. El
test `test_export_pdf_after_approval` dependía por tanto de acceso a internet
real, contradiciendo la política del proyecto de usar dobles estructurales
para dependencias externas. Corregido mediante inyección de dependencia
(`get_image_fetcher`, mismo patrón que `get_repository`) en
[openspec/changes/0028-pdf-export-offline-test-isolation](../../openspec/changes/0028-pdf-export-offline-test-isolation).
El test ahora es 100% offline y determinista; el comportamiento en producción
no cambia (sigue usando el fetcher real de ARASAAC por defecto).

## Ampliación de la suite Playwright (no solo happy path)

Se añadieron 4 archivos de spec (45 tests nuevos, total 58 en 11 archivos):

- `material-lifecycle-negative.spec.ts`: aprobar sin enviar a revisión (409);
  ciclo rechazar → reenviar → aprobar; exportación bloqueada en los 5
  formatos antes de aprobar (API y botones deshabilitados en la interfaz);
  límites del tablero (24 aceptadas, 25 y 1 rechazadas); payload con campos
  extra o pictograma sin licencia rechazado.
- `ai-governance-negative.spec.ts`: email, teléfono, DNI/NIE, URL y lenguaje
  diagnóstico rechazados con 422 antes de tocar el proveedor; falta de
  confirmación de privacidad; cantidad de conceptos fuera de rango; proveedor
  no disponible (formulario bloqueado, flujo manual utilizable); error
  transitorio del proveedor (504) informado sin crear material; plan con
  cero candidatos exige búsqueda manual.
- `accessibility-full-keyboard.spec.ts`: flujo completo (buscar → seleccionar
  → crear → enviar → aprobar) operado solo con teclado (foco + Enter/Espacio,
  sin clicks de ratón); finalización funcional (no solo visual) del flujo a
  768px (tablet).
- `material-types-smoke.spec.ts`: lectura fácil, historia social y señalética
  — tipos de material expuestos en la interfaz sin ninguna prueba previa.

Los 27 tests de estos archivos y de los preexistentes que usan el fixture
`request` (sin navegador) se ejecutaron contra la API y el servidor MCP reales
en este entorno y pasan. Los tests que usan el fixture `page` requieren un
navegador Chromium funcional; se validó que los 58 tests totales cargan y
parsean correctamente (`npx playwright test --list`), pero su ejecución con
navegador queda pendiente de una máquina con Chromium instalable (ver más
abajo). Se añadió `make test-uat` como comando único que ejecuta lint,
typecheck, unitario, E2E completo, OpenSpec, agent-packs, build, `npm audit` y
validación de Docker Compose.

## Limitaciones del entorno de QA (sandbox aislado, no del proyecto)

- **Sin Python 3.11**: el sandbox solo tiene Python 3.10 y no hay acceso de
  red a los repositorios que lo proveerían (apt, python.org, GitHub releases
  están fuera de la allowlist del proxy). Se usó 3.10 con dos shims de
  compatibilidad exclusivos del entorno de prueba (`enum.StrEnum`,
  `datetime.UTC`), verificados funcionalmente equivalentes; no se modificó el
  `requires-python` real del proyecto (sigue en `>=3.11`, correcto). `mypy` no
  es representativo bajo 3.10 y no se cuenta como ejecutado.
- **Sin Chromium ejecutable**: falta `libXdamage.so.1` del sistema y no hay
  `sudo`/root para instalarlo, ni acceso a los repositorios apt que lo
  proveerían. Todos los tests que dependen de un navegador (`page`) quedan
  sin ejecutar aquí.
- **Sin Docker**: no está instalado en el sandbox; no se pudo validar
  `docker compose config --quiet` en esta ronda (sin cambios en
  `docker-compose.yml`, riesgo bajo).
- **Sin red hacia ARASAAC/OpenAI reales**: consistente con la política del
  proyecto de dobles estructurales; no afecta a esta ronda salvo por el bug
  descrito arriba, ya corregido.

**Recomendación**: ejecutar `make test-uat` en una máquina con Docker y
Chromium instalable (la del propio equipo, o CI) para completar la cobertura
de navegador (flujo manual/IA feliz, teclado visual, axe, regresión visual,
responsive) que no pudo verificarse en este sandbox.

## Capa IA verificada

- Estado seguro con proveedor disponible/no disponible.
- Schema cerrado para input, plan textual y candidatos.
- Confirmación explícita de escenario genérico.
- Bloqueo previo de email, teléfono, DNI/NIE, URL y lenguaje diagnóstico
  (ahora también cubierto end-to-end vía HTTP real en Playwright, no solo
  unitario).
- Responses API mediante SDK oficial, structured output y `store=False`.
- Ausencia de tools, endpoints de imagen, URL de proveedor arbitraria y logs
  de contenido.
- Segunda validación de salida, cantidad exacta y timeout/fallos controlados.
- Resolución posterior de cada término contra ARASAAC.
- Cero auto-selección, creación, aprobación o exportación por IA.
- Degradación segura: el flujo manual permanece disponible sin clave.

## Riesgos y pendientes

- Ejecutar `make test-uat` completo (con navegador y Docker) en una máquina
  sin las limitaciones descritas arriba, y registrar el resultado.
- Antes de una presentación externa debe inyectarse una clave efímera
  mediante `.env` o gestor de secretos y ejecutar un smoke real sin PII.
- El guard local detecta patrones evidentes, no sustituye un proceso
  organizativo de privacidad ni autoriza introducir datos personales.
- La dependencia externa puede fallar o tener coste/latencia; el producto
  falla cerrado y conserva la ruta manual.
- FastAPI emite un aviso de deprecación entre TestClient y Starlette; no
  afecta a esta versión y debe revisarse al actualizar dependencias.
