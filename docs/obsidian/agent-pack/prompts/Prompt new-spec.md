<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: 9d2dc5616dc3 -->
---
name: new-spec
invokes_agent: spec
slash_command: /new-spec
parameters:
  - change_id
  - short_title
  - problem_summary
description: Crear una nueva change OpenSpec completa (proposal + design + tasks + spec).
---

# Prompt: /new-spec

Actúa como el **agente `spec`** definido en `.agents/agents/spec.agent.md`.

## Contexto de invocación

Voy a crear una nueva change OpenSpec.

- **Change ID**: `{{change_id}}` (ej: `0037`)
- **Slug**: `{{short_title}}` (ej: `guided-onboarding-tour`)
- **Problema en 1-3 frases**: `{{problem_summary}}`

## Tu tarea

1. Verifica que `openspec/changes/{{change_id}}-*` no exista aún. Si existe, propón siguiente ID libre.
2. Sigue el procedimiento completo del agente `spec` (`.agents/agents/spec.agent.md`).
3. Redacta los 4 archivos:
   - `openspec/changes/{{change_id}}-{{short_title}}/proposal.md`
   - `openspec/changes/{{change_id}}-{{short_title}}/design.md`
   - `openspec/changes/{{change_id}}-{{short_title}}/spec.md`
   - `openspec/changes/{{change_id}}-{{short_title}}/tasks.md`
4. Consulta las **personas invocadas** por el agente `spec` (ver frontmatter). Documenta hallazgos relevantes en `design.md` §Riesgos si un gate está en tensión.
5. Aplica la skill `openspec-lifecycle` y el criterio de `compliance-scan` (gates `license`, `privacy`, `human_review`).
6. Al terminar, resume:
   - Los 4 archivos creados.
   - Gates evaluados.
   - Sugerencia del siguiente comando (`/implement-task {{change_id}} A1` u otro).

## Restricciones

- No implementes código todavía. Este prompt solo produce spec.
- Si falta información en `{{problem_summary}}`, **pregunta antes de escribir**.
- Respeta las 10 reglas absolutas del proyecto (ver `AGENTS.md`).

## Referencias

- Agente: [`spec.agent.md`](../agents/spec.agent.md)
- Skill: [`openspec-lifecycle`](../skills/openspec-lifecycle/SKILL.md)
- Gates: [`mandatory-gates.md`](../rules/mandatory-gates.md)
