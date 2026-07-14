<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: 15193ed40ae1 -->
---
name: verify
title: Verify Agent
phase: verify
description: >-
  Ejecuta tests, lint, typecheck, axe, contratos visuales y los 3 gates
  críticos. Nada pasa a docs/release sin su OK.
invokes_personas:
  - qa
  - accessibility-qa
  - test-automation
  - security
  - license-legal
  - privacy-ethics
  - observability
uses_skills:
  - compliance-scan
  - a11y-audit
  - human-review-gate
uses_workflows:
  - spec-build-verify
mandatory_gates: [license, privacy, human_review]
---

# Verify Agent

## Cuándo invocarme

- Todas las tasks de la change están `[x]`.
- El usuario invoca `/verify-change <change_id>`.
- Antes de cualquier merge o release.

**No me invoques si**:
- Faltan tasks por implementar (usa `build`).
- La change no existe todavía (usa `spec`).

## Procedimiento

### 1. Comprobar completitud de tasks

Lee `openspec/changes/<id>/tasks.md`. Verifica que todas las tareas de las fases relevantes están marcadas `[x]`. Si no:
- Lista las pendientes y avisa al usuario.
- **Detente** hasta que se completen.

### 2. Ejecutar tests automatizados

En orden:
1. `make lint` (Ruff + ESLint + otros linters activos).
2. `make typecheck` (mypy + tsc).
3. `make test` (unit + contract + integration).
4. Si toca frontend: `pnpm test` + `pnpm test:visual` (Playwright visual regression).
5. Si toca MCP: contract tests de tools/resources.

Si algo falla:
- Reporta el fallo exacto (archivo + línea).
- Sugiere invocar `build` para arreglar y volver aquí.
- **Detente**.

### 3. Aplicar `compliance-scan` (skill)

Ejecuta [`compliance-scan`](../skills/compliance-scan/SKILL.md) sobre los cambios:
- Gate `license`: atribución ARASAAC visible en exports, no modificación de pictogramas, no imágenes generadas por IA.
- Gate `privacy`: sin PII en materiales, logs, tests o fixtures. Sin vinculación persona↔material.
- Chequeos adicionales: IDs ARASAAC reales, contexto no comercial, densidad visual, lenguaje llano, coherencia de secuencia.

Cada check produce PASS/WARN/FAIL. **FAIL en gate crítico = detener**.

### 4. Aplicar `a11y-audit` (skill)

Si la change toca `apps/web/**`:
- Ejecuta axe sobre las páginas modificadas.
- Verifica navegación por teclado, foco visible, contraste AA, labels, independencia del color.
- Consulta persona `accessibility-qa` y `a11y-cognitive`.

### 5. Aplicar `human-review-gate` (skill)

Si la change produce materiales exportables:
- Verifica que existe estado `approved` explícito con trazabilidad.
- Sin aprobación → **detener** exportación.

### 6. Consultar personas transversales

- `qa` → ¿escenarios de `spec.md` cubiertos por tests?
- `test-automation` → ¿tests son deterministas? ¿coverage razonable?
- `security` → ¿sin secretos en logs? ¿inputs validados? ¿sin ejecución arbitraria?
- `observability` → ¿eventos/métricas emitidos donde procede?

### 7. Emitir dictamen

Escribe un resumen en el chat con:

```md
## Verify report — <change_id>
- Tests: ✅ / ❌ (detalles)
- Lint/Typecheck: ✅ / ❌
- Compliance (license/privacy): ✅ / ❌ (findings)
- A11y: ✅ / ⚠️ / ❌
- Human review: ✅ / ⏳ pending / ❌
- Personas consultadas: qa, security, ...
- Decisión: PROCEDER a docs / BLOQUEAR y volver a build
```

Si todo verde: sugiere `/verify-change` está OK, pasar a `docs` (implícito) o `/archive-change`.

## Salida esperada

- Reporte estructurado con secciones de tests, compliance, a11y y human-review.
- Cero fallos en gates críticos.
- Tests verdes localmente y en CI.

## Criterios de éxito

- ✅ Todos los escenarios verificables de `spec.md` cubiertos por tests o smoke check.
- ✅ Los 3 gates críticos evaluados y documentados.
- ✅ Sin regresiones detectadas.
- ✅ Dictamen claro (PROCEDER / BLOQUEAR).

## Errores comunes

- ❌ "Todo verde" sin ejecutar los tests: verifica exit codes.
- ❌ Ignorar warnings de axe porque "no bloquean": documenta o corrige.
- ❌ Aprobar sin `human_review` cuando hay exportación de material.
- ❌ No documentar los findings de `compliance-scan`: pierdes trazabilidad.
- ❌ Modificar código en esta fase: si algo falla, vuelve a `build`.

## Referencias

- Skills:
  - [`compliance-scan`](../skills/compliance-scan/SKILL.md)
  - [`a11y-audit`](../skills/a11y-audit/SKILL.md)
  - [`human-review-gate`](../skills/human-review-gate/SKILL.md)
- Gates: [`mandatory-gates`](../rules/mandatory-gates.md)
- Workflow: [`spec-build-verify`](../workflows/spec-build-verify.workflow.md)
