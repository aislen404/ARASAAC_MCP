# ARASAAC Social MCP Platform — Instrucciones Copilot

Este repositorio usa packs agenticos multi-IDE con fuente canónica en `.agents/`.

## Reglas universales

# Reglas absolutas del proyecto

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

# Flujo OpenSpec obligatorio

Antes de escribir código:

1. Crear change folder en `openspec/changes/<id>/`.
2. Redactar `proposal.md`, `design.md`, `tasks.md` y `spec.md`.
3. Ejecutar verificación.
4. Implementar con el agente de coding del IDE contra task atómica.
5. Ejecutar tests y actualizar docs.
6. Archivar OpenSpec al completar.


## Packs por IDE

- **Cursor:** `.cursor/`
- **Codex:** `.codex/`
- **Claude Code:** `.claude/`
- **OpenCode:** `.opencode/`
- **VS Code / Copilot:** `.github/` (este pack)
- **Obsidian (referencia humana):** `docs/obsidian/agent-pack/`

## Documentación maestra

- `AGENTS.md` — reglas del repositorio
- `.agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md` — definición operativa completa
- Skills portables: `.agents/skills/` (estándar Agent Skills)

Todos los participantes deben tener las mismas capacidades agenticas; solo cambia el formato por IDE.
