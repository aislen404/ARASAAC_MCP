import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.sync_obsidian_vault import (  # noqa: E402
    MANIFEST_NAME,
    SyncError,
    synchronize,
)


def create_repository(root: Path) -> Path:
    write(root / "README.md", "# Proyecto\n")
    write(root / "AGENTS.md", "# Reglas\n")
    write(root / "NOTICE-ARASAAC.md", "# Licencia\n")
    write(root / "docs/obsidian/ARASAAC_Project-Index.md", "# Inicio\n")
    write(root / "docs/architecture/design.md", "# Diseño\n")
    write(root / "docs/obsidian/agent-pack/README.md", "# Pack\n")
    write(root / "docs/obsidian/agent-pack/README 3.md", "# Copia de conflicto\n")
    write(root / "openspec/changes/0001/spec.md", "# Spec\n")
    write(root / ".agents/README.md", "# Agentes\n")
    write(root / ".agents/skills/example/SKILL.md", "# Skill\n")
    write(root / "docs/.DS_Store", "ignored")
    return root


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_initial_sync_maps_visible_knowledge_and_writes_manifest(
    tmp_path: Path,
) -> None:
    repository = create_repository(tmp_path / "repository")
    vault = tmp_path / "vault"
    (repository / "docs/link.md").symlink_to(repository / "README.md")

    result = synchronize(vault, repository_root=repository)

    assert result.in_sync is True
    assert (vault / "00-Inicio.md").read_text() == "# Inicio\n"
    assert (vault / "Proyecto/README.md").read_text() == "# Proyecto\n"
    assert (vault / "Proyecto/Agentes/README.md").read_text() == "# Agentes\n"
    assert not (vault / "Proyecto/.agents").exists()
    assert not (vault / "Proyecto/docs/.DS_Store").exists()
    assert not (vault / "Proyecto/docs/link.md").exists()
    assert not (vault / "Proyecto/docs/obsidian/agent-pack/README 3.md").exists()
    assert (vault / "Proyecto/docs/obsidian/agent-pack/README.md").exists()
    manifest = json.loads((vault / MANIFEST_NAME).read_text())
    assert manifest["schema_version"] == 1
    assert "Proyecto/Agentes/skills/example/SKILL.md" in manifest["files"]

    second = synchronize(vault, repository_root=repository)
    assert second.copied == 0
    assert second.removed == 0


def test_check_detects_source_and_destination_drift(tmp_path: Path) -> None:
    repository = create_repository(tmp_path / "repository")
    vault = tmp_path / "vault"
    synchronize(vault, repository_root=repository)

    assert synchronize(
        vault,
        repository_root=repository,
        check=True,
    ).in_sync

    write(repository / "README.md", "# Cambio\n")
    source_drift = synchronize(vault, repository_root=repository, check=True)
    assert source_drift.in_sync is False
    assert "manifiesto" in " ".join(source_drift.problems)

    synchronize(vault, repository_root=repository)
    write(vault / "Proyecto/README.md", "# Edición manual no permitida aquí\n")
    destination_drift = synchronize(vault, repository_root=repository, check=True)
    assert destination_drift.in_sync is False
    assert "Contenido distinto" in " ".join(destination_drift.problems)


def test_check_does_not_write_and_rejects_destination_symlink(
    tmp_path: Path,
) -> None:
    repository = create_repository(tmp_path / "repository")
    vault = tmp_path / "vault"
    synchronize(vault, repository_root=repository)
    paths_before = sorted(path.relative_to(vault) for path in vault.rglob("*"))

    assert synchronize(vault, repository_root=repository, check=True).in_sync
    assert sorted(path.relative_to(vault) for path in vault.rglob("*")) == paths_before

    outside = tmp_path / "outside.md"
    outside.write_text("# Proyecto\n", encoding="utf-8")
    destination = vault / "Proyecto/README.md"
    destination.unlink()
    destination.symlink_to(outside)

    checked = synchronize(vault, repository_root=repository, check=True)
    assert checked.in_sync is False
    assert "symlink" in " ".join(checked.problems)
    with pytest.raises(SyncError, match="symlink"):
        synchronize(vault, repository_root=repository)


def test_sync_removes_only_stale_managed_files_and_preserves_notes(
    tmp_path: Path,
) -> None:
    repository = create_repository(tmp_path / "repository")
    vault = tmp_path / "vault"
    synchronize(vault, repository_root=repository)
    manual_note = vault / "Notas/Decisiones del equipo.md"
    write(manual_note, "# Nota libre\n")

    (repository / "docs/architecture/design.md").unlink()
    result = synchronize(vault, repository_root=repository)

    assert result.removed == 1
    assert not (vault / "Proyecto/docs/architecture/design.md").exists()
    assert manual_note.read_text() == "# Nota libre\n"


def test_sync_rejects_manifest_that_targets_unmanaged_note(tmp_path: Path) -> None:
    repository = create_repository(tmp_path / "repository")
    vault = tmp_path / "vault"
    vault.mkdir()
    manual_note = vault / "Notas/Privada.md"
    write(manual_note, "# Conservar\n")
    (vault / MANIFEST_NAME).write_text(
        json.dumps(
            {
                "schema_version": 1,
                "files": {"Notas/Privada.md": "0" * 64},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(SyncError, match="ruta no permitida"):
        synchronize(vault, repository_root=repository)

    assert manual_note.read_text() == "# Conservar\n"


def test_check_reports_missing_vault_without_creating_it(tmp_path: Path) -> None:
    repository = create_repository(tmp_path / "repository")
    vault = tmp_path / "missing"

    result = synchronize(vault, repository_root=repository, check=True)

    assert result.in_sync is False
    assert not vault.exists()


def test_hooks_are_non_blocking_and_make_targets_are_declared(
    tmp_path: Path,
) -> None:
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")

    assert "obsidian-sync:" in makefile
    assert "obsidian-sync-check:" in makefile
    assert "obsidian-hooks-install:" in makefile
    for hook_name in ("post-commit", "post-merge"):
        hook = ROOT / ".githooks" / hook_name
        content = hook.read_text(encoding="utf-8")
        assert content.startswith("#!/bin/sh")
        assert 'exit 0' in content

        blocker = tmp_path / f"{hook_name}-not-a-directory"
        blocker.write_text("block", encoding="utf-8")
        environment = os.environ | {
            "OBSIDIAN_VAULT_PATH": str(blocker / "vault"),
        }
        completed = subprocess.run(
            [str(hook)],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0
        assert "Aviso" in completed.stderr
