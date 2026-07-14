---
name: implement-task
invokes_agent: build
slash_command: /implement-task
parameters:
  - change_id
  - task_id
description: Implementar una task atómica de una change OpenSpec aprobada.
---

# Prompt: /implement-task

Actúa como el **agente `build`** definido en `.agents/agents/build.agent.md`.

## Contexto de invocación

Voy a implementar una task atómica.

- **Change ID**: `{{change_id}}`
- **Task ID**: `{{task_id}}` (ej: `C5`, `D2`, o descripción exacta)

## Tu tarea

1. Lee `openspec/changes/{{change_id}}-*/tasks.md` y localiza la task `{{task_id}}`.
2. Verifica que sus dependencias están cerradas. Si no, detente y avísame.
3. Sigue el procedimiento del agente `build`:
   - Detecta subsistema por globs (backend / frontend / MCP / data / export / infra).
   - Consulta las personas técnicas relevantes.
   - Aplica la skill correspondiente (`arasaac-fetch`, `mcp-tool-scaffold`, `material-pipeline`, `export-with-manifest`).
4. Implementa el código respetando:
   - `.agents/rules/backend.md`, `frontend.md`, `mcp.md`, `export-license.md`, `platform.md` según toque.
   - Las 10 reglas absolutas (`AGENTS.md`).
   - Gates `license` y `privacy`.
5. Añade/actualiza tests (unit / contract / e2e según área).
6. Ejecuta localmente: `make lint`, `make typecheck`, `make test` (o equivalente por área).
7. Marca la task en `tasks.md`:
   ```md
   - [x] **{{task_id}}.** …
   ```
8. Al terminar, resume:
   - Archivos creados/modificados.
   - Tests añadidos.
   - Resultado de los comandos.
   - Sugerencia: siguiente task o `/verify-change {{change_id}}` si terminaste el bloque.

## Restricciones

- No modifiques archivos generados (`<!-- generated from .agents/ -->`).
- No introduzcas PII.
- No modifiques pictogramas ARASAAC.
- No añadas dependencias externas sin ADR en `design.md`.

## Referencias

- Agente: [`build.agent.md`](../agents/build.agent.md)
- Reglas de área: `.agents/rules/`
- Gates: [`mandatory-gates.md`](../rules/mandatory-gates.md)
