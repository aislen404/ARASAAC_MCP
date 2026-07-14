# Spec — 0036 Agent System Refactor

## MUST

### Estructura canónica `.agents/`

- MUST contener exactamente los siguientes catálogos: `agents.yaml`, `personas.yaml`, `skills.yaml`, `workflows.yaml`, `prompts.yaml`, `packs.yaml`.
- MUST contener `.agents/agents/` con exactamente 5 archivos `*.agent.md` (`spec`, `build`, `verify`, `docs`, `release`).
- MUST contener `.agents/personas/` con al menos las 15 personas mínimas requeridas (todas las responsabilidades de dominio previamente cubiertas por los 25 agentes-rol se conservan como personas).
- MUST contener `.agents/skills/` con exactamente 10 directorios listados en `catalog/skills.yaml`, cada uno con un `SKILL.md` no vacío y con procedimiento paso a paso.
- MUST contener `.agents/workflows/` con exactamente 4 archivos `*.workflow.md` (`spec-build-verify` + 3 de negocio).
- MUST contener `.agents/prompts/` con exactamente 4 archivos `*.prompt.md` (`new-spec`, `implement-task`, `verify-change`, `archive-change`).
- MUST contener `.agents/rules/mandatory-gates.md` como único punto de verdad para los 3 gates críticos (license, privacy, human-review).
- MUST contener `.agents/00_OPERATING_MODEL.md` como doc maestro operativo.
- MUST conservar la documentación previa y las 25 agentes/69 skills legacy en `.agents/archive/`.

### Contrato de archivos

- Cada `*.agent.md` MUST declarar en frontmatter YAML: `name`, `title`, `phase`, `invokes_personas`, `uses_skills`, `uses_workflows`, `mandatory_gates`.
- Cada `*.persona.md` MUST declarar `name`, `role`, `scope`, `gates_enforced`.
- Cada `SKILL.md` MUST declarar `name`, `description`, `inputs`, `outputs`, `gates` y MUST tener una sección `## Procedimiento paso a paso` con ≥ 3 pasos numerados.
- Cada `*.workflow.md` MUST declarar `name`, `kind`, `uses_agents` y tener una sección por paso del ciclo.
- Cada `*.prompt.md` MUST declarar `name`, `invokes_agent`, `parameters` y contener el prompt parametrizable con `{{placeholders}}`.
- Todo archivo generado por el sync MUST llevar header `<!-- generated from .agents/ — do not edit manually -->` y el hash SHA-256 del contenido fuente en frontmatter.

### Reglas y gates

- `mandatory-gates.md` MUST enumerar exactamente 3 gates: `license`, `privacy`, `human_review`, con criterios verificables por cada uno.
- Cada agente-fase y cada skill que tenga gates MUST referenciarlos por nombre (no duplicar texto).
- Las 10 reglas absolutas de `AGENTS.md` MUST permanecer sin cambios semánticos.
- El flujo obligatorio OpenSpec (proposal → design → tasks → spec → implementación → tests → docs → archive) MUST estar declarado en `spec-build-verify.workflow.md` con todos los pasos desarrollados.

### Sincronización multi-IDE

- `scripts/sync_agent_packs.py` MUST regenerar los packs de los 6 IDEs desde la fuente canónica sin intervención manual.
- Cada pack IDE MUST contener los 5 agentes-fase, las personas mínimas (15), las 10 skills, los 4 workflows y los 4 prompts, en el formato nativo del IDE:
  - **Cursor**: reglas en `.cursor/rules/*.mdc`; commands en `.cursor/commands/*.md`.
  - **Codex**: archivos plano en `.codex/{agents,personas,skills,workflows,prompts}/`.
  - **Claude Code**: `.claude/agents/`, `.claude/skills/`, `.claude/commands/` (slash-commands).
  - **OpenCode**: `.opencode/{agents,skills,commands}/`.
  - **VS Code/Copilot**: `.github/agents/`, `.github/prompts/`, `.github/instructions/*.instructions.md` (con `applyTo`), y `.github/copilot-instructions.md` regenerado desde template.
  - **Obsidian**: `docs/obsidian/agent-pack/` con las mismas piezas en formato humano/linkeable.
- El `.github/copilot-instructions.md` regenerado MUST estar completo (no truncado) e incluir explícitamente los 4 prompts como slash-commands (`/new-spec`, `/implement-task`, `/verify-change`, `/archive-change`).
- `scripts/verify_agent_packs_sync.py` MUST implementar los 9 invariantes descritos en `design.md` §4 y MUST fallar el proceso con exit code no-cero si detecta drift.

### CI

- `.github/workflows/agent-packs.yml` MUST ejecutar en cada PR: `sync_agent_packs.py --check` (dry-run que falla si generaría cambios) + `verify_agent_packs_sync.py` + los tests unitarios nuevos.
- El workflow MUST fallar si alguno de los 9 invariantes no se cumple.

### Migración y limpieza

- `.github/prompts/planMaterialsInboxAndPersistence.prompt.md` MUST moverse a `openspec/changes/0034-materials-inbox-and-persistence/implementation-plan.md`.
- Los 25 agentes legacy MUST estar copiados a `.agents/archive/agents-legacy/` antes de eliminarse de `.agents/content/agents/`.
- Las 69 skills legacy MUST estar copiadas a `.agents/archive/skills-legacy/` antes de eliminarse de `.agents/skills/`.
- Los docs maestros legacy (`02_AGENTES_SKILLS_WORKFLOWS.md`, `V2`, `00_MASTER_INDEX.md`, `01_INTRODUCCION_AGENTES_Y_SKILLS.md`) MUST moverse a `.agents/archive/docs-legacy/`.

## SHOULD

- SHOULD documentar la tabla de mapeo legacy→nuevo en `.agents/00_OPERATING_MODEL.md` para permitir búsqueda inversa.
- SHOULD generar el `AGENTS.md` de raíz desde template (fuente `.agents/rules/mandatory-gates.md` + `catalog/agents.yaml`) para evitar drift con la fuente canónica.
- SHOULD mantener nombres de personas alineados con los agentes legacy (ej. `license-legal` mapea a `license-legal-compliance`) para facilitar búsqueda.
- SHOULD conservar `docs/agents/multi-ide-agent-packs.md` como documentación pública actualizada con la nueva estructura y la tabla de mapeo.

## MUST NOT

- MUST NOT eliminar ninguna de las 10 reglas absolutas del proyecto.
- MUST NOT romper el flujo OpenSpec obligatorio (proposal/design/tasks/spec).
- MUST NOT permitir que un IDE quede con menos capacidades que otro (paridad total requerida).
- MUST NOT dejar skills, agentes o workflows huérfanos (no referenciados en `catalog/*`).
- MUST NOT permitir que un archivo generado se edite manualmente sin regenerar (verificado por hash).
- MUST NOT introducir dependencias externas nuevas (Jinja, cookiecutter, npm packages, etc.).
- MUST NOT modificar el modelo o proveedor IA de ningún IDE.
- MUST NOT tocar las changes OpenSpec 0009–0035 activas.
- MUST NOT borrar los 11 archivos `* 2.py` con contenido divergente de `services/api/tests/` y `services/api/alembic/` (se documentan como deuda separada).

## Escenarios verificables

1. **Sincronización limpia desde cero**: borrar `.cursor/`, `.codex/`, `.claude/`, `.opencode/`, `.github/agents/`, `.github/prompts/`, `.github/instructions/`, `docs/obsidian/agent-pack/` y ejecutar `python3 scripts/sync_agent_packs.py`. Resultado: los 6 packs regenerados idénticos al estado de referencia, sin diffs pendientes en git.
2. **Detección de drift**: modificar manualmente `.cursor/rules/mandatory-gates.mdc` y ejecutar `python3 scripts/verify_agent_packs_sync.py`. Resultado: exit code 1 y mensaje señalando el archivo divergente.
3. **CI verde en PR**: abrir un PR sin tocar `.agents/` ni packs. Resultado: workflow `agent-packs.yml` verde.
4. **CI rojo tras editar fuente sin sync**: modificar `.agents/rules/mandatory-gates.md` sin regenerar. Resultado: workflow rojo con mensaje "run sync_agent_packs.py".
5. **Presencia de 5 agentes en Copilot**: abrir chat de Copilot en VS Code. Resultado: los 5 chat modes (`spec`, `build`, `verify`, `docs`, `release`) están disponibles y ningún agente legacy aparece.
6. **Slash-commands en Claude Code**: en Claude Code, tipear `/`. Resultado: los 4 comandos (`new-spec`, `implement-task`, `verify-change`, `archive-change`) están listados.
7. **Regla gates unificada aplicada**: abrir cualquier `SKILL.md` con gates en cualquier pack IDE. Resultado: la sección de gates referencia `mandatory-gates.md` por nombre, sin duplicar texto.
8. **Legacy conservado**: `.agents/archive/agents-legacy/` contiene 25 archivos y `.agents/archive/skills-legacy/` contiene 69 directorios.
9. **`copilot-instructions.md` completo**: el archivo generado NO contiene ninguna sección truncada; incluye los pasos 6, 7, 8, 9, 10 del flujo OpenSpec desarrollados.
10. **Prompt mal ubicado migrado**: `.github/prompts/planMaterialsInboxAndPersistence.prompt.md` ya no existe; `openspec/changes/0034-materials-inbox-and-persistence/implementation-plan.md` sí existe con el mismo contenido.
