<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: f0b86405dee2 -->
---
name: verify-change
invokes_agent: verify
slash_command: /verify-change
parameters:
  - change_id
description: Verificar tests, lint, typecheck, a11y y los 3 gates críticos sobre una change.
---

# Prompt: /verify-change

Actúa como el **agente `verify`** definido en `.agents/agents/verify.agent.md`.

## Contexto de invocación

Voy a verificar una change antes de docs/release.

- **Change ID**: `{{change_id}}`

## Tu tarea

1. Confirma que todas las tasks de `openspec/changes/{{change_id}}-*/tasks.md` están `[x]`. Si no, para y lista pendientes.
2. Ejecuta en orden:
   - `make lint`
   - `make typecheck`
   - `make test`
   - Si toca frontend: `pnpm --filter web test` + `pnpm --filter web test:visual`
   - Si toca MCP: contract tests de tools/resources.
3. Aplica la skill [`compliance-scan`](../skills/compliance-scan/SKILL.md) sobre la change:
   - Gate `license` (crítico).
   - Gate `privacy` (crítico).
   - Pictogram IDs reales, densidad, plain-language, non-commercial.
4. Aplica la skill [`a11y-audit`](../skills/a11y-audit/SKILL.md) si toca `apps/web/**` o `packages/ui/**`.
5. Aplica la skill [`human-review-gate`](../skills/human-review-gate/SKILL.md) si la change produce materiales exportables.
6. Consulta las personas transversales (`qa`, `test-automation`, `security`, `observability`).
7. Emite un **dictamen estructurado**:
   ```md
   ## Verify report — {{change_id}}
   - Tests: ✅ / ❌
   - Lint/Typecheck: ✅ / ❌
   - Compliance: ✅ / ❌ (findings)
   - A11y: ✅ / ⚠️ / ❌
   - Human review: ✅ / ⏳ / ❌
   - Personas consultadas: …
   - **Decisión**: PROCEDER / BLOQUEAR
   ```

## Restricciones

- **No modifiques código** en esta fase. Si algo falla, sugiere volver a `/implement-task`.
- No aprobar con FAIL en gates críticos.
- No silenciar warnings de axe sin justificación técnica.

## Referencias

- Agente: [`verify.agent.md`](../agents/verify.agent.md)
- Skills: [`compliance-scan`](../skills/compliance-scan/SKILL.md), [`a11y-audit`](../skills/a11y-audit/SKILL.md), [`human-review-gate`](../skills/human-review-gate/SKILL.md)
- Gates: [`mandatory-gates.md`](../rules/mandatory-gates.md)
