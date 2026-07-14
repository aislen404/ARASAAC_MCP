# Tasks — 0035 Honest Workspace Metrics v2

## 1. OpenSpec

- [x] Crear `proposal.md`, `design.md`, `tasks.md`, `spec.md`.
- [x] Confirmar dependencias resueltas por 0032 (subpasos), 0033 (report) y 0034 (recientes) antes de implementar — confirmado 2026-07-14.
- [ ] Orden de implementación acordado: **último del paquete** (0033 → 0032 ∥ 0034 → 0035).

## 2. Extender modelo de métricas

- [ ] Actualizar `apps/web/src/components/convergencia-serena/workspace-metrics.ts` con los nuevos campos definidos en el design.
- [ ] Añadir función `deriveValidationSummary()` a partir de `ValidationReport`.
- [ ] Añadir función `deriveCurrentStep()` a partir de `phase` + `reviewPhase`.
- [ ] Tests unitarios con matriz completa de escenarios.

## 3. Hooks

- [ ] Confirmar/consumir `useValidationReport(workspaceSlug, materialId, version)` (definido en 0033).
- [ ] Crear `useRecentWorkspaceMaterials(slug)` que consume `GET /api/workspaces/{slug}/materials?limit=3&sort=updated_at:desc`. **No usar `localStorage` ni `useRecentMaterials()`**.
- [ ] Añadir degradación cuando alguno no está disponible ("Sin datos").

## 4. Refactor `CsMetricCards`

- [ ] Refactorizar `apps/web/src/components/convergencia-serena/CsMetricCards.tsx` para consumir las nuevas métricas.
- [ ] Añadir CTAs contextuales por estado.
- [ ] Añadir card opcional "Materiales recientes" si cabe (feature flag interno para postergar).
- [ ] Actualizar `apps/web/src/design-system/component-contracts/CsMetricCards.md`.

## 5. Accesibilidad

- [ ] Badges con texto visible.
- [ ] `aria-live="assertive"` solo al aparecer bloqueantes; `polite` en cambios normales.
- [ ] CTAs con `<a>` vs `<button>` según semántica.
- [ ] axe-core sin violaciones en los cinco estados definidos.

## 6. Regresión visual

- [ ] Nuevos snapshots para los cinco estados.
- [ ] Actualizar rúbrica de aceptación si aplica.

## 7. Tests

- [ ] Tests unitarios de `workspace-metrics` con matriz.
- [ ] Tests unitarios del componente `CsMetricCards` con mocks.
- [ ] Test e2e: material con bloqueantes → card muestra bloqueantes → resolver → card actualiza.
- [ ] Test e2e: sin material → CTAs "Comenzar" y "Ir al área de trabajo" funcionan.

## 8. Documentación

- [ ] Actualizar `apps/web/src/design-system/component-contracts/CsMetricCards.md`.
- [ ] Referenciar 0032, 0033 y 0034 en el contrato.
- [ ] Añadir notas al design-system doc si aplica.

## 9. Validación final

- [ ] `make agent-packs-verify`.
- [ ] Lint/typecheck frontend.
- [ ] Suite completa de tests + axe + visual regression.
- [ ] Revisión por Accessibility QA + Product Owner Social antes de archivar.
