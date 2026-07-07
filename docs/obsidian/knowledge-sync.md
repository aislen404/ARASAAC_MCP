# Sincronización de conocimiento con Obsidian

## Bóveda

La bóveda predeterminada es:

```text
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/ARASAAC_Project
```

Puede cambiarse sin modificar el repositorio:

```bash
OBSIDIAN_VAULT_PATH="/ruta/a/otra/boveda" make obsidian-sync
```

## Contenido

El sincronizador publica únicamente:

- `README.md`, `AGENTS.md` y `NOTICE-ARASAAC.md`;
- `docs/`;
- `openspec/`;
- `.agents/`, visible en Obsidian como `Proyecto/Agentes/`;
- el índice `00-Inicio.md`.

No publica código, `.env`, secretos, `.git`, pictogramas, dependencias, builds,
caches o `.DS_Store`.

## Cambios recientes (2026-07-06)

- OpenSpecs MVP archivadas en `openspec/changes/archive/`.
- Documentación de arquitectura MCP dual: `docs/architecture/mcp-dual-surface.md`.
- Dossier institucional: `docs/compliance/arasaac-validation-dossier.md`.
- Plan de pruebas Release 2: `docs/testing/test-plan-release2.md`.

Ejecutar `make obsidian-sync` tras actualizar documentación en el repositorio.

## Comandos

Actualizar la bóveda:

```bash
make obsidian-sync
```

Comprobarla sin escribir:

```bash
make obsidian-sync-check
```

Activar los hooks solo para este repositorio:

```bash
make obsidian-hooks-install
```

La activación configura `core.hooksPath=.githooks`. `post-commit` y `post-merge`
intentan sincronizar; si iCloud no está disponible, muestran una advertencia pero
no bloquean Git.

## Garantías

`.arasaac-sync-manifest.json` contiene los hashes SHA-256 de los archivos
administrados. El sincronizador:

- escribe mediante reemplazo atómico;
- serializa ejecuciones mediante un lock;
- elimina solo rutas presentes en el manifiesto anterior;
- rechaza rutas fuera de la allowlist;
- conserva notas manuales no administradas.

Las copias de conflicto numeradas que macOS/iCloud pueda crear dentro del pack
generado de agentes (`nombre 2.md`, `nombre 3.md`, etc.) no se sincronizan si
existe el archivo canónico hermano.

No edites directamente archivos bajo `Proyecto/` si esperas conservar el cambio:
el repositorio es la fuente de verdad. Guarda notas propias fuera de esa carpeta,
por ejemplo en `Notas/`.

## Recuperación

Si una sincronización queda desactualizada:

```bash
make obsidian-sync
make obsidian-sync-check
```

Si cambia la ubicación de la bóveda, define `OBSIDIAN_VAULT_PATH`. Para desactivar
los hooks locales:

```bash
git config --unset core.hooksPath
```
