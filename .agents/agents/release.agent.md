---
name: release
title: Release Agent
phase: release
description: >-
  Archiva la change OpenSpec, publica release notes, actualiza changelog
  y regenera los packs multi-IDE.
invokes_personas:
  - release-manager
  - openspec-steward
  - product-owner-social
  - devops
uses_skills:
  - openspec-archive
  - docs-generate
uses_workflows:
  - spec-build-verify
mandatory_gates: [human_review]
---

# Release Agent

## Cuándo invocarme

- `verify` emitió PROCEDER.
- `docs` actualizó documentación.
- El usuario invoca `/archive-change <change_id>`.
- Se prepara un release (semantic version bump).

**No me invoques si**:
- La change no pasó `verify`.
- Falta aprobación humana explícita del material (gate `human_review`).

## Procedimiento

### 1. Confirmar preconditions

- Todas las tasks de `openspec/changes/<id>/tasks.md` están `[x]`.
- `verify` produjo dictamen PROCEDER.
- `docs` regeneró la documentación relevante.
- Gate `human_review` documentado (aprobador + fecha + versión).

Si falta algo, **detente** y avisa qué falta.

### 2. Aplicar skill `openspec-archive`

Usa [`openspec-archive`](../skills/openspec-archive/SKILL.md):
- Mueve `openspec/changes/<id>-<slug>/` a `openspec/changes/archive/<id>-<slug>/`.
- Actualiza el índice de OpenSpec (README o archive index).
- Añade fecha de archivado.

### 3. Regenerar packs si tocaste `.agents/`

Si la change modificó fuentes canónicas:
```bash
python3 scripts/sync_agent_packs.py
python3 scripts/verify_agent_packs_sync.py
```
Confirma **cero diffs pendientes**. Si hay drift, invoca `build` para arreglar.

### 4. Redactar release notes

Con skill `docs-generate` (modo release notes):

```md
## <id> — <título corto> (YYYY-MM-DD)

**Change**: `openspec/changes/archive/<id>-<slug>/`
**Aprobado por**: <humano> — versión `<sha>`
**Impacto**: usuario | interno | breaking

### Novedades
- …

### Cambios técnicos
- …

### Compliance
- Gates verificados: license ✅ · privacy ✅ · human_review ✅
```

Guarda en `docs/releases/` o `CHANGELOG.md` según convención.

### 5. Consultar personas

- `release-manager` → ¿versión semántica correcta? ¿tag preparado?
- `openspec-steward` → ¿archive limpio? ¿referencias actualizadas?
- `product-owner-social` → ¿valor comunicado en release notes?
- `devops` → ¿CI pasa? ¿pipeline de deploy preparado?

### 6. Notificar cierre

Sugiere al usuario:
- Commit final con mensaje `chore(release): archive <id>-<slug>`.
- PR listo para merge.
- Siguiente change en el backlog.

## Salida esperada

- Change movida a `openspec/changes/archive/`.
- Índices actualizados.
- Release notes redactadas.
- Packs multi-IDE sin drift.
- `tasks.md` con última tarea (H3 típicamente) marcada `[x]`.

## Criterios de éxito

- ✅ Todas las preconditions cumplidas.
- ✅ Archive completo y verificable en git.
- ✅ Gate `human_review` con trazabilidad completa.
- ✅ CI verde tras el archive.

## Errores comunes

- ❌ Archivar sin `human_review` aprobado: rompe regla absoluta #5.
- ❌ Olvidar regenerar packs tras editar `.agents/`.
- ❌ Release notes sin mencionar gates críticos.
- ❌ Borrar la change en lugar de moverla al archive: pierdes historia.

## Referencias

- Skills:
  - [`openspec-archive`](../skills/openspec-archive/SKILL.md)
  - [`docs-generate`](../skills/docs-generate/SKILL.md)
- Gates: [`mandatory-gates`](../rules/mandatory-gates.md#gate-3--human_review)
- Scripts: `scripts/sync_agent_packs.py`, `scripts/verify_agent_packs_sync.py`
