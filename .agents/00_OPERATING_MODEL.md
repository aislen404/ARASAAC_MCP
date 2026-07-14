# ARASAAC Social MCP Platform — Modelo Operativo Agentico

> Fuente canónica única para las capacidades agenticas del proyecto.
> Todos los packs por IDE (`.cursor/`, `.codex/`, `.claude/`, `.opencode/`, `.github/`, `docs/obsidian/agent-pack/`) se generan desde aquí. **No editar los packs manualmente.**

## 1. Filosofía

Un solo modelo mental para 6 entornos IDE:

- **5 agentes-fase** que reflejan el ciclo OpenSpec → producción.
- **25 personas** de dominio que los agentes invocan internamente (no aparecen en la UI).
- **10 skills** con procedimiento ejecutable paso-a-paso.
- **4 workflows** (1 canónico + 3 de negocio).
- **4 prompts** parametrizables (slash-commands).
- **3 gates críticos** unificados en `rules/mandatory-gates.md`.

## 2. Los 5 agentes-fase

| Agente | Fase | Cuándo invocar | Slash-command principal |
|---|---|---|---|
| `spec` | Diseño | Necesidad nueva sin change OpenSpec | `/new-spec` |
| `build` | Implementación | Task atómica en change aprobada | `/implement-task` |
| `verify` | Validación | Todas las tasks cerradas | `/verify-change` |
| `docs` | Documentación | Cambios visibles al usuario/dev | (implícito tras verify) |
| `release` | Cierre | Verify OK + docs OK | `/archive-change` |

Ver: `.agents/agents/*.agent.md`

## 3. Personas de dominio (invocación interna)

25 personas agrupadas por rol. **No son seleccionables en la UI** — los agentes las abren como checklist mental.

| Grupo | Personas |
|---|---|
| Producto / Dominio social | product-owner-social, ngo-cee-domain, caasaac-methodology, a11y-cognitive, arasaac-liaison |
| Compliance / Legal / Seguridad | license-legal, privacy-ethics, security |
| Arquitectura / Implementación | solution-architect, mcp-architect, backend, frontend, data-connector, semantic-search, export-document, devops |
| Calidad / Verificación | qa, accessibility-qa, test-automation, observability |
| Documentación / UX | documentation, easy-reading, ux-accessibility |
| Gobernanza / Release | openspec-steward, release-manager |

Cada persona = archivo `.agents/personas/<name>.persona.md` con:
- Preguntas que debe hacer.
- Bloqueos que debe levantar.
- Checklist obligatoria.

## 4. Skills (procedimiento ejecutable)

10 skills que consolidan las 69 skills legacy:

| Skill | Invocada por | Gates |
|---|---|---|
| `openspec-lifecycle` | spec, build | — |
| `openspec-archive` | release | — |
| `arasaac-fetch` | build | license |
| `mcp-tool-scaffold` | build | — |
| `material-pipeline` | build | license, privacy, human_review |
| `export-with-manifest` | build | license |
| `human-review-gate` | verify | human_review |
| `compliance-scan` | spec, verify | license, privacy |
| `a11y-audit` | verify | — |
| `docs-generate` | docs, release | — |

Cada skill = directorio `.agents/skills/<name>/SKILL.md` con procedimiento paso-a-paso, ejemplos y errores comunes.

## 5. Workflows

1. **`spec-build-verify`** (canónico) — obligatorio en toda change.
2. **`create-visual-agenda`** (negocio) — agenda visual accesible.
3. **`create-communication-board`** (negocio) — tablero CAA/SAAC.
4. **`create-easy-reading`** (negocio) — adaptación a lectura fácil.

Ver: `.agents/workflows/*.workflow.md`

## 6. Prompts (slash-commands)

4 prompts que aterrizan como slash-commands en cada IDE:

| Prompt | Invoca | Comando |
|---|---|---|
| `new-spec` | `spec` | `/new-spec <id> <title> <problem>` |
| `implement-task` | `build` | `/implement-task <id> <task>` |
| `verify-change` | `verify` | `/verify-change <id>` |
| `archive-change` | `release` | `/archive-change <id>` |

## 7. Gates críticos (fuente única)

Los 3 gates viven en `.agents/rules/mandatory-gates.md`:

- **`license`** — CC BY-NC-SA + atribución visible + no modificación de pictogramas + no IA imitando estilo.
- **`privacy`** — sin PII + no vinculación material↔persona + logs limpios.
- **`human_review`** — reviewer humano identificado + separación autor/reviewer + versión hash congelada.

Cada agente/skill declara qué gates aplica vía frontmatter `gates: [...]`.

## 8. Mapeo legacy → nuevo

| Legacy (v1) | Nuevo (v2) | Notas |
|---|---|---|
| 25 agentes (`content/agents/*.md`) | 5 agentes-fase + 25 personas | Agentes = fase del ciclo; personas = checklist interna |
| 69 skills (`skills/*/SKILL.md`) | 10 skills consolidadas | Ver design 0036 §3 para mapping detallado |
| 8 workflows | 4 workflows | 1 canónico + 3 de negocio |
| Doc `02_AGENTES_SKILLS_WORKFLOWS_V2.md` | Este archivo (`00_OPERATING_MODEL.md`) | Legacy archivado en `.agents/archive/docs-legacy/` |

Backup completo del legacy: `.agents/archive/`.

## 9. Regeneración de packs

Tras editar cualquier fuente canónica:

```bash
python3 scripts/sync_agent_packs.py       # regenera .cursor/, .codex/, .claude/, .opencode/, .github/, docs/obsidian/agent-pack/
python3 scripts/verify_agent_packs_sync.py  # confirma zero drift
# equivalentes:
make agent-packs-sync
make agent-packs-verify
```

CI lo comprueba en `.github/workflows/agent-packs.yml`.

## 10. Estructura de `.agents/`

```
.agents/
├── 00_OPERATING_MODEL.md          ← este archivo
├── agents/                         ← 5 agentes-fase
│   ├── spec.agent.md
│   ├── build.agent.md
│   ├── verify.agent.md
│   ├── docs.agent.md
│   └── release.agent.md
├── personas/                       ← 25 personas (checklists)
│   └── *.persona.md
├── skills/                         ← 10 skills (procedimiento)
│   └── <skill-name>/SKILL.md
├── workflows/                      ← 4 workflows
│   └── *.workflow.md
├── prompts/                        ← 4 prompts (slash-commands)
│   └── *.prompt.md
├── rules/                          ← reglas por área
│   ├── mandatory-gates.md          ← FUENTE ÚNICA de los 3 gates
│   ├── backend.md
│   ├── frontend.md
│   ├── mcp.md
│   ├── export-license.md
│   └── platform.md
├── catalog/                        ← manifests YAML
│   ├── agents.yaml
│   ├── personas.yaml
│   ├── skills.yaml
│   ├── workflows.yaml
│   ├── prompts.yaml
│   └── packs.yaml                  ← targets de cada IDE
└── archive/                        ← backup legacy (no editar)
    ├── agents-legacy/
    ├── skills-legacy/
    ├── docs-legacy/
    └── catalog-legacy/
```

## 11. Referencias

- Reglas del proyecto: `AGENTS.md` (raíz)
- Change OpenSpec de este refactor: `openspec/changes/0036-agent-system-refactor/`
- Docs multi-IDE: `docs/agents/multi-ide-agent-packs.md`
