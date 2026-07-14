#!/usr/bin/env python3
"""Fail if IDE agent packs are out of sync with canonical .agents/ (v2).

Estrategia (design 0036 §9):
1. Ejecutar `sync_agent_packs.py`.
2. Comprobar con `git diff --quiet` sobre GENERATED_PATHS.
3. Verificar 9 invariantes estructurales:
   I1: cada IDE tiene los 5 agentes-fase
   I2: cada IDE tiene 25 personas
   I3: cada IDE tiene 10 skills
   I4: cada IDE tiene 4 workflows
   I5: cada IDE tiene 4 prompts/commands
   I6: `.github/copilot-instructions.md` referencia los 10 rules absolutos
   I7: cada archivo generado empieza por el header canónico
   I8: `.agents/00_OPERATING_MODEL.md` existe
   I9: `.agents/rules/mandatory-gates.md` existe (fuente única de gates)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Rutas que deben quedar iguales tras un sync (bit-exact).
GENERATED_PATHS = [
    ".cursor",
    ".codex",
    ".claude",
    ".opencode",
    ".github/agents",
    ".github/personas",
    ".github/skills",
    ".github/workflows-agents",
    ".github/prompts",
    ".github/instructions",
    ".github/copilot-instructions.md",
    "docs/obsidian/agent-pack",
]

# Los 6 IDE targets (base_path, tiene commands o prompts)
IDE_TARGETS = [
    (".cursor", "commands"),
    (".codex", "prompts"),
    (".claude", "commands"),
    (".opencode", "commands"),
    (".github", "prompts"),
]

GENERATED_HEADER = "<!-- generated from .agents/ — do not edit manually -->"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def check_invariants() -> list[str]:
    errors: list[str] = []

    # I8, I9 — fuentes canónicas presentes
    if not (ROOT / ".agents/00_OPERATING_MODEL.md").exists():
        errors.append("I8: falta .agents/00_OPERATING_MODEL.md")
    if not (ROOT / ".agents/rules/mandatory-gates.md").exists():
        errors.append("I9: falta .agents/rules/mandatory-gates.md")

    # I1-I5 — conteos por IDE
    for base, prompt_key in IDE_TARGETS:
        base_path = ROOT / base
        # I1
        agents = list((base_path / "agents").glob("*.agent.md")) if (base_path / "agents").exists() else []
        if len(agents) != 5:
            errors.append(f"I1 [{base}]: se esperaban 5 agentes, hay {len(agents)}")
        # I2
        personas_dir = base_path / "personas"
        personas = list(personas_dir.glob("*.persona.md")) if personas_dir.exists() else []
        if len(personas) != 25:
            errors.append(f"I2 [{base}]: se esperaban 25 personas, hay {len(personas)}")
        # I3
        skills_dir = base_path / "skills"
        skills = [d for d in skills_dir.iterdir() if d.is_dir()] if skills_dir.exists() else []
        if len(skills) != 10:
            errors.append(f"I3 [{base}]: se esperaban 10 skills, hay {len(skills)}")
        # I4
        wf_dir = base_path / ("workflows-agents" if base == ".github" else "workflows")
        wfs = list(wf_dir.glob("*.workflow.md")) if wf_dir.exists() else []
        if len(wfs) != 4:
            errors.append(f"I4 [{base}]: se esperaban 4 workflows, hay {len(wfs)}")
        # I5
        prompts_dir = base_path / prompt_key
        prompt_ext = "*.md" if prompt_key == "commands" else "*.prompt.md"
        prompts = list(prompts_dir.glob(prompt_ext)) if prompts_dir.exists() else []
        if len(prompts) != 4:
            errors.append(f"I5 [{base}/{prompt_key}]: se esperaban 4 prompts, hay {len(prompts)}")

    # I6 — copilot-instructions referencia gates
    copilot = ROOT / ".github/copilot-instructions.md"
    if copilot.exists():
        text = copilot.read_text(encoding="utf-8")
        for keyword in ("CC BY-NC-SA", "revisión humana", "atribución", "MCP", "OpenSpec"):
            if keyword not in text:
                errors.append(f"I6: copilot-instructions.md no menciona '{keyword}'")
    else:
        errors.append("I6: falta .github/copilot-instructions.md")

    # I7 — header canónico en archivos generados (muestra representativa)
    sample_paths = [
        ROOT / ".cursor/agents/spec.agent.md",
        ROOT / ".claude/skills/openspec-lifecycle/SKILL.md",
        ROOT / ".github/personas/backend.persona.md",
        ROOT / ".codex/workflows/spec-build-verify.workflow.md",
    ]
    for p in sample_paths:
        if not p.exists():
            errors.append(f"I7: falta archivo esperado {p.relative_to(ROOT)}")
            continue
        first_line = p.read_text(encoding="utf-8").splitlines()[0] if p.stat().st_size else ""
        if first_line.strip() != GENERATED_HEADER:
            errors.append(f"I7: {p.relative_to(ROOT)} no comienza con header canónico")

    return errors


def main() -> int:
    # Paso 1: ejecutar sync
    sync = run([sys.executable, "scripts/sync_agent_packs.py"])
    if sync.returncode != 0:
        print("❌ Falló scripts/sync_agent_packs.py", file=sys.stderr)
        if sync.stdout:
            print(sync.stdout, file=sys.stderr)
        if sync.stderr:
            print(sync.stderr, file=sys.stderr)
        return sync.returncode

    # Paso 2: git diff sobre GENERATED_PATHS
    diff = run(["git", "diff", "--quiet", "--"] + GENERATED_PATHS)
    diff_ok = diff.returncode == 0

    # Paso 3: invariantes
    errors = check_invariants()

    if diff_ok and not errors:
        print("✅ Packs en sync con .agents/ y todos los invariantes se cumplen.")
        return 0

    if not diff_ok:
        print(
            "❌ Los packs generados están desincronizados con .agents/.\n"
            "Edita SOLO archivos en .agents/ y ejecuta:\n"
            "  python3 scripts/sync_agent_packs.py\n\n"
            "Diff resumen:",
            file=sys.stderr,
        )
        stat = run(["git", "diff", "--stat", "--"] + GENERATED_PATHS)
        if stat.stdout:
            print(stat.stdout, file=sys.stderr)

    if errors:
        print("\n❌ Invariantes rotos:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
