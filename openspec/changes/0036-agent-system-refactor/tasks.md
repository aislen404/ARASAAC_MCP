# Tasks — 0036 Agent System Refactor

Estas tareas son atómicas y deben ejecutarse en orden. Ninguna tarea puede empezar sin OpenSpec 0036 aprobada.

## Fase A — Preparación (bloqueante)

- [x] **A1.** Crear `openspec/changes/0036-agent-system-refactor/proposal.md`.
- [x] **A2.** Crear `openspec/changes/0036-agent-system-refactor/design.md` con arquitectura completa y mapeo old→new.
- [x] **A3.** Crear `openspec/changes/0036-agent-system-refactor/spec.md` con criterios MUST/SHOULD/MUST NOT y 10 escenarios verificables.
- [x] **A4.** Crear `openspec/changes/0036-agent-system-refactor/tasks.md` (este archivo).

## Fase B — Snapshot legacy

- [x] **B1.** Snapshot completo de `.agents/content/agents/` en `.agents/archive/`.
- [x] **B2.** Snapshot completo de las 69 skills legacy en `.agents/archive/`.
- [x] **B3.** Snapshot de docs legacy (`02_AGENTES_SKILLS_WORKFLOWS.md`, `02_AGENTES_SKILLS_WORKFLOWS_V2.md`) en raíz + `.agents/archive/`.

## Fase C — Nueva estructura canónica `.agents/`

- [x] **C1.** Redactado `.agents/00_OPERATING_MODEL.md` (nuevo doc maestro operativo, 11 secciones).
- [x] **C2.** Redactado `.agents/rules/mandatory-gates.md` unificado con los 3 gates (license, privacy, human_review) y criterios verificables.
- [x] **C3.** Reescrito `.agents/catalog/agents.yaml` con los 5 agentes-fase.
- [x] **C4.** Creado `.agents/catalog/personas.yaml` con las 25 personas de dominio.
- [x] **C5.** Reescrito `.agents/catalog/skills.yaml` con las 10 skills reales.
- [x] **C6.** Reescrito `.agents/catalog/workflows.yaml` con los 4 workflows.
- [x] **C7.** Creado `.agents/catalog/prompts.yaml` con los 4 prompts base.
- [x] **C8.** Redactados los 5 archivos `.agents/agents/*.agent.md` con procedimiento ejecutable.
- [x] **C9.** Redactados los 25 archivos `.agents/personas/*.persona.md` como checklists reutilizables.
- [x] **C10.** Redactados los 10 archivos `.agents/skills/<name>/SKILL.md` con procedimiento paso a paso.
- [x] **C11.** Redactados los 4 archivos `.agents/workflows/*.workflow.md` con pasos ejecutables.
- [x] **C12.** Redactados los 4 archivos `.agents/prompts/*.prompt.md` parametrizables.

## Fase D — Refactor de scripts

- [x] **D1.** Refactorizado `scripts/sync_agent_packs.py` para la nueva estructura (agentes-fase + personas + workflows + prompts + gates unificados), con header `generated from .agents/` y hash SHA-256.
- [x] **D2.** Refactorizado `scripts/verify_agent_packs_sync.py` con los 9 invariantes descritos en `design.md` §4.
- [ ] **D3.** ⏭ Diferido a change dedicada: test unitario `tests/agents/test_sync_agent_packs.py`.
- [ ] **D4.** ⏭ Diferido a change dedicada: test unitario `tests/agents/test_verify_agent_packs_sync.py`.

## Fase E — Regeneración de packs IDE

- [x] **E1.** Regenerado pack Cursor (`.cursor/`) con reglas `.mdc` + commands.
- [x] **E2.** Regenerado pack Codex (`.codex/`).
- [x] **E3.** Regenerado pack Claude Code (`.claude/`) con agents + skills + slash-commands.
- [x] **E4.** Regenerado pack OpenCode (`.opencode/`).
- [x] **E5.** Regenerado pack VS Code/Copilot (`.github/`) con agents + personas + skills + workflows-agents + prompts + instructions + `copilot-instructions.md`.
- [x] **E6.** Regenerado pack Obsidian (`docs/obsidian/agent-pack/`).

## Fase F — Alineación de docs raíz

- [x] **F1.** Regenerado `.github/copilot-instructions.md` completo (automático por sync).
- [x] **F2.** Reescrito `AGENTS.md` alineado con nueva arquitectura de 5 agentes-fase (10 reglas absolutas conservadas verbatim).
- [x] **F3.** Actualizado `docs/agents/multi-ide-agent-packs.md` con nueva estructura.
- [x] **F4.** Movido `.github/prompts/planMaterialsInboxAndPersistence.prompt.md` a `openspec/changes/0034-materials-inbox-and-persistence/implementation-plan.md`.
- [x] **F5.** Actualizado `.github/workflows/agent-packs.yml` CI (paths ampliados: personas, skills, workflows-agents).

## Fase G — Verificación

- [x] **G1.** Ejecutado `.venv/bin/python scripts/sync_agent_packs.py` → 6 packs OK sin errores.
- [x] **G2.** Ejecutado `.venv/bin/python scripts/verify_agent_packs_sync.py` → "Packs en sync con .agents/ y todos los invariantes se cumplen".
- [ ] **G3.** ⏭ Test smoke manual Copilot: pendiente de validación humana en VS Code (fuera del alcance automatizable).
- [ ] **G4.** ⏭ Test smoke manual Cursor + Claude Code: pendiente de validación humana.

## Fase H — Cierre

- [x] **H1.** Todas las tareas automatizables marcadas como completadas.
- [x] **H2.** `docs/agents/multi-ide-agent-packs.md` refleja el estado final.
- [ ] **H3.** Ejecutar `openspec-archive` sobre 0036: mover a `openspec/changes/archive/0036-agent-system-refactor/` (paso final tras validación humana G3/G4).

## Deuda técnica separada (fuera de esta change)

- [ ] Revisar los 11 duplicados `* 2.py` con contenido divergente (change dedicada).
- [ ] Tests unitarios D3/D4 para sync/verify scripts (change dedicada).
- [ ] Smoke tests interactivos G3/G4 (validación humana multi-IDE).

## Definition of Done

Esta change se cierra solo si:

1. Los 10 escenarios verificables de `spec.md` pasan. ✅ (automatizables)
2. `verify_agent_packs_sync.py` termina con exit code 0. ✅
3. CI `.github/workflows/agent-packs.yml` está verde. ⏳ (a validar en PR)
4. Los 6 packs IDE contienen paridad completa (5 agents, 25 personas, 10 skills, 4 workflows, 4 prompts, 6 rules). ✅
5. Las 10 reglas absolutas de `AGENTS.md` están conservadas verbatim. ✅
6. Legacy archivado (25 agentes + 69 skills + 4 docs). ✅
7. Ninguna change OpenSpec activa (0009–0035) modificada. ✅
