# Design — 0036 Agent System Refactor

## Principio rector

**Un IDE solo ofrece al usuario lo que puede ejecutar; todo lo demás es contexto interno.**
Los agentes-fase son el único punto de selección visible; las personas, skills, reglas y gates viven por debajo como piezas invocables por los agentes o referenciadas por frontmatter. Nada se selecciona manualmente si puede resolverse por convención (globs, fase OpenSpec, tipo de material).

## Estado actual

### Fuente canónica `.agents/`

```
.agents/
├── 00_MASTER_INDEX.md
├── 01_INTRODUCCION_AGENTES_Y_SKILLS.md
├── 02_AGENTES_SKILLS_WORKFLOWS_V2.md   # doc extenso, descriptivo, no operativo
├── 02_AGENTES_SKILLS_WORKFLOWS.md      # versión previa
├── catalog/
│   ├── agents.yaml       # 25 agentes-rol con misiones solapadas
│   ├── skills.yaml       # 69 skills, mayoría plantillas huecas
│   ├── workflows.yaml    # 8 workflows como listas de tags
│   └── packs.yaml        # OK: 6 IDE targets
├── content/
│   └── agents/           # 25 .md, uno por agente
├── rules/
│   ├── platform.md
│   ├── backend.md
│   ├── frontend.md
│   ├── mcp.md
│   └── export-license.md
└── skills/
    └── <69 dirs>/SKILL.md   # cada uno con frontmatter + gates repetidos
```

### Packs derivados

`scripts/sync_agent_packs.py` genera:
- `.cursor/rules/` + `.cursor/skills/`
- `.codex/` (agentes + skills como md)
- `.claude/agents/` + `.claude/skills/` + `.claude/commands/` (parcial)
- `.opencode/` (equivalente)
- `.github/agents/` + `.github/instructions/` + `.github/prompts/` + `.github/copilot-instructions.md`
- `docs/obsidian/agent-pack/`

### Problemas medibles

| Métrica | Valor actual | Objetivo |
|---------|--------------|----------|
| Agentes seleccionables por IDE | 25 | 5 |
| Skills totales | 69 | ~10 |
| Workflows | 8 (YAML tags) | 4 (`.md` ejecutables) |
| Prompts base | 0 canónicos + 1 mal ubicado | 4 |
| Gates duplicados | ~5 líneas × 69 skills × 5 IDEs ≈ 1.725 líneas | 1 archivo canónico |
| Doc maestro operativo | No (V2 es descriptivo) | Sí (`00_OPERATING_MODEL.md`) |

## Cambio propuesto

### 1. Nueva estructura `.agents/` objetivo

```
.agents/
├── 00_OPERATING_MODEL.md        # NUEVO doc maestro operativo
├── README.md                    # índice mínimo
├── catalog/
│   ├── agents.yaml              # 5 agentes-fase
│   ├── personas.yaml            # NUEVO: 15 personas de dominio
│   ├── skills.yaml              # ~10 skills reales
│   ├── workflows.yaml           # 4 workflows (1 canónico + 3 negocio)
│   ├── prompts.yaml             # NUEVO: 4 prompts base
│   └── packs.yaml               # OK, sin cambios estructurales
├── agents/                      # NUEVO (reemplaza content/agents/)
│   ├── spec.agent.md
│   ├── build.agent.md
│   ├── verify.agent.md
│   ├── docs.agent.md
│   └── release.agent.md
├── personas/                    # NUEVO: 15 checklists reutilizables
│   ├── license-legal.persona.md
│   ├── privacy-ethics.persona.md
│   ├── a11y-cognitive.persona.md
│   ├── caasaac-methodology.persona.md
│   ├── arasaac-liaison.persona.md
│   ├── solution-architect.persona.md
│   ├── backend.persona.md
│   ├── frontend.persona.md
│   ├── mcp-architect.persona.md
│   ├── data-connector.persona.md
│   ├── semantic-search.persona.md
│   ├── export-document.persona.md
│   ├── devops.persona.md
│   ├── qa.persona.md
│   ├── accessibility-qa.persona.md
│   ├── test-automation.persona.md
│   ├── security.persona.md
│   ├── observability.persona.md
│   ├── documentation.persona.md
│   ├── easy-reading.persona.md
│   ├── ux-accessibility.persona.md
│   ├── release-manager.persona.md
│   ├── openspec-steward.persona.md
│   ├── product-owner-social.persona.md
│   └── ngo-cee-domain.persona.md
├── skills/                      # ~10 dirs con SKILL.md real
│   ├── openspec-lifecycle/SKILL.md
│   ├── openspec-archive/SKILL.md
│   ├── arasaac-fetch/SKILL.md
│   ├── mcp-tool-scaffold/SKILL.md
│   ├── material-pipeline/SKILL.md
│   ├── export-with-manifest/SKILL.md
│   ├── human-review-gate/SKILL.md
│   ├── compliance-scan/SKILL.md
│   ├── a11y-audit/SKILL.md
│   └── docs-generate/SKILL.md
├── workflows/                   # NUEVO: 4 .md ejecutables
│   ├── spec-build-verify.workflow.md
│   ├── create-visual-agenda.workflow.md
│   ├── create-communication-board.workflow.md
│   └── create-easy-reading.workflow.md
├── prompts/                     # NUEVO: 4 prompts base
│   ├── new-spec.prompt.md
│   ├── implement-task.prompt.md
│   ├── verify-change.prompt.md
│   └── archive-change.prompt.md
├── rules/
│   ├── mandatory-gates.md       # NUEVO unificado (license/privacy/human-review)
│   ├── platform.md              # ligeramente reescrito
│   ├── backend.md
│   ├── frontend.md
│   ├── mcp.md
│   └── export-license.md
└── archive/                     # snapshot legacy
    ├── agents-legacy/           # 25 .md originales
    ├── skills-legacy/           # 69 SKILL.md originales
    └── docs-legacy/             # V2, V1, master_index, introducción
```

Nota: el número exacto de personas (25 arriba) refleja que **todas** las responsabilidades actuales se preservan como checklists; la reducción operativa es "5 agentes seleccionables invocando N personas por dentro", no "eliminar personas".

### 2. Contrato de cada tipo de archivo

**Agente-fase (`.agents/agents/*.agent.md`)**

```yaml
---
name: spec
title: Spec Agent
phase: spec
invokes_personas:
  - license-legal
  - privacy-ethics
  - a11y-cognitive
  - caasaac-methodology
  - arasaac-liaison
  - solution-architect
uses_skills:
  - openspec-lifecycle
  - compliance-scan
uses_workflows:
  - spec-build-verify
mandatory_gates: [license, privacy, human_review]
---

## Cuándo invocarme
## Procedimiento
## Salida esperada
## Criterios de éxito
## Errores comunes
```

**Persona (`.agents/personas/*.persona.md`)**

```yaml
---
name: license-legal
role: License & Legal Compliance
scope: [export, material, arasaac]
gates_enforced: [license]
---

## Checklist obligatoria
## Preguntas que debo hacer
## Bloqueos que debo levantar
```

**Skill (`.agents/skills/*/SKILL.md`)**

```yaml
---
name: openspec-lifecycle
description: Crear, validar y evolucionar una change OpenSpec.
inputs:
  - change_id
  - problem_statement
outputs:
  - openspec/changes/<id>/{proposal,design,tasks,spec}.md
gates: []
---

## Procedimiento paso a paso
1. …
2. …

## Ejemplos
## Errores comunes
```

**Workflow (`.agents/workflows/*.workflow.md`)**

```yaml
---
name: spec-build-verify
kind: canonical
uses_agents: [spec, build, verify, docs, release]
---

## Paso 1 — spec
## Paso 2 — build
## Paso 3 — verify
## Paso 4 — docs
## Paso 5 — release
```

**Prompt (`.agents/prompts/*.prompt.md`)**

```yaml
---
name: new-spec
invokes_agent: spec
parameters:
  - change_id
  - short_title
---
Actúa como spec-agent y crea la change {{change_id}}-{{short_title}} …
```

### 3. Mapeo old → new

**Agentes (25 → 5 + personas)**

| Agente legacy | Nuevo destino |
|---------------|---------------|
| product-owner-social | persona (invocada por spec + release) |
| accessibility-qa | persona (invocada por verify) |
| arasaac-liaison | persona (invocada por spec + docs) |
| backend | persona (invocada por build) |
| caasaac-methodology | persona (invocada por spec) |
| cognitive-accessibility → a11y-cognitive | persona (invocada por spec + verify + docs) |
| data-connector | persona (invocada por build) |
| devops | persona (invocada por build + release) |
| documentation | persona (invocada por docs) |
| easy-reading | persona (invocada por docs) |
| export-document | persona (invocada por build) |
| frontend | persona (invocada por build) |
| license-legal-compliance → license-legal | persona (invocada por spec + verify) |
| mcp-architect | persona (invocada por spec + build) |
| ngo-cee-domain | persona (invocada por spec) |
| observability | persona (invocada por verify) |
| openspec-steward | persona (invocada por spec + release) |
| privacy-ethics | persona (invocada por spec + verify) |
| qa | persona (invocada por verify) |
| release-manager | persona (invocada por release) |
| security | persona (invocada por verify) |
| semantic-search | persona (invocada por build) |
| solution-architect | persona (invocada por spec) |
| test-automation | persona (invocada por verify) |
| ux-accessibility | persona (invocada por docs) |

**Skills (69 → 10)**

| Cluster de skills legacy | Nueva skill |
|---|---|
| openspec-create-change, openspec-split-tasks, openspec-detect-dependency-conflicts, openspec-validate-acceptance-criteria, development-openspec | `openspec-lifecycle` |
| openspec-archive-change | `openspec-archive` |
| arasaac-query-api, arasaac-get-pictogram, arasaac-cache-reference, arasaac-normalize-metadata, arasaac-generate-manifest-entry, arasaac-validate-real-id, arasaac-handle-api-error | `arasaac-fetch` |
| mcp-define-tool-schema, mcp-implement-tool, mcp-define-resource, mcp-define-prompt, mcp-validate-tool-security, mcp-write-contract-test | `mcp-tool-scaffold` |
| create-visual-agenda, create-communication-board, easy-reading-document, cee-conacee-kit, cermi-foundation-kit, material-create-* (todas) | `material-pipeline` (los "create-*" pasan además a ser **workflows** de negocio) |
| export-generate-pdf/docx/pptx/html/images, export-package-zip, export-attach-manifest, export-render-html | `export-with-manifest` |
| review-approve-material, review-reject-material, review-request-human-review | `human-review-gate` |
| validate-license-notice-visible, validate-no-modified-pictograms, validate-non-commercial-context, validate-no-personal-data, validate-pictogram-ids-real, validate-visual-density, validate-plain-language, validate-sequence-coherence, validate-export-readiness, validate-human-review-approved | `compliance-scan` |
| a11y-review-cognitive-accessibility, a11y-test-color-independence, a11y-test-focus-order, a11y-test-keyboard-navigation, a11y-test-labels | `a11y-audit` |
| docs-generate-readme, docs-generate-technical-manual, docs-generate-deployment-guide, docs-generate-contribution-guide, docs-generate-release-notes, docs-generate-entity-manual, docs-generate-arasaac-validation-dossier | `docs-generate` |
| editor-adjust-layout, editor-reorder-steps, editor-replace-pictogram, editor-update-text-block | absorbidas por `material-pipeline` |
| agent-create-pr-summary, agent-generate-task-prompt, agent-review-patch | absorbidas por prompts `implement-task` y `verify-change` |

**Workflows (8 → 4)**

| Legacy | Nuevo |
|--------|-------|
| development-openspec | `spec-build-verify.workflow.md` (canónico) |
| create-visual-agenda | `create-visual-agenda.workflow.md` |
| create-communication-board | `create-communication-board.workflow.md` |
| easy-reading-document | `create-easy-reading.workflow.md` |
| cee-conacee-kit, cermi-foundation-kit | absorbidos como variantes de `material-pipeline` (fuera del set de workflows top-level) |

### 4. Refactor de scripts

**`scripts/sync_agent_packs.py`** — cambios:

- Nueva función `load_catalog()` que lee `agents.yaml`, `personas.yaml`, `skills.yaml`, `workflows.yaml`, `prompts.yaml`, `packs.yaml`.
- Nueva sección de generación por IDE con **el mismo contrato de invariantes** por pack:
  - `AGENTS/` (5 archivos por IDE).
  - `PERSONAS/` (15 archivos por IDE, presentados como referencia).
  - `SKILLS/<name>/SKILL.md` (~10 por IDE).
  - `WORKFLOWS/*.md` (4 por IDE).
  - `PROMPTS/*.md` (4 por IDE) o slash-commands en Cursor/Claude/OpenCode.
  - `RULES/mandatory-gates.md` + reglas de dominio.
- Formato específico por IDE:
  - **Cursor**: `.cursor/rules/*.mdc` para reglas + `.cursor/commands/*.md` para prompts (formato Cursor Commands).
  - **Codex**: `.codex/agents/`, `.codex/skills/`, `.codex/prompts/`.
  - **Claude Code**: `.claude/agents/`, `.claude/skills/`, `.claude/commands/` (slash-commands nativos).
  - **OpenCode**: `.opencode/agents/`, `.opencode/skills/`, `.opencode/commands/`.
  - **VS Code/Copilot**: `.github/agents/*.agent.md` (chat modes), `.github/prompts/*.prompt.md` (comandos `/name`), `.github/instructions/*.instructions.md` con `applyTo`, `.github/copilot-instructions.md` regenerado desde template.
  - **Obsidian**: `docs/obsidian/agent-pack/` con notas linkeables (mismo contenido, formato humano).
- Todos los archivos generados llevan header `<!-- generated from .agents/ — do not edit manually -->` y hash SHA-256 del contenido fuente en frontmatter para verificación.

**`scripts/verify_agent_packs_sync.py`** — nuevos invariantes:

1. `.agents/catalog/agents.yaml` tiene exactamente 5 entradas, todas con archivo `.agents/agents/<name>.agent.md`.
2. `.agents/catalog/personas.yaml` referencia solo archivos existentes en `.agents/personas/`.
3. `.agents/catalog/skills.yaml` tiene exactamente los directorios listados en `.agents/skills/` (sin huérfanos).
4. `.agents/catalog/workflows.yaml` tiene 4 entradas, todas `.md` en `.agents/workflows/`.
5. `.agents/catalog/prompts.yaml` tiene 4 entradas, todas `.md` en `.agents/prompts/`.
6. Cada pack IDE contiene N agentes, N personas, N skills, N workflows, N prompts según su matriz (definida en `packs.yaml`).
7. Cada archivo generado tiene el hash correcto vs su fuente canónica.
8. `mandatory-gates.md` es referenciado desde frontmatter por ≥ 1 agente y ≥ 1 skill (verificando que no queda huérfano).
9. Ningún archivo legacy queda fuera de `.agents/archive/`.

### 5. Contrato del `copilot-instructions.md` regenerado

El template canónico vive en `.agents/00_OPERATING_MODEL.md` y `sync_agent_packs.py` lo compone así:

```md
# ARASAAC Social MCP Platform — Instrucciones Copilot

## Reglas absolutas       # ← desde rules/mandatory-gates.md
## Flujo obligatorio      # ← desde workflows/spec-build-verify.workflow.md
  - Paso 1: /new-spec …
  - Paso 2: /implement-task …
  - Paso 3: /verify-change …
  - Paso 4: /archive-change …
## Agentes-fase           # ← desde catalog/agents.yaml
## Prompts disponibles    # ← desde catalog/prompts.yaml
## Reglas por área        # ← desde rules/*.md como instructions con applyTo
## Referencias            # ← AGENTS.md, docs/agents/, packs de otros IDEs
```

### 6. Movimientos y limpieza

- `.github/prompts/planMaterialsInboxAndPersistence.prompt.md` → `openspec/changes/0034-materials-inbox-and-persistence/implementation-plan.md` (no es un prompt, es un plan de fases de esa change).
- 25 archivos en `.agents/content/agents/` → `.agents/archive/agents-legacy/`.
- 69 dirs en `.agents/skills/` (todos los que no coincidan con el nuevo set de 10) → `.agents/archive/skills-legacy/`.
- `.agents/02_AGENTES_SKILLS_WORKFLOWS.md`, `02_AGENTES_SKILLS_WORKFLOWS_V2.md`, `00_MASTER_INDEX.md`, `01_INTRODUCCION_AGENTES_Y_SKILLS.md` → `.agents/archive/docs-legacy/`.

## Alternativas descartadas

- **Mantener los 25 agentes-rol y solo consolidar skills**: no elimina la fricción de selección; el usuario seguiría preguntando "¿backend o mcp-architect?".
- **Reducir todo a 1 agente universal**: pierde la capacidad de aplicar `applyTo`/globs por fase; el LLM tendería a mezclar responsabilidades y saltarse gates.
- **Migrar todos los IDEs a un solo formato (ej. solo Claude Skills)**: cada IDE tiene convenciones nativas (chat modes en Copilot, commands en Cursor, slash-commands en Claude). Homogeneizar rompe UX nativa.
- **Reemplazar `sync_agent_packs.py` por Jinja/Cookiecutter externo**: añade dependencia sin ganancia; el script actual es autocontenido y basta con refactor.

## Riesgos

| Riesgo | Mitigación |
|--------|-----------|
| Perder trazabilidad de responsabilidades legacy. | Snapshot completo en `.agents/archive/` + tabla de mapeo en este design. |
| Romper packs IDE de un usuario a mitad de sesión. | Cambio big-bang en un único PR; regenerar todos los packs en el mismo commit; anunciar en release notes. |
| El usuario espera un agente concreto (ej. "security") y no lo ve. | `verify` invoca la persona `security` internamente; documentar en `00_OPERATING_MODEL.md` la tabla persona↔agente. |
| Gates unificados desincronizados con AGENTS.md. | `mandatory-gates.md` es la fuente; `AGENTS.md` se regenera desde este archivo en el mismo sync. |
| CI `agent-packs.yml` falla tras el refactor. | Actualizar invariantes en `verify_agent_packs_sync.py` como parte del mismo PR. |
| Duplicados divergentes `* 2.py` en tests siguen contaminando el repo. | Documentar como deuda separada (fuera de esta change); no bloquear el refactor por eso. |

## Impacto en tests

- Nuevo test unitario para `sync_agent_packs.py` que valide la generación de un pack de prueba en un tmpdir.
- Nuevo test unitario para `verify_agent_packs_sync.py` con un fixture "drifted" que debe fallar.
- Smoke test manual documentado en `tasks.md` (Copilot + Cursor + Claude Code).
- CI `.github/workflows/agent-packs.yml` extendido para correr sync + verify + los tests unitarios nuevos.
