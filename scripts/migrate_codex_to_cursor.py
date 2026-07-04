#!/usr/bin/env python3
"""Migrate .codex pack to .cursor format with Cursor-native frontmatter."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / ".codex"
CURSOR = ROOT / ".cursor"

READONLY_AGENTS = {
    "qa",
    "accessibility_qa",
    "license_legal_compliance",
    "privacy_ethics",
    "arasaac_liaison",
}

WORKFLOW_DESCRIPTIONS = {
    "development_openspec_codex": (
        "Flujo maestro OpenSpec → Cursor: intake, proposal, design, compliance, "
        "tasks, implementación, tests, review y archive."
    ),
    "create_visual_agenda": (
        "Crear agenda visual accesible con pictogramas ARASAAC reales, "
        "desde intake guiado hasta exportación con revisión humana."
    ),
    "create_communication_board": (
        "Crear tablero de comunicación con categorías, pictogramas reales "
        "y validación CAA/SAAC."
    ),
    "easy_reading_document": (
        "Adaptar documento a lectura fácil con apoyo pictográfico y revisión humana."
    ),
    "cee_conacee_kit": (
        "Generar kit CEE/CONACEE: PRL, rutinas, señalética y pack exportable."
    ),
    "cermi_foundation_kit": (
        "Generar kit CERMI/fundaciones: guías, trámites y comunicación institucional."
    ),
    "export_readiness": (
        "Validar readiness global antes de exportar: PII, licencia, pictogramas, revisión."
    ),
    "arasaac_validation_dossier": (
        "Preparar dossier institucional para validación ARASAAC/Gobierno de Aragón."
    ),
}

WORKFLOW_STEP_OVERRIDES: dict[str, dict[str, str]] = {
    "easy_reading_document": {
        "review": "Revisión humana o profesional antes de exportar",
    },
    "export_readiness": {
        "human_review": "validate_human_review_approved",
    },
}

WORKFLOW_STEP_LABELS = {
    "intake": "Intake estructurado de necesidad social",
    "proposal": "Redactar proposal.md",
    "design": "Redactar design.md y ADRs si aplica",
    "compliance_precheck": "Precheck licencia, privacidad y seguridad",
    "atomic_tasks": "Dividir tasks.md atómicas listas para Cursor",
    "codex_implementation": "Implementación según OpenSpec (Cursor Agent)",
    "tests": "Ejecutar y añadir tests",
    "review": "Review técnica, QA, accesibilidad y seguridad",
    "archive": "Archivar change OpenSpec",
    "guided_intake": "Intake guiado: objetivo, contexto, nivel, idioma",
    "privacy_check": "Validar ausencia de PII",
    "caasaac_strategy": "Definir estrategia CAA/SAAC",
    "draft_steps": "Generar borrador de pasos",
    "search_pictograms": "Buscar pictogramas reales ARASAAC",
    "edit": "Edición por usuario/profesional",
    "validate": "Ejecutar validadores de material",
    "human_review": "Revisión humana obligatoria",
    "export": "Exportar con créditos y manifiesto",
    "domain_categories": "Seleccionar dominio y categorías",
    "caasaac_balance": "Revisar equilibrio de vocabulario CAA/SAAC",
    "edit_grid": "Editar grid del tablero",
    "source_intake": "Ingesta de documento fuente",
    "extract_key_messages": "Extraer mensajes clave",
    "simplify": "Simplificar lenguaje",
    "map_concepts": "Mapear conceptos pictografiables",
    "select_process": "Seleccionar proceso CEE",
    "domain_template": "Aplicar plantilla de dominio NGO/CEE",
    "caasaac_review": "Revisión metodológica CAA/SAAC",
    "generate_pack": "Generar pack de materiales",
    "expert_review_flag": "Marcar contenido que requiere revisión experta",
    "select_goal": "Seleccionar objetivo del kit",
    "easy_reading": "Adaptar a lectura fácil",
    "cognitive_review": "Revisión de accesibilidad cognitiva",
    "institutional_review": "Revisión institucional",
    "no_pii": "validate_no_personal_data",
    "real_ids": "validate_pictogram_ids_real",
    "no_modified_pictograms": "validate_no_modified_pictograms",
    "license_visible": "validate_license_notice_visible",
    "non_commercial": "validate_non_commercial_context",
    "plain_language": "validate_plain_language",
    "visual_density": "validate_visual_density",
    "manifest": "validate_manifest_complete",
    "collect_purpose": "Recopilar propósito social y entidades objetivo",
    "collect_controls": "Recopilar controles técnicos y de licencia",
    "examples": "Incluir ejemplos exportados",
    "legal_review": "Revisión legal de anexos",
    "dossier": "Redactar dossier completo",
    "human_approval": "Aprobación humana del equipo",
    "send": "Enviar a ARASAAC (pendiente de validación institucional)",
}


def slugify(value: str) -> str:
    value = value.replace("skill.", "")
    value = value.replace("skill.", "")
    if value.startswith("codex."):
        value = "cursor." + value[len("codex.") :]
    return value.replace(".", "-").replace("_", "-")


def agent_slug(agent_id: str) -> str:
    return agent_id.replace("_", "-")


def build_agent_description(name: str, mission: str) -> str:
    short = mission.rstrip(".")
    return f"{short}. Usar para tareas de {name} en ARASAAC Social MCP Platform."


def migrate_agents() -> int:
    catalog = yaml.safe_load((CODEX / "agents" / "agent_catalog.yaml").read_text())
    count = 0
    agents_dir = CURSOR / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    for entry in catalog["agents"]:
        agent_id = entry["id"]
        src = CODEX / "agents" / f"{agent_id}.md"
        body = src.read_text(encoding="utf-8").strip()
        body = re.sub(r"Codex/OpenSpec", "Cursor/OpenSpec", body)
        body = re.sub(r"\bCodex\b", "Cursor", body)

        frontmatter = [
            "---",
            f"name: {agent_slug(agent_id)}",
            f"description: {build_agent_description(entry['name'], entry['mission'])}",
            "model: inherit",
        ]
        if agent_id in READONLY_AGENTS:
            frontmatter.append("readonly: true")
        frontmatter.append("---")

        content = "\n".join(frontmatter) + "\n\n" + body + "\n"
        (agents_dir / f"{agent_slug(agent_id)}.md").write_text(content, encoding="utf-8")
        count += 1

    return count


def skill_domain(skill: dict) -> str:
    domain = skill["domain"]
    return "cursor" if domain == "codex" else domain


def skill_description(skill: dict) -> str:
    domain = skill_domain(skill)
    name = skill["name"].replace("_", " ")
    gates = skill.get("critical_gates") or []
    base = f"Skill {domain}/{name} para ARASAAC Social MCP Platform."
    if gates:
        base += f" Gates críticos: {', '.join(gates)}."
    if skill.get("requires_openspec"):
        base += " Requiere OpenSpec aprobada."
    return base


def migrate_skills() -> int:
    catalog = yaml.safe_load((CODEX / "skills" / "skill_catalog.yaml").read_text())
    count = 0

    for skill in catalog["skills"]:
        folder_name = slugify(skill["id"])
        skill_dir = CURSOR / "skills" / folder_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        domain = skill_domain(skill)
        skill_id = skill["id"].replace("skill.codex.", "skill.cursor.")

        metadata_lines = [
            f"  domain: {domain}",
            f"  requires_openspec: {str(skill.get('requires_openspec', False)).lower()}",
        ]
        if skill.get("critical_gates"):
            metadata_lines.append(f"  critical_gates: {skill['critical_gates']}")

        frontmatter = [
            "---",
            f"name: {folder_name}",
            f"description: {skill_description(skill)}",
            "metadata:",
            *metadata_lines,
            "---",
        ]

        body = f"""# {skill_id}

## Propósito

Ejecutar la capacidad `{skill_id}` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `{domain}/{skill['name']}`.

## Salida esperada

```text
status: pass | warn | fail
summary: <resumen>
artifacts: <artefactos generados o modificados>
risks: <riesgos>
next_actions: <acciones>
```

## Gates

- Trabajar siempre contra OpenSpec aprobada.
- No generar ni modificar pictogramas ARASAAC.
- No exportar sin revisión humana aprobada.
- No introducir datos personales en MVP.
- Preservar atribución visible CC BY-NC-SA.
"""
        if skill.get("critical_gates"):
            body += "\n## Gates críticos adicionales\n\n"
            for gate in skill["critical_gates"]:
                body += f"- `{gate}`\n"

        (skill_dir / "SKILL.md").write_text(
            "\n".join(frontmatter) + "\n\n" + body + "\n",
            encoding="utf-8",
        )
        count += 1

    return count


def migrate_workflows() -> int:
    catalog = yaml.safe_load((CODEX / "workflows" / "workflow_catalog.yaml").read_text())
    count = 0

    for workflow_id, steps in catalog["workflows"].items():
        folder_name = workflow_id.replace("_", "-")
        if folder_name == "development-openspec-codex":
            folder_name = "development-openspec-cursor"

        skill_dir = CURSOR / "skills" / folder_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        description = WORKFLOW_DESCRIPTIONS.get(
            workflow_id,
            f"Workflow {workflow_id.replace('_', ' ')} para ARASAAC Social MCP Platform.",
        )

        frontmatter = [
            "---",
            f"name: {folder_name}",
            f"description: {description}",
            "metadata:",
            f"  type: workflow",
            f"  source_id: {workflow_id}",
            "---",
        ]

        lines = [
            f"# Workflow: {workflow_id}",
            "",
            "## Pasos",
            "",
        ]
        for index, step in enumerate(steps, start=1):
            label = WORKFLOW_STEP_OVERRIDES.get(workflow_id, {}).get(step)
            if not label:
                label = WORKFLOW_STEP_LABELS.get(step, step.replace("_", " "))
            lines.append(f"{index}. **{step}** — {label}")

        lines.extend(
            [
                "",
                "## Reglas transversales",
                "",
                "- Solo pictogramas reales ARASAAC.",
                "- Revisión humana obligatoria antes de exportar.",
                "- Atribución visible en toda exportación.",
                "- Sin datos personales en MVP.",
                "- OpenSpec aprobada para cambios de producto/código.",
                "",
            ]
        )

        (skill_dir / "SKILL.md").write_text(
            "\n".join(frontmatter) + "\n\n" + "\n".join(lines) + "\n",
            encoding="utf-8",
        )
        count += 1

    return count


def migrate_commands() -> int:
    commands_dir = CURSOR / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)

    mappings = {
        "generate-task-prompt.md": CODEX / "codex" / "task_prompt_template.md",
        "review-patch.md": CODEX / "codex" / "review_prompt_template.md",
        "create-pr-summary.md": CODEX / "codex" / "pr_summary_template.md",
        "cursor-master-prompt.md": CODEX / "prompts" / "codex_master_prompt.md",
    }

    for dest_name, src_path in mappings.items():
        content = src_path.read_text(encoding="utf-8")
        content = content.replace("Codex Task Prompt Template", "Cursor Task Prompt Template")
        content = content.replace("Codex Review Prompt Template", "Cursor Review Prompt Template")
        content = content.replace("Codex Master Prompt", "Cursor Master Prompt")
        content = content.replace("Codex", "Cursor")
        (commands_dir / dest_name).write_text(content, encoding="utf-8")

    return len(mappings)


def migrate_rules() -> None:
    rules_dir = CURSOR / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)

    content = """---
description: Reglas absolutas ARASAAC Social MCP Platform — licencia, privacidad, accesibilidad y OpenSpec
alwaysApply: true
---

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
4. Implementar con Cursor Agent contra task atómica.
5. Ejecutar tests y actualizar docs.
6. Archivar OpenSpec al completar.

# Política ARASAAC

Cada uso de pictograma debe almacenar ID, label, URL, autor, propietario, licencia CC BY-NC-SA, fecha y material. Cada exportación incluye atribución visible.

# Accesibilidad

El frontend debe aspirar a WCAG 2.2 AA: teclado, foco visible, contraste, semántica, labels claros, no depender solo del color.
"""
    (rules_dir / "arasaac-platform.mdc").write_text(content, encoding="utf-8")


def write_readme(agent_count: int, skill_count: int, workflow_count: int, command_count: int) -> None:
    readme = f"""# ARASAAC Agents, Skills & Workflows — Cursor Pack

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
| Subagentes | {agent_count} | `.codex/agents/*.md` + `agent_catalog.yaml` |
| Skills | {skill_count} | `.codex/skills/skill_catalog.yaml` |
| Workflows (como skills) | {workflow_count} | `.codex/workflows/workflow_catalog.yaml` |
| Commands | {command_count} | `.codex/codex/*` + `prompts/codex_master_prompt.md` |
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
"""
    (CURSOR / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    agent_count = migrate_agents()
    skill_count = migrate_skills()
    workflow_count = migrate_workflows()
    command_count = migrate_commands()
    migrate_rules()
    write_readme(agent_count, skill_count, workflow_count, command_count)
    print(
        f"Migrated: {agent_count} agents, {skill_count} skills, "
        f"{workflow_count} workflows, {command_count} commands, 1 rule"
    )


if __name__ == "__main__":
    main()
