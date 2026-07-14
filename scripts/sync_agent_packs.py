#!/usr/bin/env python3
"""Sync multi-IDE agent packs from canonical .agents/ source (v2 architecture).

Fuente canónica única: `.agents/{agents,personas,skills,workflows,prompts,rules,catalog}`.
Targets: `.cursor/`, `.codex/`, `.claude/`, `.opencode/`, `.github/`, `docs/obsidian/agent-pack/`.

Cada archivo generado lleva el header:
    <!-- generated from .agents/ — do not edit manually -->
    <!-- source-hash: <sha256 first 12 chars of the source content> -->

Diseño OpenSpec: `openspec/changes/0036-agent-system-refactor/design.md`.
"""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / ".agents"
CATALOG_DIR = AGENTS_DIR / "catalog"

GENERATED_HEADER = "<!-- generated from .agents/ — do not edit manually -->\n"

# ── Utilidades ──────────────────────────────────────────────────────────────


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((CATALOG_DIR / f"{name}.yaml").read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def source_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def write_generated(target: Path, source_text: str, extra_prefix: str = "") -> None:
    """Escribir archivo generado con header + hash reproducibles."""
    target.parent.mkdir(parents=True, exist_ok=True)
    header = GENERATED_HEADER + f"<!-- source-hash: {source_hash(source_text)} -->\n"
    body = extra_prefix + source_text
    target.write_text(header + body if not body.startswith("---") else header + body, encoding="utf-8")


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


# ── Copias canónicas (agents, personas, skills, workflows) ──────────────────


def copy_canonical_files(
    source_dir: Path,
    target_dir: Path,
    pattern: str = "*",
    recursive: bool = False,
) -> int:
    """Copiar los .md canónicos añadiendo header generado."""
    clean_dir(target_dir)
    count = 0
    if recursive:
        # skills viven en subdirectorios (skill-name/SKILL.md)
        for skill_dir in sorted(source_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            source = read_text(skill_file)
            target = target_dir / skill_dir.name / "SKILL.md"
            write_generated(target, source)
            count += 1
    else:
        for src in sorted(source_dir.glob(pattern)):
            if not src.is_file():
                continue
            source = read_text(src)
            target = target_dir / src.name
            write_generated(target, source)
            count += 1
    return count


# ── Prompts / slash-commands ────────────────────────────────────────────────


def prompt_source(prompt_name: str) -> str:
    return read_text(AGENTS_DIR / "prompts" / f"{prompt_name}.prompt.md")


def write_prompts(prompts: list[dict], target_dir: Path, extension: str = "prompt.md") -> int:
    """Materializar prompts como slash-commands en el IDE target."""
    clean_dir(target_dir)
    count = 0
    for entry in prompts:
        source = prompt_source(entry["name"])
        # slash-command name = /entry["slash_command"] (sin la barra)
        filename = f"{entry['name']}.{extension}"
        write_generated(target_dir / filename, source)
        count += 1
    return count


# ── Rules ───────────────────────────────────────────────────────────────────

RULE_APPLY = {
    "backend": "apps/api/**,packages/domain/**,packages/contracts/**,services/api/**",
    "frontend": "apps/web/**,packages/ui/**",
    "mcp": "apps/mcp-server/**,packages/mcp-contracts/**,services/mcp/**",
    "export-license": "packages/export/**,templates/**,docs/legal/**,docs/compliance/**",
}


def write_rules(target_dir: Path, extension: str, add_apply_to: bool = False) -> int:
    """Copiar rules a target con extensión IDE-específica (.mdc, .instructions.md, .md)."""
    clean_dir(target_dir)
    rules_src = AGENTS_DIR / "rules"
    count = 0
    for src in sorted(rules_src.glob("*.md")):
        name = src.stem  # backend, frontend, mcp, export-license, platform, mandatory-gates
        body = read_text(src)
        if add_apply_to and name in RULE_APPLY:
            fm = (
                "---\n"
                f"description: Reglas {name} — ARASAAC Social MCP Platform\n"
                f"applyTo: \"{RULE_APPLY[name]}\"\n"
                "---\n\n"
            )
            content = fm + body
        elif add_apply_to and name in ("platform", "mandatory-gates"):
            fm = (
                "---\n"
                f"description: Reglas {name} — ARASAAC Social MCP Platform (always apply)\n"
                "applyTo: \"**\"\n"
                "---\n\n"
            )
            content = fm + body
        else:
            content = body
        target_file = target_dir / f"{name}.{extension}"
        write_generated(target_file, content)
        count += 1
    return count


# ── Copilot instructions (VS Code) ──────────────────────────────────────────


def build_copilot_instructions() -> str:
    """Construir .github/copilot-instructions.md desde platform + gates + operating model."""
    platform = read_text(AGENTS_DIR / "rules" / "platform.md")
    gates = read_text(AGENTS_DIR / "rules" / "mandatory-gates.md")
    body = f"""# ARASAAC Social MCP Platform — Instrucciones Copilot

Este repositorio usa packs agenticos multi-IDE con fuente canónica en `.agents/`.
Modelo operativo completo: `.agents/00_OPERATING_MODEL.md`.

## Modelo operativo

- **5 agentes-fase**: `spec`, `build`, `verify`, `docs`, `release`.
- **25 personas** de dominio invocadas internamente (no seleccionables en la UI).
- **10 skills** con procedimiento ejecutable.
- **4 workflows** (1 canónico + 3 de negocio).
- **4 prompts** parametrizables: `/new-spec`, `/implement-task`, `/verify-change`, `/archive-change`.
- **3 gates críticos** en `.agents/rules/mandatory-gates.md`.

## Reglas absolutas (platform)

{platform}

## Gates críticos (resumen)

{gates}

## Packs por IDE (todos generados desde `.agents/`)

- **Cursor:** `.cursor/`
- **Codex:** `.codex/`
- **Claude Code:** `.claude/`
- **OpenCode:** `.opencode/`
- **VS Code / Copilot:** `.github/` (este pack)
- **Obsidian (referencia humana):** `docs/obsidian/agent-pack/`

## Documentación

- `AGENTS.md` — reglas del repositorio.
- `.agents/00_OPERATING_MODEL.md` — definición operativa completa.
- `docs/agents/multi-ide-agent-packs.md` — guía multi-IDE.

**Nunca edites archivos generados; edita `.agents/` y ejecuta `python3 scripts/sync_agent_packs.py`.**
"""
    return body


# ── Obsidian vault (humano) ─────────────────────────────────────────────────


def build_obsidian_index(catalogs: dict) -> str:
    lines = [
        "---",
        "tags: [agent-pack, moc]",
        "---",
        "",
        "# Agent Pack — Índice",
        "",
        "Vault de referencia humana. Fuente canónica: `.agents/`.",
        "",
        "## Modelo operativo",
        "",
        "- [[00 Operating Model]]",
        "",
        "## Agentes (5 fases)",
        "",
    ]
    for a in catalogs["agents"]["agents"]:
        lines.append(f"- [[Agente {a['name']}]] — {a['title']}")
    lines += ["", "## Personas (25 de dominio)", ""]
    for p in catalogs["personas"]["personas"]:
        lines.append(f"- [[Persona {p['name']}]] — {p['role']}")
    lines += ["", "## Skills (10)", ""]
    for s in catalogs["skills"]["skills"]:
        lines.append(f"- [[Skill {s['name']}]] — {s.get('description', s['name'])}")
    lines += ["", "## Workflows (4)", ""]
    for w in catalogs["workflows"]["workflows"]:
        subtitle = w.get("title") or w.get("description") or w["name"]
        lines.append(f"- [[Workflow {w['name']}]] — {subtitle}")
    lines += ["", "## Prompts (4)", ""]
    for pr in catalogs["prompts"]["prompts"]:
        cmd = pr["slash_command"].lstrip("/")
        lines.append(f"- [[Prompt {pr['name']}]] — `/{cmd}`")
    lines += ["", "## Reglas", ""]
    for r in ("platform", "mandatory-gates", "backend", "frontend", "mcp", "export-license"):
        lines.append(f"- [[Regla {r}]]")
    return "\n".join(lines) + "\n"


# ── Orquestación por IDE ────────────────────────────────────────────────────


def sync_target(target_key: str, config: dict, catalogs: dict) -> dict[str, int]:
    """Regenerar el pack de un IDE target."""
    t = config["targets"][target_key]
    counts: dict[str, int] = {}

    # 1. Agents
    counts["agents"] = copy_canonical_files(
        AGENTS_DIR / "agents", ROOT / t["agents_path"], pattern="*.agent.md"
    )

    # 2. Personas
    counts["personas"] = copy_canonical_files(
        AGENTS_DIR / "personas", ROOT / t["personas_path"], pattern="*.persona.md"
    )

    # 3. Skills (recursive)
    counts["skills"] = copy_canonical_files(
        AGENTS_DIR / "skills", ROOT / t["skills_path"], recursive=True
    )

    # 4. Workflows
    counts["workflows"] = copy_canonical_files(
        AGENTS_DIR / "workflows", ROOT / t["workflows_path"], pattern="*.workflow.md"
    )

    # 5. Prompts / slash-commands (ubicación varía por IDE)
    prompts_path_key = "commands_path" if "commands_path" in t else "prompts_path"
    if prompts_path_key in t:
        extension = "md" if prompts_path_key == "commands_path" else "prompt.md"
        counts["prompts"] = write_prompts(
            catalogs["prompts"]["prompts"], ROOT / t[prompts_path_key], extension=extension
        )

    # 6. Rules
    if target_key == "cursor":
        counts["rules"] = write_rules(ROOT / t["rules_path"], extension="mdc")
    elif target_key == "vscode":
        # Copilot: instructions/*.instructions.md con applyTo
        counts["rules"] = write_rules(
            ROOT / t["instructions_subpath"], extension="instructions.md", add_apply_to=True
        )
        # Global copilot-instructions.md
        copilot_content = build_copilot_instructions()
        write_generated(ROOT / t["instructions_path"], copilot_content)
    else:
        counts["rules"] = write_rules(ROOT / t["rules_path"], extension="md")

    return counts


def sync_obsidian(config: dict, catalogs: dict) -> dict[str, int]:
    t = config["targets"]["obsidian"]
    vault = ROOT / t["path"]
    clean_dir(vault)

    counts = {"agents": 0, "personas": 0, "skills": 0, "workflows": 0, "prompts": 0, "rules": 0}

    # Índice
    write_generated(vault / "00-Indice.md", build_obsidian_index(catalogs))

    # Copiar canónicos con wikilinks-friendly names
    for entry in catalogs["agents"]["agents"]:
        src = AGENTS_DIR / "agents" / f"{entry['name']}.agent.md"
        write_generated(vault / "agents" / f"Agente {entry['name']}.md", read_text(src))
        counts["agents"] += 1

    for entry in catalogs["personas"]["personas"]:
        src = AGENTS_DIR / "personas" / f"{entry['name']}.persona.md"
        if src.exists():
            write_generated(vault / "personas" / f"Persona {entry['name']}.md", read_text(src))
            counts["personas"] += 1

    for entry in catalogs["skills"]["skills"]:
        src = AGENTS_DIR / "skills" / entry["name"] / "SKILL.md"
        if src.exists():
            write_generated(vault / "skills" / f"Skill {entry['name']}.md", read_text(src))
            counts["skills"] += 1

    for entry in catalogs["workflows"]["workflows"]:
        src = AGENTS_DIR / "workflows" / f"{entry['name']}.workflow.md"
        if src.exists():
            write_generated(vault / "workflows" / f"Workflow {entry['name']}.md", read_text(src))
            counts["workflows"] += 1

    for entry in catalogs["prompts"]["prompts"]:
        src = AGENTS_DIR / "prompts" / f"{entry['name']}.prompt.md"
        if src.exists():
            write_generated(vault / "prompts" / f"Prompt {entry['name']}.md", read_text(src))
            counts["prompts"] += 1

    for rule in ("platform", "mandatory-gates", "backend", "frontend", "mcp", "export-license"):
        src = AGENTS_DIR / "rules" / f"{rule}.md"
        if src.exists():
            write_generated(vault / "rules" / f"Regla {rule}.md", read_text(src))
            counts["rules"] += 1

    # Operating model
    write_generated(
        vault / "00 Operating Model.md",
        read_text(AGENTS_DIR / "00_OPERATING_MODEL.md"),
    )

    return counts


# ── Main ────────────────────────────────────────────────────────────────────


def main() -> None:
    config = load_yaml("packs")
    catalogs = {
        "agents": load_yaml("agents"),
        "personas": load_yaml("personas"),
        "skills": load_yaml("skills"),
        "workflows": load_yaml("workflows"),
        "prompts": load_yaml("prompts"),
    }

    print(f"🔄 Regenerando packs desde {AGENTS_DIR.relative_to(ROOT)}/\n")

    for target_key in ("cursor", "codex", "claude", "opencode", "vscode"):
        counts = sync_target(target_key, config, catalogs)
        label = config["targets"][target_key]["label"]
        summary = " ".join(f"{k}={v}" for k, v in counts.items())
        print(f"✅ {label:<28} {summary}")

    counts = sync_obsidian(config, catalogs)
    summary = " ".join(f"{k}={v}" for k, v in counts.items())
    print(f"✅ {'Obsidian':<28} {summary}")

    print("\n✔ Todos los packs regenerados.")
    print("→ Ejecuta: python3 scripts/verify_agent_packs_sync.py")


if __name__ == "__main__":
    main()
