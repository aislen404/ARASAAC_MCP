---
name: openspec-archive
description: Cerrar tasks.md, mover a openspec/changes/archive/, actualizar índices y release notes.
inputs:
  - change_id
outputs:
  - openspec/changes/archive/<id>-<slug>/  (moved)
  - openspec/archive-index updated
  - CHANGELOG entry
invoked_by_agents: [release]
gates: []
---

# Skill: openspec-archive

## Cuándo usarla
- La change pasó `verify` con PROCEDER y `docs` actualizó documentación.
- Existe evidencia de `human_review` aprobada.

## Procedimiento paso a paso

1. **Verificar preconditions**:
   - `openspec/changes/<id>-<slug>/tasks.md` con todas las tasks `[x]`.
   - Verify report guardado o mencionado en el PR.
   - Human review aprobada (si aplica).
2. **Mover carpeta**:
   ```bash
   git mv openspec/changes/<id>-<slug> openspec/changes/archive/<id>-<slug>
   ```
3. **Añadir metadata final** en un archivo `ARCHIVED.md` dentro de la carpeta archivada:
   ```md
   # Archived on YYYY-MM-DD
   - Verify: ✅
   - Human review: <nombre> — <fecha>
   - Release: v<x.y.z>
   ```
4. **Actualizar índice** en `openspec/changes/archive/README.md` (crear si no existe).
5. **Añadir entrada** en `CHANGELOG.md` bajo `## [Unreleased]` con formato Keep-a-Changelog.
6. **Regenerar packs** si la change tocó `.agents/`:
   ```bash
   python3 scripts/sync_agent_packs.py
   python3 scripts/verify_agent_packs_sync.py
   ```

## Ejemplo

```bash
git mv openspec/changes/0036-agent-system-refactor \
       openspec/changes/archive/0036-agent-system-refactor
```

## Errores comunes

- ❌ Borrar la carpeta en vez de moverla: se pierde la historia OpenSpec.
- ❌ Archivar sin actualizar `CHANGELOG`.
- ❌ Olvidar regenerar packs → CI falla en el siguiente PR.

## Ver también

- Skill: [`docs-generate`](../docs-generate/SKILL.md) para release notes.
