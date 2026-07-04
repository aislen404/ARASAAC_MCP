# ARASAAC Agents, Skills & Workflows — Cursor Pack

Migración operativa desde `.codex/` a formato nativo `.cursor/`.

## Estructura

```text
.cursor/
├── agents/          # Subagentes Cursor (*.md + YAML frontmatter)
├── skills/          # Skills y workflows (*/SKILL.md)
├── commands/        # Slash commands (/generate-task-prompt, etc.)
└── rules/           # Reglas del proyecto (*.mdc)
```

## Contenido migrado

| Tipo | Cantidad | Origen |
|------|----------|--------|
| Subagentes | 25 | `.codex/agents/*.md` + `agent_catalog.yaml` |
| Skills | 64 | `.codex/skills/skill_catalog.yaml` |
| Workflows (como skills) | 8 | `.codex/workflows/workflow_catalog.yaml` |
| Commands | 4 | `.codex/codex/*` + `prompts/codex_master_prompt.md` |
| Rules | 1 | `AGENTS.md` (reglas absolutas) |

## Uso en Cursor

- **Subagentes**: delegación automática o `/nombre-agente` (ej. `/backend`, `/openspec-steward`).
- **Skills**: descubrimiento automático o `/nombre-skill` (ej. `/create-visual-agenda`).
- **Commands**: `/generate-task-prompt`, `/review-patch`, `/create-pr-summary`, `/cursor-master-prompt`.
- **Rules**: `arasaac-platform.mdc` siempre activa (`alwaysApply: true`).

## Documento maestro

Ver `.codex/02_AGENTES_SKILLS_WORKFLOWS_V2.md` para la definición operativa completa.

## Notas de migración

- Frontmatter Codex/TOML → YAML frontmatter Cursor.
- Workflows no tienen carpeta nativa en Cursor; se modelan como skills.
- Skills `skill.codex.*` renombradas a dominio `cursor-*` (ej. `cursor-generate-task-prompt`).
- Workflow `development_openspec_codex` → skill `development-openspec-cursor`.
- `.codex/` se conserva como fuente histórica; `.cursor/` es el pack activo para Cursor IDE.
