# Tasks — 0032 Review & Export Guided Flow

## 1. OpenSpec

- [x] Crear `proposal.md`, `design.md`, `tasks.md`, `spec.md`.
- [x] Validar dependencia con 0033 (validation panel) y 0034 (inbox) — confirmado 2026-07-14.
- [ ] Orden de implementación acordado: iniciar tras 0033; puede solaparse con 0034 desde la mitad.

## 2. Backend — contratos mínimos

- [ ] Extender `ReviewMaterialInput` con campo opcional `checklist: list[ChecklistItem]` (schema Pydantic).
- [ ] Añadir validación: si `outcome == approved`, `checklist` debe estar presente y todos los ítems marcados.
- [ ] Persistir `checklist` serializado dentro de `ReviewDecision.note` estructurado (JSON compacto con prefijo identificable) o como campo dedicado si es trivial.
- [ ] Añadir endpoint `GET /api/workspaces/{slug}/materials/{id}/export/manifest?formats=html,pdf,docx,pptx,zip` que devuelve `ExportManifest` sin `content_base64`.
- [ ] Alinear todas las llamadas del constructor con el prefijo `/api/workspaces/{slug}/materials/...` introducido por 0034 (submit, review, audit, export, export/manifest).
- [ ] Cambiar el deep-link del constructor de `?material=<uuid>` a la ruta `/w/<slug>/material/<uuid>` (coordinado con 0034).
- [ ] Cubrir con tests contract (`services/api/tests`): checklist obligatorio en approved, manifiesto no genera binarios, endpoints cruzados devuelven 404.

## 3. Frontend — estado `reviewPhase`

- [ ] Añadir `computeReviewPhase()` en `apps/web/src/features/material-builder/flow-context.tsx` (o nuevo `review-phase.ts`).
- [ ] Exponer `reviewPhase` desde `use-material-builder.ts`.
- [ ] Añadir estado local `manifestPreview`, `selectedFormats`, `checklist`, `reviewNote` en el hook.
- [ ] Añadir acciones `loadManifest()`, `toggleFormat()`, `updateChecklistItem()`, `updateReviewNote()`, `downloadPackage()`.
- [ ] Tests unitarios de `computeReviewPhase` con matriz de casos.

## 4. Frontend — componente `ReviewPanel` refactorizado

- [ ] Sustituir `review-panel.tsx` por composición de subpasos.
- [ ] Crear subcomponentes: `ReviewSubStepValidation`, `ReviewSubStepSubmit`, `ReviewSubStepHumanReview`, `ReviewSubStepPreparePackage`, `ReviewSubStepDownload`.
- [ ] Implementar `CsReviewSubStepper` (o extender `CsWorkflowStepper` existente) con `aria-current="step"`.
- [ ] Renderizar timeline de auditoría en 3.5 como `<details>` con `ol` semántica.
- [ ] Mantener modo `embedded` (Convergencia Serena) y modo clásico.

## 5. Frontend — accesibilidad

- [ ] `fieldset` + `legend` en checklist, cada `input` con `label`.
- [ ] Botones siempre con texto; no depender solo de color.
- [ ] `aria-live="polite"` en feedback de subpaso; `assertive` en errores bloqueantes.
- [ ] Foco al `hX` del subpaso activo al avanzar (`tabindex="-1"`).
- [ ] Ejecutar axe-core en la vista con material aprobado y con material rechazado.

## 6. Contratos visuales (Convergencia Serena)

- [ ] Crear `apps/web/src/design-system/component-contracts/CsReviewSubStepper.md`.
- [ ] Actualizar `MaterialBuilderEmbedded.md` para reflejar los subpasos.
- [ ] Actualizar snapshots de regresión visual afectados.

## 7. Tests

- [ ] Test e2e Playwright: recorrido 3.1 → 3.5 completo, con validación ok.
- [ ] Test e2e negativo: aprobar sin checklist devuelve error visible.
- [ ] Test e2e negativo: descarga sin selección de formatos deshabilita botón.
- [ ] Test e2e teclado: recorrido completo sin ratón (axe + tab order).
- [ ] Actualizar `material-flow.spec.ts` y `accessibility-full-keyboard.spec.ts`.

## 8. Documentación

- [ ] Actualizar `docs/testing/test-plan-mvp0.md` con nuevos casos.
- [ ] Documentar el flujo en `docs/architecture/` (si aplica) o README de la app web.
- [ ] Añadir nota en `NOTICE-ARASAAC.md` si el manifiesto pre-descarga cambia contenido visible.

## 9. Validación final

- [ ] `make agent-packs-verify`.
- [ ] Ejecutar lint/typecheck backend y frontend.
- [ ] Ejecutar suite completa de tests.
- [ ] Revisión humana del flujo por Product Owner Social + Accessibility QA antes de archivar.
