# Proposal — 0036 Agent System Refactor

## Problema

El sistema agentico actual introduce fricción operativa continua en todos los IDEs (Cursor, Codex, Claude Code, OpenCode, VS Code/Copilot y Obsidian). El diagnóstico realizado en la fuente canónica `.agents/` y en los packs derivados muestra:

- **25 agentes-rol** con misiones fuertemente solapadas (backend/frontend/mcp/data/security/qa/…) que obligan al usuario a decidir "qué agente uso" en cada paso, cuando en la práctica un mismo flujo de implementación los invoca a todos.
- **69 skills** de las cuales la gran mayoría son plantillas huecas con el mismo bloque *"Entradas / Salida / Gates"* repetido palabra por palabra; existen además duplicados evidentes (`create-visual-agenda` vs `material-create-visual-agenda`, `export-readiness` vs `validate-export-readiness`, etc.). Al replicarse en 5 packs IDE, generan cientos de archivos sin procedimiento accionable.
- **8 workflows** definidos como listas de tags en YAML que se renderizan como `SKILL.md` igual de vacíos, sin instrucciones ejecutables.
- **`copilot-instructions.md` truncado** en el paso 6 del flujo OpenSpec, sin describir qué hace cada paso ni cómo el agente debe encadenarlos.
- **Prompts sueltos con nomenclatura incoherente** (`planMaterialsInboxAndPersistence.prompt.md` alojado en `.github/prompts/` es en realidad un plan de 15 fases de la change 0034, no un template reutilizable).
- **Duplicación multi-IDE mecánica**: cada skill/agente vacío se replica ×5, amplificando el ruido y disparando confirmaciones/selecciones innecesarias.
- **Cero flujos end-to-end invocables**: no existe un único comando/prompt que traduzca *necesidad social → OpenSpec → implementación → verificación → cierre*. Todo requiere que el humano encadene decisiones manualmente.

La causa raíz es un sistema diseñado para **seleccionar y confirmar** en vez de para **ejecutar flujos consistentes**. Los IDEs preguntan "¿qué agente uso?" porque hay 25 con misiones casi idénticas, y las skills no describen *cómo* hacer nada, solo declaran qué gates cumplir.

## Cambio propuesto

Refactorizar el sistema agentico completo hacia una arquitectura basada en **5 agentes-fase**, con las 25 responsabilidades de dominio actuales convertidas en **personas invocables internamente** por los agentes-fase (checklists ejecutables, no entidades seleccionables). Las 69 skills se consolidan en **~10 skills reales con procedimiento paso a paso**. Los workflows se transforman en **1 canónico + 3 de negocio**, invocables como slash-commands/prompts en todos los IDEs.

### 1. Nueva capa de agentes-fase (5)

Un único punto de entrada por fase del ciclo de vida:

- **`spec`** — traduce necesidad social a OpenSpec (`proposal.md` + `design.md` + `tasks.md` + `spec.md`), invocando internamente las personas `license-legal`, `privacy-ethics`, `caasaac-methodology`, `a11y-cognitive`, `arasaac-liaison`, `solution-architect`.
- **`build`** — implementa una task atómica de OpenSpec sin importar el subsistema (backend/frontend/mcp/data se deciden por globs de la task); invoca personas `backend`, `frontend`, `mcp-architect`, `data-connector`, `semantic-search`, `export-document`, `devops` según los archivos tocados.
- **`verify`** — ejecuta tests, lint, typecheck, axe, contratos visuales y los 3 gates críticos (license/privacy/human-review); invoca personas `qa`, `accessibility-qa`, `test-automation`, `security`, `license-legal`, `privacy-ethics`, `observability`.
- **`docs`** — genera/actualiza README, manuales, changelogs y dossier ARASAAC; invoca personas `documentation`, `arasaac-liaison`, `easy-reading`, `ux-accessibility`.
- **`release`** — archiva la change OpenSpec, publica release notes y regenera packs multi-IDE; invoca personas `release-manager`, `openspec-steward`, `product-owner-social`, `devops`.

Los agentes-fase son los únicos seleccionables desde el UI de los IDEs. Las 15 personas viven en `.agents/personas/` como checklists reutilizables.

### 2. Consolidación de skills (~10 con procedimiento real)

- `openspec-lifecycle` — crear/validar/archivar changes OpenSpec.
- `arasaac-fetch` — consulta API + normalización + cache + manifest entry.
- `mcp-tool-scaffold` — schema + implementación + contract test + security review.
- `material-pipeline` — intake → search pictograms → edit → validate → human-review → export.
- `export-with-manifest` — HTML/PDF/DOCX/PPTX/ZIP con atribución y manifest.
- `human-review-gate` — solicita/aprueba/rechaza revisión humana.
- `compliance-scan` — un único scan que agrupa license + privacy + pictogram-ids + visual-density + plain-language + non-commercial-context.
- `a11y-audit` — WCAG 2.2 AA + keyboard + focus + color-independence + labels + cognitive.
- `docs-generate` — README + technical + deployment + contribution + release-notes + entity-manual + dossier.
- `openspec-archive` — cerrar `tasks.md`, mover a `openspec/changes/archive/`, actualizar índices.

Las 69 skills legacy se archivan en `.agents/archive/skills-legacy/` sin pérdida de información.

### 3. Workflows ejecutables (1 canónico + 3 de negocio)

- **`spec-build-verify.workflow.md`** — canónico OpenSpec: intake → proposal → design → tasks → spec → implementación → tests → review → archive.
- **`create-visual-agenda.workflow.md`** — negocio, encadena skills `material-pipeline` + `arasaac-fetch` + `human-review-gate` + `export-with-manifest`.
- **`create-communication-board.workflow.md`** — negocio.
- **`create-easy-reading.workflow.md`** — negocio.

Cada workflow es un `.md` con procedimiento paso a paso; se convierte automáticamente en:
- slash-command en Cursor/Claude Code (`.cursor/commands/`, `.claude/commands/`)
- prompt en Copilot (`.github/prompts/`)
- prompt en Codex y OpenCode.

### 4. Reglas unificadas

- `.agents/rules/mandatory-gates.md` — único archivo que declara los 3 gates críticos (license/privacy/human-review), referenciado por todas las skills y agentes vía frontmatter. Elimina la duplicación de 5 líneas repetidas en 69 skills × 5 IDEs.

### 5. Nuevo doc maestro

- `.agents/00_OPERATING_MODEL.md` reemplaza `02_AGENTES_SKILLS_WORKFLOWS_V2.md` (versión anterior demasiado extensa y descriptiva; el nuevo es operativo y accionable).

### 6. Sincronización multi-IDE preservada

Los targets se mantienen (Cursor, Codex, Claude Code, OpenCode, VS Code/Copilot, Obsidian). El script `scripts/sync_agent_packs.py` se refactoriza para entender:
- agentes-fase (5) → cada IDE recibe los 5 con su formato nativo.
- personas (15) → se distribuyen como referencia (no seleccionable en UI).
- skills (~10) → un directorio por skill con `SKILL.md` real.
- workflows (4) → generan slash-command/prompt en cada IDE.
- prompts base (4) → `new-spec`, `implement-task`, `verify-change`, `archive-change`.

`scripts/verify_agent_packs_sync.py` se actualiza con invariantes nuevos y falla el CI si detecta drift.

## Fuera de alcance

- Cambiar el modelo o proveedor de IA de ningún IDE (no toca `0030-azure-foundry-ai-provider`).
- Modificar reglas de negocio del dominio (licencia CC BY-NC-SA, revisión humana obligatoria, prohibición de PII, prohibición de pictogramas generados). Estas quedan intactas y se refuerzan al unificar los gates.
- Añadir nuevas capacidades funcionales del producto (agendas, tableros, easy-reading). Solo se reorganiza el pack agentico.
- Retirar o modificar changes OpenSpec activas (0009–0035).
- Migrar los 11 duplicados `* 2.py` con contenido divergente detectados en `services/api/tests/` (se documentan como deuda técnica separada).

## Valor

- **Elimina la fricción de selección**: el usuario en Copilot/Cursor/Claude sólo ve 5 agentes-fase y 4 slash-commands consistentes, en vez de 25 agentes + 69 skills + 8 workflows.
- **Refuerza el cumplimiento**: los 3 gates críticos (license/privacy/human-review) pasan de estar duplicados en 345 archivos (69 × 5 IDEs) a un único punto de verdad referenciado por todos.
- **Flujos ejecutables reales**: cada workflow es un procedimiento paso a paso con inputs/outputs claros, no una lista de tags.
- **Multi-IDE garantizado sin ruido**: el script de sync mantiene los 6 IDEs operativos pero con ×85 % menos archivos generados.
- **Reduce el mantenimiento**: cambiar un gate o una regla se hace en 1 archivo, no en 345.
- **Preserva la trazabilidad**: nada se borra sin archivar; el legacy queda accesible en `.agents/archive/` por auditoría.
- **Alineado con AGENTS.md**: mantiene el flujo OpenSpec obligatorio y las 10 reglas absolutas del proyecto; solo cambia el *cómo* se ejecutan, no el *qué*.

## Referencias

- Fuente canónica actual: `.agents/` (`catalog/`, `content/`, `rules/`, `skills/`).
- Doc maestro previo: `.agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md`.
- Reglas de repositorio: `AGENTS.md`.
- Instrucciones IDE truncadas: `.github/copilot-instructions.md` (paso 6 sin desarrollar).
- Script de sync actual: `scripts/sync_agent_packs.py`.
- Verificador actual: `scripts/verify_agent_packs_sync.py`.
- CI: `.github/workflows/agent-packs.yml`.
- Documentación pública: `docs/agents/multi-ide-agent-packs.md`.
- Deuda separada: 11 duplicados `* 2.py` con contenido divergente en `services/api/tests/` y `services/api/alembic/` (fuera de esta change).
