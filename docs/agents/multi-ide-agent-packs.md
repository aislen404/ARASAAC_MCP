# Packs agenticos multi-IDE

Este documento describe cómo trabajamos con **una sola fuente canónica** de configuración agentica (`.agents/`) que se materializa automáticamente en packs específicos para cada IDE / cliente de IA usado en el proyecto.

## Objetivo

Que todos los entornos (Cursor, Codex, Claude Code, OpenCode, VS Code/GitHub Copilot, Obsidian como referencia humana) tengan **exactamente la misma capa de reglas, agentes-fase, personas de dominio, skills, workflows y prompts**, sin drift, sin duplicación manual y con CI que garantice la paridad.

## Arquitectura

```
.agents/                          ← fuente canónica (editar solo aquí)
├── 00_OPERATING_MODEL.md         ← modelo operativo completo
├── agents/                       ← 5 agentes-fase: spec, build, verify, docs, release
├── personas/                     ← 25 personas de dominio (.persona.md)
├── skills/                       ← 10 skills reales (procedimientos ejecutables)
├── workflows/                    ← 4 workflows (1 canónico OpenSpec + 3 negocio)
├── prompts/                      ← 4 prompts parametrizables (slash commands)
├── rules/                        ← reglas globales + gates críticos + reglas por área
└── catalog/                      ← YAML descriptivo (fuente de verdad de contadores)

Packs generados (NO editar a mano)
├── .cursor/                      ← Cursor
├── .codex/                       ← Codex CLI
├── .claude/                      ← Claude Code
├── .opencode/                    ← OpenCode
├── .github/                      ← VS Code + GitHub Copilot
│   ├── agents/  personas/  skills/  workflows-agents/
│   ├── prompts/  instructions/
│   └── copilot-instructions.md
└── docs/obsidian/agent-pack/     ← Obsidian (referencia humana)
```

## Contadores de paridad (invariantes)

Cada IDE debe contener exactamente:

| Elemento | Cantidad |
|----------|----------|
| Agentes-fase | 5 |
| Personas | 25 |
| Skills | 10 |
| Workflows | 4 |
| Prompts / slash commands | 4 |
| Reglas | 6 |

El script `verify_agent_packs_sync.py` comprueba estos contadores más otros invariantes estructurales (I1–I9) y hace `git diff --quiet` sobre los directorios generados. Cualquier drift falla el CI.

## Herramientas

Script | Uso
--- | ---
`scripts/sync_agent_packs.py` | Regenera los 6 packs desde `.agents/`. Idempotente.
`scripts/verify_agent_packs_sync.py` | Verifica invariantes + ausencia de diffs.

Ambos requieren `pyyaml`. Usa `.venv/bin/python` en local; en CI se instala automáticamente.

## Convenciones de generación

- Cada archivo generado incluye cabecera canónica:
  ```
  <!-- generated from .agents/ — do not edit manually -->
  <!-- source-hash: XXXXXXXXXXXX -->
  ```
- El `source-hash` (SHA-256, 12 primeros chars) permite detectar re-generación.
- Los prompts se materializan según convención de cada IDE (`.cursor/commands/`, `.codex/prompts/`, `.claude/commands/`, `.opencode/prompts/`, `.github/prompts/`).
- Las reglas se materializan como `.mdc` (Cursor), `.md` (Codex/Claude/OpenCode) o `*.instructions.md` con `applyTo` (VS Code Copilot).

## Flujo de trabajo

1. Editar cualquier archivo dentro de `.agents/`.
2. Ejecutar `make agent-packs-sync` (o el script directamente).
3. Verificar con `make agent-packs-verify`.
4. Commitear `.agents/` **y** los packs generados en el mismo commit.
5. El CI (`.github/workflows/agent-packs.yml`) volverá a verificar en PR.

## Gates críticos

Los 3 gates críticos del proyecto (`license`, `privacy`, `human_review`) tienen texto único en `.agents/rules/mandatory-gates.md`. Cualquier agente / skill / workflow los **referencia por nombre**; nunca duplica el texto. El sync copia ese archivo tal cual a cada pack.

## Personas invocadas por agentes

Las 25 personas de dominio **no son seleccionables** en la UI de ningún IDE. Los 5 agentes-fase las invocan internamente según necesidad (ej. el agente `verify` invoca `license-legal`, `privacy-ethics`, `qa`, `accessibility-qa`). Esto simplifica la elección para el usuario y mantiene consistencia entre herramientas.

## Prompts parametrizables

Los 4 prompts son la superficie de entrada más habitual:

- `/new-spec` → invoca agente `spec`.
- `/implement-task` → invoca agente `build`.
- `/verify-change` → invoca agente `verify`.
- `/archive-change` → invoca agente `release`.

Cada uno se materializa en el formato nativo de slash command de cada IDE.

## Referencias

- `.agents/00_OPERATING_MODEL.md` — filosofía y detalle completo.
- `AGENTS.md` §11 — resumen operativo.
- `.github/workflows/agent-packs.yml` — CI.
