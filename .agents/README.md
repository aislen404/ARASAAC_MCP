# ARASAAC Agent Pack — Fuente canónica

Capa **IDE-neutral** compartida por todo el equipo. Los packs por IDE se **generan** desde aquí.

## Principio

> Mismas capacidades agenticas para todos; distinto frontmatter/ruta según el IDE.

## Estructura

```text
.agents/
├── catalog/           # YAML: agents, skills, workflows, packs
├── content/           # Cuerpos markdown neutros (sin marca de IDE)
├── rules/             # Reglas por dominio
├── skills/            # Skills portables (estándar Agent Skills / agentskills.io)
└── 02_AGENTES_SKILLS_WORKFLOWS_V2.md
```

## Packs generados

| IDE / herramienta | Ruta | Uso |
|-------------------|------|-----|
| **Portable** | `.agents/skills/` | Cursor, Claude, OpenCode, Copilot |
| Cursor | `.cursor/` | Subagentes, rules `.mdc`, commands |
| Codex | `.codex/` | Agents `.toml` + compat `.md` |
| Claude Code | `.claude/` | Subagentes + skills + commands |
| OpenCode | `.opencode/` | Skills + agents |
| VS Code / Copilot | `.github/` | `copilot-instructions.md`, `.agent.md` |
| Obsidian | `docs/obsidian/agent-pack/` | Navegación humana, wikilinks |

## Regenerar

```bash
make agent-packs-sync
# equivalente: python3 scripts/sync_agent_packs.py
```

## Verificar sincronía

```bash
make agent-packs-verify
# equivalente: python3 scripts/verify_agent_packs_sync.py
```

El CI (`.github/workflows/agent-packs.yml`) ejecuta la verificación en PRs y en
`main` cuando cambian rutas de agent packs.

Guía completa: [docs/agents/multi-ide-agent-packs.md](../docs/agents/multi-ide-agent-packs.md).

## Conteos actuales

- Agentes: 25
- Skills: 72
- Workflows: 8
