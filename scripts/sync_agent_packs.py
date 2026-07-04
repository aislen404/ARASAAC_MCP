#!/usr/bin/env python3
"""Sync multi-IDE agent packs from canonical .agents/ source."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".agents"
CATALOG = AGENTS / "catalog"
CONTENT = AGENTS / "content"

WORKFLOW_DESCRIPTIONS = {
    "development_openspec_codex": (
        "Flujo maestro OpenSpec → implementación: intake, proposal, design, "
        "compliance, tasks, implementación, tests, review y archive."
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
    "atomic_tasks": "Dividir tasks.md atómicas listas para el agente de implementación",
    "codex_implementation": "Implementación según OpenSpec",
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

RULE_GLOBS = {
    "backend": "apps/api/**,packages/domain/**,packages/contracts/**",
    "frontend": "apps/web/**,packages/ui/**",
    "mcp": "apps/mcp-server/**,packages/mcp-contracts/**",
    "export-license": "packages/export/**,templates/**,docs/legal/**",
}


def load_config() -> dict[str, Any]:
    return yaml.safe_load((CATALOG / "packs.yaml").read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    value = value.replace("skill.", "")
    if value.startswith("codex."):
        value = "agent." + value[len("codex.") :]
    return value.replace(".", "-").replace("_", "-")


def agent_slug(agent_id: str) -> str:
    return agent_id.replace("_", "-")


def workflow_folder(workflow_id: str) -> str:
    name = workflow_id.replace("_", "-")
    if name == "development-openspec-codex":
        return "development-openspec"
    return name


def read_agent_body(agent_id: str) -> str:
    return (CONTENT / "agents" / f"{agent_id}.md").read_text(encoding="utf-8").strip()


def localize_body(body: str, impl_agent: str) -> str:
    body = body.replace("agente de implementación/OpenSpec", f"{impl_agent}/OpenSpec")
    body = body.replace("agente de implementación", impl_agent)
    return body


def build_agent_description(name: str, mission: str) -> str:
    return f"{mission.rstrip('.')}. Usar para tareas de {name} en ARASAAC Social MCP Platform."


def skill_needs_manual(skill: dict, folder_name: str, config: dict) -> bool:
    if skill.get("domain") in config.get("manual_invocation_domains", []):
        return True
    return folder_name in config.get("manual_invocation_workflows", [])


def build_skill_body(skill_id: str, domain: str, skill_name: str) -> str:
    return f"""# {skill_id}

## Propósito

Ejecutar la capacidad `{skill_id}` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `{domain}/{skill_name}`.

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


def skill_description(skill: dict) -> str:
    domain = skill["domain"]
    if domain == "codex":
        domain = "agent"
    name = skill["name"].replace("_", " ")
    gates = skill.get("critical_gates") or []
    base = f"Skill {domain}/{name} para ARASAAC Social MCP Platform."
    if gates:
        base += f" Gates críticos: {', '.join(gates)}."
    if skill.get("requires_openspec"):
        base += " Requiere OpenSpec aprobada."
    return base


def canonical_skill_id(skill: dict) -> str:
    return skill["id"].replace("skill.codex.", "skill.agent.")


def build_skill_frontmatter(
    folder_name: str,
    skill: dict,
    config: dict,
    *,
    cursor_extras: bool = False,
) -> list[str]:
    metadata_lines = [
        f"  domain: {skill['domain'] if skill['domain'] != 'codex' else 'agent'}",
        f"  requires_openspec: {str(skill.get('requires_openspec', False)).lower()}",
    ]
    if skill.get("critical_gates"):
        metadata_lines.append(f"  critical_gates: {skill['critical_gates']}")

    lines = [
        "---",
        f"name: {folder_name}",
        f"description: {skill_description(skill)}",
    ]
    if cursor_extras and skill_needs_manual(skill, folder_name, config):
        lines.append("disable-model-invocation: true")
    lines.extend(["metadata:", *metadata_lines, "---"])
    return lines


def write_skill(path: Path, frontmatter: list[str], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(frontmatter) + "\n\n" + body + "\n", encoding="utf-8")


def build_workflow_skill(workflow_id: str, steps: list[str], config: dict) -> tuple[list[str], str]:
    folder_name = workflow_folder(workflow_id)
    description = WORKFLOW_DESCRIPTIONS.get(
        workflow_id,
        f"Workflow {workflow_id.replace('_', ' ')} para ARASAAC Social MCP Platform.",
    )
    frontmatter = [
        "---",
        f"name: {folder_name}",
        f"description: {description}",
        "metadata:",
        "  type: workflow",
        f"  source_id: {workflow_id}",
        "---",
    ]
    lines = [f"# Workflow: {workflow_id}", "", "## Pasos", ""]
    for index, step in enumerate(steps, start=1):
        label = WORKFLOW_STEP_OVERRIDES.get(workflow_id, {}).get(step)
        if not label:
            label = WORKFLOW_STEP_LABELS.get(step, step.replace("_", " "))
        if step == "codex_implementation":
            label = f"Implementación según OpenSpec ({config['targets']['cursor']['impl_agent']})"
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
    return frontmatter, "\n".join(lines) + "\n"


def sync_canonical_skills(config: dict) -> dict[str, Path]:
    skills_catalog = yaml.safe_load((CATALOG / "skills.yaml").read_text(encoding="utf-8"))
    workflows = yaml.safe_load((CATALOG / "workflows.yaml").read_text(encoding="utf-8"))
    canonical_dir = ROOT / config["canonical"]["skills_path"]
    skill_paths: dict[str, Path] = {}

    if canonical_dir.exists():
        shutil.rmtree(canonical_dir)
    canonical_dir.mkdir(parents=True)

    for skill in skills_catalog["skills"]:
        folder_name = slugify(skill["id"])
        skill_id = canonical_skill_id(skill)
        domain = skill["domain"] if skill["domain"] != "codex" else "agent"
        body = build_skill_body(skill_id, domain, skill["name"])
        if skill.get("critical_gates"):
            body += "\n## Gates críticos adicionales\n\n"
            for gate in skill["critical_gates"]:
                body += f"- `{gate}`\n"
        path = canonical_dir / folder_name / "SKILL.md"
        write_skill(path, build_skill_frontmatter(folder_name, skill, config), body)
        skill_paths[folder_name] = path

    for workflow_id, steps in workflows["workflows"].items():
        folder_name = workflow_folder(workflow_id)
        frontmatter, body = build_workflow_skill(workflow_id, steps, config)
        if folder_name in config.get("manual_invocation_workflows", []):
            frontmatter.insert(-1, "metadata:")
            frontmatter.insert(-1, "disable-model-invocation: true")
        path = canonical_dir / folder_name / "SKILL.md"
        write_skill(path, frontmatter, body)
        skill_paths[folder_name] = path

    return skill_paths


def copy_skills_tree(src: Path, dest: Path, *, cursor_extras: bool = False, config: dict | None = None) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    skills_catalog = yaml.safe_load((CATALOG / "skills.yaml").read_text(encoding="utf-8"))
    workflows = yaml.safe_load((CATALOG / "workflows.yaml").read_text(encoding="utf-8"))
    skill_by_folder = {slugify(s["id"]): s for s in skills_catalog["skills"]}

    for skill_dir in sorted(src.iterdir()):
        if not skill_dir.is_dir():
            continue
        folder_name = skill_dir.name
        target = dest / folder_name / "SKILL.md"
        body = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        parts = body.split("---", 2)
        body_content = parts[2].strip() if len(parts) >= 3 else body.strip()

        if folder_name in skill_by_folder:
            skill = skill_by_folder[folder_name]
            fm = build_skill_frontmatter(folder_name, skill, config or {}, cursor_extras=cursor_extras)
            write_skill(target, fm, body_content)
        else:
            shutil.copytree(skill_dir, dest / folder_name)

    for workflow_id, steps in workflows["workflows"].items():
        folder_name = workflow_folder(workflow_id)
        frontmatter, wf_body = build_workflow_skill(workflow_id, steps, config or load_config())
        if cursor_extras and folder_name in (config or load_config()).get("manual_invocation_workflows", []):
            frontmatter.insert(-1, "disable-model-invocation: true")
        write_skill(dest / folder_name / "SKILL.md", frontmatter, wf_body)


def sync_cursor_agents(config: dict) -> int:
    catalog = yaml.safe_load((CATALOG / "agents.yaml").read_text(encoding="utf-8"))
    agents_dir = ROOT / ".cursor" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    readonly = set(config.get("readonly_agents", []))
    impl = config["targets"]["cursor"]["impl_agent"]
    count = 0
    for entry in catalog["agents"]:
        agent_id = entry["id"]
        body = localize_body(read_agent_body(agent_id), impl)
        frontmatter = [
            "---",
            f"name: {agent_slug(agent_id)}",
            f"description: {build_agent_description(entry['name'], entry['mission'])}",
            "model: inherit",
        ]
        if agent_id in readonly:
            frontmatter.append("readonly: true")
        frontmatter.append("---")
        (agents_dir / f"{agent_slug(agent_id)}.md").write_text(
            "\n".join(frontmatter) + "\n\n" + body + "\n",
            encoding="utf-8",
        )
        count += 1
    return count


def sync_claude_opencode_agents(target: str, config: dict) -> int:
    catalog = yaml.safe_load((CATALOG / "agents.yaml").read_text(encoding="utf-8"))
    agents_dir = ROOT / config["targets"][target]["agents_path"]
    agents_dir.mkdir(parents=True, exist_ok=True)
    readonly = set(config.get("readonly_agents", []))
    impl = config["targets"][target]["impl_agent"]
    count = 0
    for entry in catalog["agents"]:
        agent_id = entry["id"]
        body = localize_body(read_agent_body(agent_id), impl)
        frontmatter = [
            "---",
            f"name: {agent_slug(agent_id)}",
            f"description: {build_agent_description(entry['name'], entry['mission'])}",
            "model: inherit",
        ]
        if target == "claude":
            frontmatter.append("color: blue")
        if agent_id in readonly:
            frontmatter.append("readonly: true")
        frontmatter.append("---")
        (agents_dir / f"{agent_slug(agent_id)}.md").write_text(
            "\n".join(frontmatter) + "\n\n" + body + "\n",
            encoding="utf-8",
        )
        count += 1
    return count


def sync_codex_pack(config: dict) -> None:
    codex = ROOT / ".codex"
    catalog = yaml.safe_load((CATALOG / "agents.yaml").read_text(encoding="utf-8"))
    readonly = set(config.get("readonly_agents", []))
    impl = config["targets"]["codex"]["impl_agent"]

    agents_dir = codex / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    for md in agents_dir.glob("*.md"):
        md.unlink()
    for toml in agents_dir.glob("*.toml"):
        toml.unlink()

    for entry in catalog["agents"]:
        agent_id = entry["id"]
        body = localize_body(read_agent_body(agent_id), impl)
        prompt_match = re.search(
            r"## Prompt base\s+```text\n(.*?)```", body, re.DOTALL
        )
        if prompt_match:
            instructions = prompt_match.group(1).strip()
        else:
            instructions = body

        toml_lines = [
            f'name = "{agent_id}"',
            f'description = "{build_agent_description(entry["name"], entry["mission"])}"',
            'model = "inherit"',
        ]
        if agent_id in readonly:
            toml_lines.append('sandbox_mode = "read-only"')
        toml_lines.append(f'developer_instructions = """\n{instructions}\n"""')
        (agents_dir / f"{agent_id}.toml").write_text("\n".join(toml_lines) + "\n", encoding="utf-8")

        md_frontmatter = [
            "---",
            f"name: {agent_slug(agent_id)}",
            f"description: {build_agent_description(entry['name'], entry['mission'])}",
            "model: inherit",
        ]
        if agent_id in readonly:
            md_frontmatter.append("readonly: true")
        md_frontmatter.append("---")
        (agents_dir / f"{agent_id}.md").write_text(
            "\n".join(md_frontmatter) + "\n\n" + body + "\n",
            encoding="utf-8",
        )

    prompts_dir = codex / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    master = (CONTENT / "prompts" / "codex_master_prompt.md").read_text(encoding="utf-8")
    master = master.replace("Codex Master Prompt", f"{impl} Master Prompt")
    master = localize_body(master, impl)
    (prompts_dir / "codex_master_prompt.md").write_text(master, encoding="utf-8")
    shutil.copy2(CONTENT / "prompts" / "agent_system_prompts.md", prompts_dir / "agent_system_prompts.md")

    templates_dir = codex / "codex"
    templates_dir.mkdir(parents=True, exist_ok=True)
    for src_name, dest_name in {
        "task_prompt_template.md": "task_prompt_template.md",
        "review_prompt_template.md": "review_prompt_template.md",
        "pr_summary_template.md": "pr_summary_template.md",
    }.items():
        text = (CONTENT / "templates" / src_name).read_text(encoding="utf-8")
        (templates_dir / dest_name).write_text(localize_body(text, impl), encoding="utf-8")

    shutil.copy2(CATALOG / "agents.yaml", codex / "agents" / "agent_catalog.yaml")
    shutil.copy2(CATALOG / "skills.yaml", codex / "skills" / "skill_catalog.yaml")
    shutil.copy2(CATALOG / "workflows.yaml", codex / "workflows" / "workflow_catalog.yaml")


def sync_cursor_commands(config: dict) -> None:
    impl = config["targets"]["cursor"]["impl_agent"]
    commands_dir = ROOT / ".cursor" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    mappings = {
        "generate-task-prompt.md": "task_prompt_template.md",
        "review-patch.md": "review_prompt_template.md",
        "create-pr-summary.md": "pr_summary_template.md",
        "cursor-master-prompt.md": "../prompts/codex_master_prompt.md",
    }
    for dest, src in mappings.items():
        src_path = CONTENT / "templates" / src if not src.startswith("../") else CONTENT / "prompts" / "codex_master_prompt.md"
        text = src_path.read_text(encoding="utf-8")
        text = text.replace("Codex", impl).replace("agente de implementación", impl)
        if dest == "cursor-master-prompt.md":
            text = text.replace(f"{impl} Master Prompt", "Cursor Master Prompt")
        (commands_dir / dest).write_text(text, encoding="utf-8")


def sync_claude_commands(config: dict) -> None:
    impl = config["targets"]["claude"]["impl_agent"]
    commands_dir = ROOT / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    for dest, src in {
        "generate-task-prompt.md": "task_prompt_template.md",
        "review-patch.md": "review_prompt_template.md",
        "create-pr-summary.md": "pr_summary_template.md",
    }.items():
        text = localize_body((CONTENT / "templates" / src).read_text(encoding="utf-8"), impl)
        (commands_dir / dest).write_text(text, encoding="utf-8")


def sync_cursor_rules(config: dict) -> None:
    rules_dir = ROOT / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    platform = (AGENTS / "rules" / "platform.md").read_text(encoding="utf-8")
    content = f"""---
description: Reglas absolutas ARASAAC Social MCP Platform — licencia, privacidad, accesibilidad y OpenSpec
alwaysApply: true
---

{platform}

# Política ARASAAC

Cada uso de pictograma debe almacenar ID, label, URL, autor, propietario, licencia CC BY-NC-SA, fecha y material. Cada exportación incluye atribución visible.

# Accesibilidad

El frontend debe aspirar a WCAG 2.2 AA: teclado, foco visible, contraste, semántica, labels claros, no depender solo del color.
"""
    (rules_dir / "arasaac-platform.mdc").write_text(content, encoding="utf-8")

    for rule_name in ("backend", "frontend", "mcp", "export-license"):
        body = (AGENTS / "rules" / f"{rule_name}.md").read_text(encoding="utf-8")
        globs = RULE_GLOBS[rule_name]
        mdc = f"""---
description: Reglas {rule_name} ARASAAC Social MCP Platform
globs: {globs}
alwaysApply: false
---

{body}
"""
        (rules_dir / f"arasaac-{rule_name}.mdc").write_text(mdc, encoding="utf-8")


def sync_vscode_pack(config: dict) -> None:
    github = ROOT / ".github"
    agents_dir = github / "agents"
    prompts_dir = github / "prompts"
    instructions_dir = github / "instructions"
    agents_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)
    instructions_dir.mkdir(parents=True, exist_ok=True)

    catalog = yaml.safe_load((CATALOG / "agents.yaml").read_text(encoding="utf-8"))
    impl = config["targets"]["vscode"]["impl_agent"]
    readonly = set(config.get("readonly_agents", []))

    for entry in catalog["agents"]:
        agent_id = entry["id"]
        body = localize_body(read_agent_body(agent_id), impl)
        tools_line = 'tools: ["read", "search", "edit", "terminal"]'
        if agent_id in readonly:
            tools_line = 'tools: ["read", "search"]'
        frontmatter = [
            "---",
            f"name: {agent_slug(agent_id)}",
            f"description: {build_agent_description(entry['name'], entry['mission'])}",
            "model: inherit",
            "target: github-copilot",
            tools_line,
            "---",
        ]
        (agents_dir / f"{agent_slug(agent_id)}.agent.md").write_text(
            "\n".join(frontmatter) + "\n\n" + body + "\n",
            encoding="utf-8",
        )

    for dest, src in {
        "generate-task-prompt.prompt.md": "task_prompt_template.md",
        "review-patch.prompt.md": "review_prompt_template.md",
        "create-pr-summary.prompt.md": "pr_summary_template.md",
    }.items():
        text = localize_body((CONTENT / "templates" / src).read_text(encoding="utf-8"), impl)
        (prompts_dir / dest).write_text(text, encoding="utf-8")

    platform = (AGENTS / "rules" / "platform.md").read_text(encoding="utf-8")
    copilot = f"""# ARASAAC Social MCP Platform — Instrucciones Copilot

Este repositorio usa packs agenticos multi-IDE con fuente canónica en `.agents/`.

## Reglas universales

{platform}

## Packs por IDE

- **Cursor:** `.cursor/`
- **Codex:** `.codex/`
- **Claude Code:** `.claude/`
- **OpenCode:** `.opencode/`
- **VS Code / Copilot:** `.github/` (este pack)
- **Obsidian (referencia humana):** `docs/obsidian/agent-pack/`

## Documentación maestra

- `AGENTS.md` — reglas del repositorio
- `.agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md` — definición operativa completa
- Skills portables: `.agents/skills/` (estándar Agent Skills)

Todos los participantes deben tener las mismas capacidades agenticas; solo cambia el formato por IDE.
"""
    (github / "copilot-instructions.md").write_text(copilot, encoding="utf-8")

    for rule_name in ("backend", "frontend", "mcp", "export-license"):
        body = (AGENTS / "rules" / f"{rule_name}.md").read_text(encoding="utf-8")
        globs = RULE_GLOBS[rule_name]
        inst = f"""---
name: ARASAAC {rule_name}
description: Reglas {rule_name} del proyecto ARASAAC Social MCP Platform
applyTo: "{globs}"
---

{body}
"""
        (instructions_dir / f"arasaac-{rule_name}.instructions.md").write_text(inst, encoding="utf-8")


def sync_obsidian_vault(config: dict) -> None:
    vault = ROOT / config["targets"]["obsidian"]["path"]
    if vault.exists():
        shutil.rmtree(vault)
    vault.mkdir(parents=True)

    agents = yaml.safe_load((CATALOG / "agents.yaml").read_text(encoding="utf-8"))["agents"]
    skills = yaml.safe_load((CATALOG / "skills.yaml").read_text(encoding="utf-8"))["skills"]
    workflows = yaml.safe_load((CATALOG / "workflows.yaml").read_text(encoding="utf-8"))["workflows"]

    index = """---
tags: [agent-pack, moc]
---

# Agent Pack — Índice Obsidian

Base de conocimiento humana del pack agentico ARASAAC. Fuente canónica: `.agents/`.

## IDE packs

- [[Cursor Pack]]
- [[Codex Pack]]
- [[Claude Code Pack]]
- [[OpenCode Pack]]
- [[VS Code Copilot Pack]]

## Capas

- [[Agentes]] — 25 subagentes especializados
- [[Skills]] — 64 capacidades reutilizables
- [[Workflows]] — 8 flujos operativos

## Documento maestro

- [[02 Agentes Skills Workflows V2]]

## Reglas

- [[Reglas Plataforma]]
- [[Reglas Backend]]
- [[Reglas Frontend]]
- [[Reglas MCP]]
- [[Reglas Export Licencia]]
"""
    (vault / "00-Indice.md").write_text(index, encoding="utf-8")

    ide_readmes = {
        "Cursor Pack": ".cursor/",
        "Codex Pack": ".codex/",
        "Claude Code Pack": ".claude/",
        "OpenCode Pack": ".opencode/",
        "VS Code Copilot Pack": ".github/",
    }
    for title, path in ide_readmes.items():
        (vault / f"{title.replace(' ', '-')}.md").write_text(
            f"---\ntags: [agent-pack, ide]\n---\n\n# {title}\n\nRuta: `{path}`\n\nVolver a [[00-Indice]].\n",
            encoding="utf-8",
        )

    agents_index = "---\ntags: [agent-pack, agentes, moc]\n---\n\n# Agentes\n\n"
    for entry in agents:
        slug = agent_slug(entry["id"])
        title = entry["name"]
        agents_index += f"- [[Agente {title}]]\n"
        page = f"""---
tags: [agent, {entry['id']}]
aliases: ["{title}"]
---

# {title}

**Misión:** {entry['mission']}

**ID:** `{entry['id']}`

## Reglas comunes

{chr(10).join(f"- `{r}`" for r in entry.get('common_rules', []))}

## Enlaces

- Pack Cursor: `.cursor/agents/{slug}.md`
- Pack Codex: `.codex/agents/{entry['id']}.toml`
- Fuente: `.agents/content/agents/{entry['id']}.md`

Volver a [[Agentes]] · [[00-Indice]]
"""
        safe_name = title.replace("/", "-")
        (vault / "Agentes" / f"Agente {safe_name}.md").parent.mkdir(parents=True, exist_ok=True)
        (vault / "Agentes" / f"Agente {safe_name}.md").write_text(page, encoding="utf-8")
    (vault / "Agentes.md").write_text(agents_index + "\nVolver a [[00-Indice]].\n", encoding="utf-8")

    skills_index = "---\ntags: [agent-pack, skills, moc]\n---\n\n# Skills\n\n"
    for skill in skills:
        sid = canonical_skill_id(skill)
        folder = slugify(skill["id"])
        skills_index += f"- [[Skill {sid}]]\n"
        page = f"""---
tags: [skill, {skill['domain']}]
---

# {sid}

**Dominio:** `{skill['domain']}`

**Skill portable:** `.agents/skills/{folder}/SKILL.md`

Volver a [[Skills]] · [[00-Indice]]
"""
        (vault / "Skills" / f"Skill {sid}.md").parent.mkdir(parents=True, exist_ok=True)
        (vault / "Skills" / f"Skill {sid}.md").write_text(page, encoding="utf-8")
    (vault / "Skills.md").write_text(skills_index + "\nVolver a [[00-Indice]].\n", encoding="utf-8")

    wf_index = "---\ntags: [agent-pack, workflows, moc]\n---\n\n# Workflows\n\n"
    for wf_id in workflows:
        folder = workflow_folder(wf_id)
        wf_index += f"- [[Workflow {wf_id}]]\n"
        steps = workflows[wf_id]
        step_lines = "\n".join(f"{i}. `{s}`" for i, s in enumerate(steps, 1))
        page = f"""---
tags: [workflow]
---

# Workflow: {wf_id}

**Skill portable:** `.agents/skills/{folder}/SKILL.md`

## Pasos

{step_lines}

Volver a [[Workflows]] · [[00-Indice]]
"""
        (vault / "Workflows" / f"Workflow {wf_id}.md").parent.mkdir(parents=True, exist_ok=True)
        (vault / "Workflows" / f"Workflow {wf_id}.md").write_text(page, encoding="utf-8")
    (vault / "Workflows.md").write_text(wf_index + "\nVolver a [[00-Indice]].\n", encoding="utf-8")

    shutil.copy2(AGENTS / "02_AGENTES_SKILLS_WORKFLOWS_V2.md", vault / "02 Agentes Skills Workflows V2.md")
    for rule in ("platform", "backend", "frontend", "mcp", "export-license"):
        title = rule.replace("-", " ").title()
        shutil.copy2(AGENTS / "rules" / f"{rule}.md", vault / f"Reglas {title}.md")


def write_readmes(config: dict, counts: dict[str, int]) -> None:
    agents_root = f"""# ARASAAC Agent Pack — Fuente canónica

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

- Agentes: {counts.get('agents', 25)}
- Skills: {counts.get('skills', 64)}
- Workflows: {counts.get('workflows', 8)}
"""
    (AGENTS / "README.md").write_text(agents_root, encoding="utf-8")

    cursor_readme = f"""# Cursor Pack (generado)

Fuente canónica: `.agents/`. Regenerar con `python3 scripts/sync_agent_packs.py`.

- Subagentes: `.cursor/agents/` ({counts.get('agents', 25)})
- Skills: `.cursor/skills/` (+ portables en `.agents/skills/`)
- Commands: `/generate-task-prompt`, `/review-patch`, `/create-pr-summary`, `/cursor-master-prompt`
- Rules: `arasaac-platform.mdc` (always-on) + reglas por dominio con globs
"""
    (ROOT / ".cursor" / "README.md").write_text(cursor_readme, encoding="utf-8")

    codex_readme = """# Codex Pack (generado)

Fuente canónica: `.agents/`. Regenerar con `python3 scripts/sync_agent_packs.py`.

- Agents nativos: `.codex/agents/*.toml`
- Compat Cursor/legacy: `.codex/agents/*.md`
- Prompts y plantillas: `.codex/prompts/`, `.codex/codex/`
- Skills portables compartidos: `.agents/skills/`

Documento maestro: `.agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md`
"""
    (ROOT / ".codex" / "README.md").write_text(codex_readme, encoding="utf-8")

    for target, path_key in [
        ("claude", ".claude/README.md"),
        ("opencode", ".opencode/README.md"),
    ]:
        text = f"""# {config['targets'][target]['label']} Pack (generado)

Fuente canónica: `.agents/`. Regenerar con `python3 scripts/sync_agent_packs.py`.

- Agents: `{config['targets'][target]['agents_path']}/`
- Skills: `{config['targets'][target]['skills_path']}/` (copia de `.agents/skills/`)
"""
        (ROOT / path_key).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / path_key).write_text(text, encoding="utf-8")

    (ROOT / "docs/obsidian/agent-pack/README.md").write_text(
        """# Obsidian Agent Pack

Vault de referencia para el equipo. Abrir esta carpeta como parte del vault Obsidian del proyecto.

- Índice: [[00-Indice]]
- Fuente canónica: `.agents/`
- Regenerar: `python3 scripts/sync_agent_packs.py`
""",
        encoding="utf-8",
    )


def main() -> None:
    config = load_config()
    canonical_skills = sync_canonical_skills(config)
    counts = {"skills": len(canonical_skills)}

    copy_skills_tree(
        ROOT / config["canonical"]["skills_path"],
        ROOT / ".cursor/skills",
        cursor_extras=True,
        config=config,
    )
    copy_skills_tree(ROOT / config["canonical"]["skills_path"], ROOT / ".claude/skills", config=config)
    copy_skills_tree(ROOT / config["canonical"]["skills_path"], ROOT / ".opencode/skills", config=config)

    counts["agents"] = sync_cursor_agents(config)
    sync_claude_opencode_agents("claude", config)
    sync_claude_opencode_agents("opencode", config)
    sync_codex_pack(config)
    sync_cursor_commands(config)
    sync_claude_commands(config)
    sync_cursor_rules(config)
    sync_vscode_pack(config)
    sync_obsidian_vault(config)

    workflows = yaml.safe_load((CATALOG / "workflows.yaml").read_text(encoding="utf-8"))["workflows"]
    counts["workflows"] = len(workflows)

    write_readmes(config, counts)
    print(
        "Synced agent packs:",
        json.dumps(counts, ensure_ascii=False),
    )


if __name__ == "__main__":
    main()
