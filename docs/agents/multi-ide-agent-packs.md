# Packs agenticos multi-IDE

Este documento describe cómo mantener **paridad de capacidades agenticas** entre
Cursor, Codex, Claude Code, OpenCode, VS Code / GitHub Copilot y Obsidian.

## Fuente canónica

Editar **solo** en `.agents/`:

| Ruta | Qué contiene |
|------|----------------|
| `.agents/catalog/` | Catálogos YAML (`agents`, `skills`, `workflows`, `packs`) |
| `.agents/content/` | Cuerpos markdown IDE-neutral (agentes, prompts, plantillas) |
| `.agents/rules/` | Reglas por dominio (`platform`, `backend`, `frontend`, `mcp`, `export-license`) |
| `.agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md` | Definición operativa maestra |

No editar manualmente los packs generados (`.cursor/`, `.codex/`, `.claude/`,
`.opencode/`, partes de `.github/` ni `docs/obsidian/agent-pack/`).

## Regenerar packs

```bash
make agent-packs-sync
# equivalente:
python3 scripts/sync_agent_packs.py
```

## Verificar sincronía (local o CI)

```bash
make agent-packs-verify
# equivalente:
python3 scripts/verify_agent_packs_sync.py
```

El verificador ejecuta el sync y comprueba que no haya diff en rutas generadas.
En pull requests y pushes a `main` que toquen agent packs, GitHub Actions ejecuta
el workflow `.github/workflows/agent-packs.yml`.

## Packs por herramienta

| Herramienta | Ruta | Formato |
|-------------|------|---------|
| Portable (todos) | `.agents/skills/` | Agent Skills (`SKILL.md`) |
| Cursor | `.cursor/` | Subagentes YAML, rules `.mdc`, commands |
| Codex | `.codex/` | Agents `.toml` + compat `.md` |
| Claude Code | `.claude/` | Subagentes, skills, commands |
| OpenCode | `.opencode/` | Skills + agents |
| VS Code / Copilot | `.github/` | `copilot-instructions.md`, `.agent.md`, `.instructions.md` |
| Obsidian | `docs/obsidian/agent-pack/` | Vault con wikilinks (referencia humana) |

## Flujo recomendado para el equipo

1. Cambiar catálogo o contenido en `.agents/`.
2. Ejecutar `make agent-packs-sync`.
3. Revisar diff de packs generados.
4. Ejecutar `make agent-packs-verify` antes de commit.
5. Commit incluyendo cambios en `.agents/` **y** packs generados.

## Limpieza post-sync

Si iCloud/Dropbox crea copias de conflicto (`* 2.md`, `* 3.toml`, etc.):

```bash
find .codex docs/obsidian \( -name '* 2.*' -o -name '* 3.*' \) -type f -delete
```

Esos patrones están en `.gitignore`. No editar manualmente archivos con sufijo numérico.


- **Reglas globales:** `AGENTS.md` + `.agents/rules/platform.md` → always-on.
- **Reglas scoped:** backend, frontend, mcp, export-license con globs por IDE.
- **Agentes readonly:** QA, licencia, privacidad, ARASAAC liaison.
- **Skills críticos:** dominios `export` y `validate` requieren invocación manual en Cursor.

## Referencias

- [AGENTS.md](../../AGENTS.md) — reglas vinculantes del repositorio
- [.agents/README.md](../../.agents/README.md) — índice de la fuente canónica
- [.agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md](../../.agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md) — catálogo operativo completo
