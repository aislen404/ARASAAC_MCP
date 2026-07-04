#!/usr/bin/env python3
"""Fail if IDE agent packs are out of sync with canonical .agents/ source."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GENERATED_PATHS = [
    ".agents/README.md",
    ".agents/skills",
    ".cursor",
    ".codex/README.md",
    ".codex/agents",
    ".codex/prompts",
    ".codex/codex",
    ".codex/skills/skill_catalog.yaml",
    ".codex/workflows/workflow_catalog.yaml",
    ".claude",
    ".opencode",
    ".github/agents",
    ".github/prompts",
    ".github/instructions",
    ".github/copilot-instructions.md",
    "docs/obsidian/agent-pack",
]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    sync = run([sys.executable, "scripts/sync_agent_packs.py"])
    if sync.returncode != 0:
        print("Failed to run scripts/sync_agent_packs.py", file=sys.stderr)
        if sync.stdout:
            print(sync.stdout, file=sys.stderr)
        if sync.stderr:
            print(sync.stderr, file=sys.stderr)
        return sync.returncode

    diff = run(["git", "diff", "--quiet", "--"] + GENERATED_PATHS)
    if diff.returncode == 0:
        print("Agent packs are in sync with .agents/ canonical source.")
        return 0

    print(
        "ERROR: Generated agent packs are out of sync with .agents/.\n"
        "Edit only .agents/catalog/, .agents/content/, .agents/rules/ "
        "or .agents/02_AGENTES_SKILLS_WORKFLOWS_V2.md, then run:\n\n"
        "  python3 scripts/sync_agent_packs.py\n\n"
        "Diff summary:",
        file=sys.stderr,
    )
    stat = run(["git", "diff", "--stat", "--"] + GENERATED_PATHS)
    if stat.stdout:
        print(stat.stdout, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
