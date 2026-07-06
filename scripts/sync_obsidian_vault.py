#!/usr/bin/env python3
"""Synchronize governed project knowledge to the ARASAAC Obsidian vault."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_NAME = ".arasaac-sync-manifest.json"
SCHEMA_VERSION = 1
INDEX_SOURCE = "docs/obsidian/ARASAAC_Project-Index.md"
FILE_MAPPINGS = {
    "README.md": "Proyecto/README.md",
    "AGENTS.md": "Proyecto/AGENTS.md",
    "NOTICE-ARASAAC.md": "Proyecto/NOTICE-ARASAAC.md",
    INDEX_SOURCE: "00-Inicio.md",
}
DIRECTORY_MAPPINGS = {
    "docs": "Proyecto/docs",
    "openspec": "Proyecto/openspec",
    ".agents": "Proyecto/Agentes",
}
IGNORED_NAMES = frozenset({".DS_Store"})
CONFLICT_COPY_PATTERN = re.compile(r"^(?P<stem>.+) (?P<copy>[2-9][0-9]*)$")
MANAGED_EXACT = frozenset(FILE_MAPPINGS.values())
MANAGED_PREFIXES = tuple(f"{target}/" for target in DIRECTORY_MAPPINGS.values())


class SyncError(RuntimeError):
    """A controlled synchronization failure."""


@dataclass(frozen=True)
class SyncResult:
    copied: int
    removed: int
    checked: int
    in_sync: bool
    problems: tuple[str, ...] = ()


def default_vault_path() -> Path:
    configured = os.environ.get("OBSIDIAN_VAULT_PATH")
    if configured:
        return Path(configured).expanduser()
    return (
        Path.home()
        / "Library"
        / "Mobile Documents"
        / "iCloud~md~obsidian"
        / "Documents"
        / "ARASAAC_Project"
    )


def synchronize(
    vault: Path,
    *,
    repository_root: Path = ROOT,
    check: bool = False,
) -> SyncResult:
    repository_root = repository_root.resolve()
    vault = vault.expanduser().resolve()
    if check and not vault.is_dir():
        return SyncResult(
            copied=0,
            removed=0,
            checked=0,
            in_sync=False,
            problems=("La bóveda no existe.",),
        )
    if not check:
        vault.mkdir(parents=True, exist_ok=True)

    desired = collect_sources(repository_root)
    desired_hashes = {
        relative: sha256(source) for relative, source in desired.items()
    }

    with vault_lock(vault):
        manifest, manifest_problem = read_manifest(vault / MANIFEST_NAME)
        if check:
            return check_state(
                vault,
                desired_hashes,
                manifest,
                manifest_problem=manifest_problem,
            )
        if manifest_problem and (vault / MANIFEST_NAME).exists():
            raise SyncError(manifest_problem)

        copied = 0
        for relative, source in desired.items():
            destination = safe_destination(vault, relative)
            expected_hash = desired_hashes[relative]
            if destination.is_symlink():
                raise SyncError(f"Destino administrado es un symlink: {relative}.")
            if not destination.is_file() or sha256(destination) != expected_hash:
                atomic_copy(source, destination)
                if sha256(destination) != expected_hash:
                    raise SyncError(f"Falló la verificación de {relative}.")
                copied += 1

        previous_manifest_files = manifest.get("files")
        previous_files = (
            set(previous_manifest_files)
            if isinstance(previous_manifest_files, dict)
            else set()
        )
        stale = sorted(previous_files - set(desired))
        removed = 0
        for relative in stale:
            ensure_managed_path(relative)
            destination = safe_destination(vault, relative)
            if destination.is_symlink():
                raise SyncError(f"No se elimina un symlink administrado: {relative}.")
            if destination.exists():
                if not destination.is_file():
                    raise SyncError(f"La ruta administrada no es un archivo: {relative}.")
                destination.unlink()
                removed += 1

        remove_empty_managed_directories(vault)
        write_manifest(vault / MANIFEST_NAME, desired_hashes)
        return SyncResult(
            copied=copied,
            removed=removed,
            checked=len(desired),
            in_sync=True,
        )


def collect_sources(repository_root: Path) -> dict[str, Path]:
    collected: dict[str, Path] = {}
    for source_relative, target_relative in FILE_MAPPINGS.items():
        source = repository_root / source_relative
        if not source.is_file() or source.is_symlink():
            raise SyncError(f"Falta la fuente obligatoria: {source_relative}.")
        ensure_managed_path(target_relative)
        collected[target_relative] = source

    for source_relative, target_root in DIRECTORY_MAPPINGS.items():
        source_root = repository_root / source_relative
        if not source_root.is_dir() or source_root.is_symlink():
            raise SyncError(f"Falta el directorio obligatorio: {source_relative}.")
        for source in sorted(source_root.rglob("*")):
            if source.is_symlink() or not source.is_file():
                continue
            if source.name in IGNORED_NAMES:
                continue
            relative_source = source.relative_to(source_root)
            if is_generated_conflict_copy(source_root, relative_source):
                continue
            target = PurePosixPath(target_root, *relative_source.parts).as_posix()
            ensure_managed_path(target)
            collected[target] = source
    return collected


def is_generated_conflict_copy(source_root: Path, relative_source: Path) -> bool:
    if relative_source.parts[:2] != ("obsidian", "agent-pack"):
        return False
    match = CONFLICT_COPY_PATTERN.match(relative_source.stem)
    if match is None:
        return False
    canonical_name = f"{match.group('stem')}{relative_source.suffix}"
    canonical = source_root / relative_source.parent / canonical_name
    return canonical.is_file()


def check_state(
    vault: Path,
    desired_hashes: dict[str, str],
    manifest: dict[str, object],
    *,
    manifest_problem: str | None,
) -> SyncResult:
    problems: list[str] = []
    if manifest_problem:
        problems.append(manifest_problem)
    manifest_files = manifest.get("files", {})
    if not isinstance(manifest_files, dict):
        manifest_files = {}

    if manifest_files != desired_hashes:
        problems.append("El manifiesto no coincide con las fuentes actuales.")

    for relative, expected_hash in desired_hashes.items():
        destination = safe_destination(vault, relative)
        if destination.is_symlink():
            problems.append(f"Destino administrado es un symlink: {relative}.")
        elif not destination.is_file():
            problems.append(f"Falta {relative}.")
        elif sha256(destination) != expected_hash:
            problems.append(f"Contenido distinto en {relative}.")

    return SyncResult(
        copied=0,
        removed=0,
        checked=len(desired_hashes),
        in_sync=not problems,
        problems=tuple(problems),
    )


def read_manifest(path: Path) -> tuple[dict[str, object], str | None]:
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "files": {}}, None
    if path.is_symlink():
        return {}, "El manifiesto no puede ser un symlink."
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}, "El manifiesto de sincronización no es JSON válido."
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
        return {}, "Versión de manifiesto no soportada."
    files = payload.get("files")
    if not isinstance(files, dict):
        return {}, "El manifiesto no contiene un mapa de archivos válido."
    for relative, digest in files.items():
        if not isinstance(relative, str) or not isinstance(digest, str):
            return {}, "El manifiesto contiene entradas inválidas."
        try:
            ensure_managed_path(relative)
        except SyncError:
            return {}, "El manifiesto intenta administrar una ruta no permitida."
    return payload, None


def write_manifest(path: Path, files: dict[str, str]) -> None:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "source": "ARASAAC_MCP",
        "files": dict(sorted(files.items())),
    }
    atomic_write(
        path,
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )


def ensure_managed_path(relative: str) -> None:
    parsed = PurePosixPath(relative)
    if parsed.is_absolute() or ".." in parsed.parts or relative in {"", "."}:
        raise SyncError(f"Ruta administrada inválida: {relative}.")
    if relative not in MANAGED_EXACT and not relative.startswith(MANAGED_PREFIXES):
        raise SyncError(f"Ruta fuera de la allowlist: {relative}.")


def safe_destination(vault: Path, relative: str) -> Path:
    ensure_managed_path(relative)
    destination = vault.joinpath(*PurePosixPath(relative).parts)
    resolved_parent = destination.parent.resolve()
    if resolved_parent != vault and vault not in resolved_parent.parents:
        raise SyncError(f"La ruta escapa de la bóveda: {relative}.")
    return destination


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as stream:
        atomic_write(destination, stream.read())


def atomic_write(destination: Path, content: bytes) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def remove_empty_managed_directories(vault: Path) -> None:
    for target_root in DIRECTORY_MAPPINGS.values():
        root = vault / target_root
        if not root.is_dir():
            continue
        directories = sorted(
            (path for path in root.rglob("*") if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        )
        for directory in directories:
            try:
                directory.rmdir()
            except OSError:
                pass


@contextmanager
def vault_lock(vault: Path) -> Iterator[None]:
    lock_id = hashlib.sha256(str(vault).encode("utf-8")).hexdigest()[:20]
    lock_path = Path(tempfile.gettempdir()) / f"arasaac-obsidian-{lock_id}.lock"
    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(lock_path, flags, 0o600)
    with os.fdopen(descriptor, "a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def parse_args(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=default_vault_path())
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args(arguments)


def main(arguments: list[str] | None = None) -> int:
    options = parse_args(arguments)
    try:
        result = synchronize(options.vault, check=options.check)
    except (OSError, SyncError) as exc:
        print(f"Error de sincronización Obsidian: {exc}", file=sys.stderr)
        return 2
    if not result.in_sync:
        for problem in result.problems:
            print(f"- {problem}", file=sys.stderr)
        return 1
    if not options.quiet:
        action = "verificados" if options.check else "sincronizados"
        print(
            f"Obsidian: {result.checked} archivos {action}; "
            f"{result.copied} copiados; {result.removed} retirados."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
