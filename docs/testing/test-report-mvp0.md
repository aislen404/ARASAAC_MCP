# Informe de ejecución — MVP-0 project-foundation

Fecha: 2026-07-04

## Resultado

**PASS** — El gate de la versión se completa correctamente.

| Comprobación | Resultado |
| --- | --- |
| Pytest API, MCP, SQL y smoke | 39 pasan, 1 live opt-in omitido |
| Contrato live ARASAAC | 1/1 pasa |
| Cobertura Python | 89,09% |
| Vitest frontend | 5/5 pasan |
| Cobertura frontend | 91% statements; 76,47% branches; 88,63% functions; 95,5% lines |
| Playwright Chromium | 11/11 flujos pasan |
| Ruff | pasa |
| ESLint | pasa |
| mypy | pasa |
| TypeScript | pasa |
| npm audit | 0 vulnerabilidades |
| Docker Compose config | válida |

Los umbrales automáticos están configurados al 75% y todas las métricas los
superan.

## Flujos E2E cubiertos

- estado, shell y flujo guiado completo;
- estructura semántica, idioma y navegación de teclado;
- comportamiento responsive sin desbordamiento horizontal;
- ausencia de imágenes/pictogramas y llamadas externas;
- contratos nominales de API y MCP;
- métodos no permitidos, rutas inexistentes y tool MCP inexistente.
- creación de agenda, bloqueo de export, revisión, aprobación y descarga HTML;
- validación mínima de tablero y selección humana;
- axe WCAG A/AA sin violaciones serias o críticas.

## Observaciones

- FastAPI emite un aviso de deprecación de compatibilidad entre su TestClient y
  Starlette; no afecta al resultado y deberá revisarse al actualizar dependencias.
- El navegador integrado del entorno Codex no pudo adjuntar su webview por una
  incompatibilidad interna. La suite Playwright Chromium instalada en el proyecto
  sí ejecutó y superó los ocho flujos.
- Docker Desktop no estaba activo; `docker compose config` pasa y el repositorio
  SQL se valida con reinicio real sobre SQLite. La construcción/arranque de las
  imágenes PostgreSQL permanece pendiente de un daemon disponible.
