# Design — 0022-obsidian-knowledge-sync

## Topología

```text
repositorio
  ├── README.md, AGENTS.md, NOTICE-ARASAAC.md
  ├── docs/
  ├── openspec/
  └── .agents/
        │
        ▼
scripts/sync_obsidian_vault.py
        │ manifiesto + SHA-256 + escritura atómica
        ▼
ARASAAC_Project/
  ├── 00-Inicio.md
  ├── .arasaac-sync-manifest.json
  └── Proyecto/
      ├── README.md, AGENTS.md, NOTICE-ARASAAC.md
      ├── docs/
      ├── openspec/
      └── Agentes/
```

`.agents/` se publica como `Agentes/` porque Obsidian no indexa normalmente
carpetas ocultas. El índice se genera desde una plantilla versionada.

## Seguridad de archivos

- La ruta se obtiene de `OBSIDIAN_VAULT_PATH` o se deriva de la ruta estándar de
  Obsidian en iCloud; no se codifica un nombre de usuario.
- Las fuentes forman una allowlist cerrada.
- Se ignoran symlinks, `.DS_Store`, temporales y archivos ocultos no aprobados.
- Las escrituras usan archivo temporal y `os.replace`.
- Un lock evita ejecuciones concurrentes.
- El manifiesto registra ruta relativa y hash, nunca contenido ni secretos.
- Solo se elimina una ruta si estaba en el manifiesto anterior y deja de formar
  parte de la allowlist. Las notas no administradas se conservan.

## Hooks

`.githooks/post-commit` y `.githooks/post-merge` invocan el script en modo
silencioso. Capturan cualquier error, muestran una advertencia breve y terminan
con código cero. La activación local usa:

```bash
git config core.hooksPath .githooks
```

Los hooks no se activan globalmente ni se escriben directamente en `.git/hooks`.

## Operación

- `make obsidian-sync`: actualiza la bóveda.
- `make obsidian-sync-check`: verifica hashes y manifiesto sin escribir.
- `make obsidian-hooks-install`: configura los hooks solo en este repositorio.

Los tests usan una bóveda temporal y no acceden a iCloud.
