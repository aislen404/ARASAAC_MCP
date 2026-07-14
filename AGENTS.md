# AGENTS.md — ARASAAC Social MCP Platform

Este documento es la **fuente humana de reglas del repositorio**. La configuración operativa completa vive en [`.agents/00_OPERATING_MODEL.md`](.agents/00_OPERATING_MODEL.md).

---

## 1. Identidad del proyecto

Este repositorio implementa una plataforma social no comercial para generar materiales accesibles usando exclusivamente pictogramas reales de ARASAAC, con MCP, Web App accesible AA, revisión humana, atribución visible y trazabilidad completa.

## 2. Reglas absolutas

1. No generar pictogramas con IA.
2. No imitar el estilo ARASAAC con IA.
3. No modificar pictogramas ARASAAC.
4. No eliminar ni ocultar atribución.
5. No exportar material final sin revisión humana aprobada.
6. No vincular materiales a personas concretas en MVP.
7. No introducir datos personales sensibles.
8. No usar el sistema para diagnóstico médico, psicológico, educativo o CAA.
9. No implementar ejecución arbitraria en MCP.
10. No añadir tools MCP sin schema estricto, tests y revisión de seguridad.

> Estas 10 reglas son **inmutables**. Cualquier PR que las contradiga se rechaza sin excepción.

## 3. Stack aprobado

- Backend: Python + FastAPI + Pydantic.
- Frontend: Next.js + React + TypeScript.
- DB: PostgreSQL + pgvector.
- Cache: Redis opcional.
- Deploy MVP: Docker Compose.
- Auth MVP: sin auth; futuro Keycloak.
- Export: HTML/PDF primero; DOCX/PPTX/ZIP después.

## 4. Modelo agentico (v2)

El sistema opera con **5 agentes-fase** que orquestan **25 personas** de dominio, invocan **10 skills** ejecutables y siguen **4 workflows** parametrizables mediante **4 prompts** (`/new-spec`, `/implement-task`, `/verify-change`, `/archive-change`).

| Fase | Agente | Propósito |
|------|--------|-----------|
| Spec | `spec` | Convertir necesidad social en OpenSpec change (proposal/design/tasks/spec). |
| Build | `build` | Implementar contra task atómica respetando stack y reglas. |
| Verify | `verify` | Tests + gates críticos (license, privacy, human_review) + a11y AA. |
| Docs | `docs` | Actualizar READMEs, manuales y notas de release. |
| Release | `release` | Empaquetar, archivar OpenSpec y publicar. |

Las 25 personas (arquitecto, backend, frontend, mcp-architect, license-legal, privacy-ethics, caasaac-methodology, easy-reading, ux-accessibility, product-owner-social, qa, security, devops, observability, release-manager, arasaac-liaison, data-connector, semantic-search, export-document, documentation, cognitive-accessibility, accessibility-qa, ngo-cee-domain, openspec-steward, test-automation) **no se seleccionan directamente**: los agentes-fase las invocan según contexto.

## 5. Flujo OpenSpec obligatorio

Antes de escribir código:

1. `/new-spec` → crear change folder en `openspec/changes/<id>/`.
2. Redactar `proposal.md`, `design.md`, `tasks.md`, `spec.md`.
3. `/verify-change` sobre el borrador.
4. `/implement-task` contra task atómica (agente `build`).
5. Tests + `/verify-change` final (agente `verify`).
6. Docs (agente `docs`).
7. `/archive-change` (agente `release`).

## 6. Definition of Done

Una implementación está completa si:

- Tiene OpenSpec aprobado y archivado al cierre.
- Pasa tests, lint y typecheck.
- Cumple los 3 gates críticos: **license**, **privacy**, **human_review** (ver `.agents/rules/mandatory-gates.md`).
- Incluye atribución ARASAAC si toca materiales.
- Mantiene audit log si genera/exporta.
- No introduce PII.
- Cumple accesibilidad AA si toca frontend.
- Actualiza documentación.

## 7. Seguridad MCP

- Allowlist estricta de tools.
- Validación Pydantic de todos los inputs.
- Prohibido: shell execution, filesystem arbitrario, red fuera de conectores aprobados, secretos en logs.
- Registro de tool calls relevantes.

## 8. Política ARASAAC

Cada uso de pictograma debe almacenar: `ID ARASAAC`, `label`, `URL/origen`, `autor: Sergio Palao`, `propietario: Gobierno de Aragón`, `licencia: CC BY-NC-SA 4.0`, `fecha_recuperacion`, `material_id`. Cada exportación incluye atribución visible en `NOTICE-ARASAAC.md`-compatible form.

## 9. Accesibilidad

Frontend aspira a **WCAG 2.2 AA**: navegación por teclado, foco visible, contraste suficiente, estructura semántica, labels y errores claros, independencia del color, lenguaje comprensible, testeable con axe.

## 10. Regla operativa para agentes de coding

Todo agente de coding (Cursor, Codex, VS Code/Copilot, Claude Code, OpenCode) trabaja **siempre contra una task atómica de OpenSpec**. Si una task no tiene spec, no se implementa. Ante conflicto entre productividad y cumplimiento, **gana cumplimiento**.

## 11. Packs agenticos multi-IDE

Fuente canónica: [`.agents/`](.agents/). Los packs por IDE se **generan automáticamente**; no editar a mano.

| Herramienta | Pack generado |
|-------------|---------------|
| Cursor | `.cursor/` |
| Codex | `.codex/` |
| Claude Code | `.claude/` |
| OpenCode | `.opencode/` |
| VS Code / GitHub Copilot | `.github/` (agents, personas, skills, workflows-agents, prompts, instructions, copilot-instructions.md) |
| Obsidian (referencia humana) | `docs/obsidian/agent-pack/` |

**Regenerar tras editar `.agents/`:**

```bash
make agent-packs-sync    # o: .venv/bin/python scripts/sync_agent_packs.py
```

**Verificar sincronía (local o CI):**

```bash
make agent-packs-verify  # o: .venv/bin/python scripts/verify_agent_packs_sync.py
```

Requiere `pyyaml` (ya en `.venv`).

## 12. Documentación de referencia

- `.agents/00_OPERATING_MODEL.md` — modelo operativo completo.
- `.agents/rules/mandatory-gates.md` — 3 gates críticos (fuente única).
- `docs/agents/multi-ide-agent-packs.md` — guía multi-IDE.
- `.github/workflows/agent-packs.yml` — CI de sincronía.
