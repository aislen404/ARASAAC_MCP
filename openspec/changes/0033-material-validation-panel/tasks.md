# Tasks — 0033 Material Validation Panel

## 1. OpenSpec

- [x] Crear `proposal.md`, `design.md`, `tasks.md`, `spec.md`.
- [x] Validar dependencia inversa con 0032 y 0035 — confirmado 2026-07-14.
- [x] Orden de implementación acordado: **iniciar primero del paquete** (0033 → 0032 ∥ 0034 → 0035).
- [ ] Endpoint de validación vive bajo `POST /api/workspaces/{slug}/materials/{id}/validate` (prefijo introducido por 0034); exponer además `no_personal_data` como servicio reusable para `PATCH /api/workspaces/{slug}` (`display_name`).

## 2. Backend — modelo y motor

- [x] Añadir enums y modelos `Severity`, `ValidationFinding`, `ValidationReport` en `services/api/src/arasaac_platform/schemas/validation.py`.
- [x] Crear módulo `services/api/src/arasaac_platform/services/validation.py` con `run_validators()`, registro de validadores y `ValidationContext`.
- [x] Añadir campo `usage_context: Literal["non_commercial"] = "non_commercial"` en `Material` si no existe (mantener compatibilidad).

## 3. Backend — validadores

- [x] Implementar `validate_pictogram_ids_real` con lookup local + fallback opcional.
- [x] Implementar `validate_license_notice_visible`.
- [x] Implementar `validate_no_personal_data` con regex documentadas.
- [x] Implementar `validate_no_modified_pictograms`.
- [x] Implementar `validate_non_commercial_context`.
- [x] Implementar `validate_visual_density` con límites configurables.
- [x] Tests unitarios por validador (happy + edge + failure paths).

## 4. Backend — endpoint

- [x] Añadir `POST /api/materials/{id}/validate` en `services/api/src/arasaac_platform/api/materials.py`.
- [x] Emitir evento de auditoría `VALIDATED` con contador de findings.
- [x] Contract test: shape, 404, idempotencia, no muta material.
- [x] Documentar endpoint en OpenAPI (auto vía FastAPI).

## 5. Frontend — cliente y panel

- [x] Añadir `validateMaterial(id)` en `apps/web/src/features/material-builder/api.ts`.
- [x] Añadir tipos `ValidationReport`, `ValidationFinding`, `Severity` en `types.ts`.
- [x] Crear componente reutilizable `apps/web/src/features/material-builder/validation-panel.tsx`.
- [x] Caché local por `material.version` para evitar revalidaciones redundantes.
- [x] Tests unitarios de `ValidationPanel` con reports de ejemplo.

## 6. Accesibilidad

- [x] Cada badge de severidad con texto visible (no solo color).
- [ ] Contraste AA verificado en los tres estados.
- [x] `aria-live="assertive"` en resumen cuando `is_blocking`.
- [x] Findings agrupados con `role="group"` y `aria-labelledby`.
- [ ] Ejecutar axe-core con reports realistas.

## 7. Contratos visuales

- [x] Crear `apps/web/src/design-system/component-contracts/ValidationPanel.md`.
- [ ] Añadir snapshot de regresión visual para los tres estados (ok, warning, blocker).

## 8. Skills

- [ ] Actualizar los 6 skills `.agents/skills/validate-*/SKILL.md` mencionados en el MVP para referenciar el endpoint y el schema.
- [ ] Regenerar packs multi-IDE: `python3 scripts/sync_agent_packs.py`.

## 9. Tests

- [x] Contract test backend por validador.
- [x] E2E: material con email en un texto → validación bloquea.
- [ ] E2E: material con pictograma desconocido → bloquea.
- [x] E2E: material con densidad al 90% → warning visible pero permite avanzar.
- [ ] E2E teclado: navegar el panel completo sin ratón.

## 10. Documentación

- [x] Documentar el motor en `docs/architecture/material-validation.md` (nuevo).
- [x] Actualizar `docs/testing/test-plan-mvp0.md` con casos de validación.
- [x] Actualizar `docs/compliance/arasaac-license-policy.md` referenciando el motor.

## 11. Validación final

- [ ] `make agent-packs-verify`.
- [ ] Lint/typecheck backend y frontend.
- [x] Suite mínima de cierre: backend validation tests + unit frontend + E2E `VAL-003`.
- [ ] Revisión por License Compliance Agent + Accessibility QA antes de archivar.
