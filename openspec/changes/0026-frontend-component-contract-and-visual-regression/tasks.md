# Tasks — 0026

## 1. Preparación

- [x] Crear rama `codex/frontend-pixel-perfect-round3`.
- [x] Instalar assets en `apps/web/public/convergencia-serena/` (sync desde `apps/web/assets/` vía `prebuild`).
- [x] Instalar tokens/CSS en `apps/web/src/design-system/css/`.
- [x] Importar CSS en el entry global.

## 2. Componentes shell

- [x] Crear `ConvergenciaSerenaApp`.
- [x] Crear `CsHeader`.
- [x] Crear `CsSideRail`.
- [x] ~~Crear `CsMobilePreview`~~ (eliminado: mockup decorativo sin valor funcional).
- [x] Crear `CsContextHelp`.
- [x] Crear `CsBottomStrip`.

## 3. Workspace

- [x] Crear `CsGuidedWorkspace`.
- [x] Crear `CsWorkflowStepper`.
- [x] Crear `CsMetricCards`.
- [x] Crear `CsContinueCard`.
- [x] Crear `CsSuggestionStrip`.

## 4. Builder

- [x] Refactorizar `MaterialBuilder` para variante embedded o crear adapter.
- [x] Separar configuración, búsqueda, preview y revisión en cards.
- [x] Preservar lógica API y estados.
- [x] Preservar atribución ARASAAC.

## 5. Tema

- [x] Implementar tokens light/dark.
- [x] Persistir preferencia.
- [x] Respetar `prefers-color-scheme`.
- [x] Verificar contraste AA.

## 6. Accesibilidad

- [x] Landmarks correctos.
- [x] Skip link.
- [x] ARIA labels en nav, status, panels y controls.
- [x] Focus visible en todos los controles.
- [x] Navegación teclado completa.
- [x] Targets ≥ 44 px.

## 7. Visual regression

- [x] Añadir screenshots desktop light/dark.
- [x] Añadir screenshots mobile light/dark.
- [x] Añadir test de no overflow horizontal.
- [x] Añadir test de assets presentes.
- [x] Añadir axe serious/critical = 0.

## 8. Validación

- [x] `make openspec-verify`.
- [x] `make lint`.
- [x] `make typecheck`.
- [x] `make test` (unitarios web).
- [x] `npm --prefix apps/web run build`.
- [x] Rúbrica visual ≥ 90/100.
