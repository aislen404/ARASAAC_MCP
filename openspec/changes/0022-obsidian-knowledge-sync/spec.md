# Spec — 0022-obsidian-knowledge-sync

## Selección

- Solo se sincronizan `README.md`, `AGENTS.md`, `NOTICE-ARASAAC.md`, `docs/`,
  `openspec/` y `.agents/`.
- `.agents/` aparece como `Proyecto/Agentes/`.
- No se copian `.git`, `.env`, código, pictogramas, dependencias, builds, caches ni
  `.DS_Store`.

## Integridad

- Cada archivo administrado aparece en un manifiesto versionado por schema con su
  SHA-256.
- Una segunda sincronización sin cambios no reescribe contenido.
- `--check` termina con cero solo si destino y manifiesto coinciden.
- Las escrituras incompletas no sustituyen el archivo válido.
- Dos ejecuciones no escriben simultáneamente.

## Preservación

- Una nota manual fuera del manifiesto nunca se modifica ni elimina.
- Un archivo eliminado del repositorio se elimina del destino solo si estaba
  registrado como administrado.
- El índice de inicio se administra desde una plantilla del repositorio.

## Hooks

- Los hooks se ejecutan después de commit y merge.
- Un fallo de iCloud produce una advertencia y código cero.
- La instalación afecta únicamente al repositorio actual.
- Existe un comando manual independiente de los hooks.

## Verificación

- Tests temporales cubren sincronización inicial, actualización, check con drift,
  archivo obsoleto, nota manual, symlink y exclusiones.
- La sincronización real deja `ARASAAC_Project` en estado verificado.
- Los gates existentes, OpenSpec y agent packs continúan pasando.
