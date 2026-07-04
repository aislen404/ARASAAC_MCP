# AGENTS.md — ARASAAC Social MCP Platform

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

## 3. Stack aprobado

- Backend: Python + FastAPI + Pydantic.
- Frontend: Next.js + React + TypeScript.
- DB: PostgreSQL + pgvector.
- Cache: Redis opcional.
- Deploy MVP: Docker Compose.
- Auth MVP: sin auth; futuro Keycloak.
- Export: HTML/PDF primero; DOCX/PPTX/ZIP después.

## 4. Flujo OpenSpec obligatorio

Antes de escribir código:

1. Crear change folder en `openspec/changes/<id>/`.
2. Redactar `proposal.md`.
3. Redactar `design.md` si hay arquitectura o decisión técnica.
4. Redactar `tasks.md` con tareas atómicas.
5. Redactar `spec.md` con escenarios verificables.
6. Ejecutar verificación.
7. Implementar con el agente de coding del IDE (Cursor, Codex, VS Code/Copilot, Claude Code u OpenCode).
8. Ejecutar tests.
9. Actualizar docs.
10. Archivar OpenSpec al completar.

## 5. Definition of Done

Una implementación está completa si:

- Tiene OpenSpec aprobado.
- Tiene tests.
- Pasa lint/typecheck.
- No viola licencia ARASAAC.
- Incluye atribución si toca materiales.
- Mantiene audit log si genera/exporta.
- No introduce PII.
- Cumple accesibilidad AA si toca frontend.
- Actualiza documentación.

## 6. Seguridad MCP

- Usar allowlist de tools.
- Validar todos los inputs con Pydantic.
- No shell execution.
- No filesystem arbitrary access.
- No network calls fuera de conectores aprobados.
- No secretos en logs.
- Registrar tool calls relevantes.

## 7. Política ARASAAC

Cada uso de pictograma debe almacenar:

- ID ARASAAC.
- Label usado.
- URL/origen.
- Autor: Sergio Palao.
- Propietario: Gobierno de Aragón.
- Licencia: CC BY-NC-SA.
- Fecha de recuperación.
- Material donde se usó.

Cada exportación debe incluir atribución visible.

## 8. Accesibilidad

El frontend debe aspirar a WCAG 2.2 AA:

- Navegación por teclado.
- Foco visible.
- Contraste suficiente.
- Estructura semántica.
- Labels y errores claros.
- No depender solo del color.
- Textos comprensibles.
- Componentes testeables con axe.

## 9. Agentes autorizados

- Product Owner Agent.
- Accessibility Expert Agent.
- CAA/SAAC Methodology Agent.
- Foundation/NGO Domain Agent.
- MCP Architect Agent.
- Backend Agent.
- Frontend Agent.
- Data/Indexing Agent.
- Export/Document Agent.
- QA Agent.
- Accessibility QA Agent.
- License Compliance Agent.
- Security Agent.
- Test Automation Agent.
- OpenSpec Steward.
- Architecture Reviewer.
- Risk & Compliance Agent.
- Documentation Agent.
- Release Manager Agent.

## 10. Instrucción a agentes de implementación

Todo agente de coding del equipo debe trabajar siempre contra una task atómica de OpenSpec. Si una tarea no tiene spec, no se implementa. Si se detecta conflicto entre productividad y cumplimiento, gana cumplimiento.

## 11. Packs agenticos multi-IDE

Fuente canónica compartida: `.agents/` (catálogos, contenido neutro, skills portables).

| Herramienta | Pack generado |
|-------------|---------------|
| Portable (todos) | `.agents/skills/` |
| Cursor | `.cursor/` |
| Codex | `.codex/` |
| Claude Code | `.claude/` |
| OpenCode | `.opencode/` |
| VS Code / GitHub Copilot | `.github/` |
| Obsidian (referencia humana) | `docs/obsidian/agent-pack/` |

Regenerar packs tras editar `.agents/`:

```bash
python3 scripts/sync_agent_packs.py
# o: make agent-packs-sync
```

Verificar sincronía (local o CI):

```bash
python3 scripts/verify_agent_packs_sync.py
# o: make agent-packs-verify
```

Documentación: [docs/agents/multi-ide-agent-packs.md](../docs/agents/multi-ide-agent-packs.md).
CI: [.github/workflows/agent-packs.yml](../.github/workflows/agent-packs.yml).

Documento operativo maestro: `.agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md`.
