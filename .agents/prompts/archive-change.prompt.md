---
name: archive-change
invokes_agent: release
slash_command: /archive-change
parameters:
  - change_id
description: Archivar una change OpenSpec completada, actualizar índices y release notes.
---

# Prompt: /archive-change

Actúa como el **agente `release`** definido en `.agents/agents/release.agent.md`.

## Contexto de invocación

Voy a cerrar y archivar una change.

- **Change ID**: `{{change_id}}`

## Tu tarea

1. Verifica preconditions:
   - Todas las tasks de `openspec/changes/{{change_id}}-*/tasks.md` `[x]`.
   - `verify` produjo dictamen PROCEDER.
   - `docs` actualizó documentación relevante.
   - `human_review` documentado (reviewer + fecha + versión).
2. Aplica la skill [`openspec-archive`](../skills/openspec-archive/SKILL.md):
   - `git mv openspec/changes/{{change_id}}-<slug> openspec/changes/archive/{{change_id}}-<slug>`
   - Añade `ARCHIVED.md` con metadata de cierre.
   - Actualiza `openspec/changes/archive/README.md`.
3. Si la change tocó `.agents/`:
   - `python3 scripts/sync_agent_packs.py`
   - `python3 scripts/verify_agent_packs_sync.py`
   - Confirma zero drift.
4. Redacta release notes en `docs/releases/YYYY-MM-DD-<version>.md` con formato Keep-a-Changelog + sección "Compliance verificada (license · privacy · human_review)".
5. Actualiza `CHANGELOG.md` bajo `## [Unreleased]`.
6. Consulta personas: `release-manager`, `openspec-steward`, `product-owner-social`, `devops`.
7. Al terminar, resume:
   - Ruta final del archive.
   - Release notes creadas.
   - Estado de packs (zero drift).
   - Sugerencia: commit `chore(release): archive {{change_id}}-<slug>` y PR listo.

## Restricciones

- No archives sin `human_review` documentado.
- No borres la carpeta: **muévela** al archive.
- No omitas la regeneración de packs si tocaste `.agents/`.

## Referencias

- Agente: [`release.agent.md`](../agents/release.agent.md)
- Skills: [`openspec-archive`](../skills/openspec-archive/SKILL.md), [`docs-generate`](../skills/docs-generate/SKILL.md)
- Gates: [`mandatory-gates.md`](../rules/mandatory-gates.md#gate-3--human_review)
