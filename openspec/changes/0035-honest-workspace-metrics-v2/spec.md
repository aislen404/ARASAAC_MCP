# Spec — 0035 Honest Workspace Metrics v2

## MUST

### Card "Progreso del flujo guiado"

- MUST compute progress from the combination of global flow phase (Paso 1, 2) and internal review substeps (0032).
- MUST show completed, in-progress and pending counts as text next to the donut.
- MUST display `currentStepLabel` such as "Paso 3.2 · Enviar a revisión" when applicable.
- MUST show "Sin borrador activo" clearly when no material is loaded.
- MUST offer a contextual CTA that navigates to the current step (or to the workspace when none exists).

### Card "Validación de la colección"

- MUST consume the latest `ValidationReport` for the active material via the hook defined in 0033.
- MUST render three counters: `bloqueantes`, `advertencias`, `ok` with textual badges.
- MUST render one of five contextual states: `no-material`, `no-report`, `blocked`, `warnings`, `clean`.
- MUST expose a CTA "Ver detalle" that links to the validation substep (3.1) or to the inbox (0034) when applicable.
- MUST expose a CTA "Volver a validar" that triggers a fresh validation when a material is loaded.
- MUST announce transitions to `blocked` via `aria-live="assertive"`; other transitions via `polite`.

### Card opcional "Materiales recientes"

- MAY be rendered when the feature is enabled.
- MUST show up to 3 recent materials fetched from `GET /api/workspaces/{slug}/materials?limit=3&sort=updated_at:desc` with title, status and a "Retomar" action.
- MUST link to `/w/<slug>/mis-materiales` for "Ver todos".
- MUST NOT use `localStorage`, `sessionStorage` or any client-only storage as data source (per 0034).

### Fuentes de datos

- MUST NOT show any counter derived from data not provided by 0032/0033/0034.
- MUST degrade gracefully when a data source is unavailable, showing "Sin datos disponibles" and an explanatory tooltip.

### Accesibilidad

- MUST meet WCAG 2.2 AA for text, icons and CTAs in all five states.
- MUST render severity via text + icon in addition to any color coding.
- MUST place `aria-labelledby` on each card region.
- MUST keep all interactive elements reachable and operable by keyboard.

## SHOULD

- SHOULD reuse Convergencia Serena tokens for spacing, color and typography.
- SHOULD keep counters concise (0–9999) and format larger numbers with locale grouping.
- SHOULD ensure feature parity with 0027 honest empty states before adding new counters.

## MUST NOT

- MUST NOT display hardcoded percentages or counts (no `66%`, no `126 elementos`).
- MUST NOT rely on color alone to convey severity.
- MUST NOT trigger validation automatically on every render; validation is invoked on demand or on material change.
- MUST NOT link to non-existent anchors or routes.
- MUST NOT expose data from workspaces other than the one addressed by the current `/w/[slug]` route.
- MUST NOT rely on client-only storage as a data source; all metrics come from backend endpoints under `/api/workspaces/{slug}/...`.

## Escenarios verificables

1. **Sin material**: card Progreso "0% · Sin borrador activo · CTA Comenzar"; card Validación "Sin material para validar · CTA Ir al área de trabajo".
2. **Material sin validar**: card Progreso muestra subpaso 3.1; card Validación "Aún no has validado · CTA Validar ahora".
3. **Reporte con 2 bloqueantes**: card Validación muestra "2 · 0 · N" con `aria-live="assertive"` en el resumen y CTA "Ver detalle" enlazando a 3.1.
4. **Reporte solo con warnings**: card Validación muestra "0 · N · M" y mensaje "Revisa antes de aprobar".
5. **Material aprobado**: card Progreso 100% + label subpaso 3.5; card Validación "Colección lista para exportar".
6. **Recientes vacíos**: card opcional oculta o muestra estado vacío honesto según feature flag.
7. **Accesibilidad**: axe-core sin violaciones en los cinco estados; navegación por teclado completa.
8. **Regresión visual**: snapshots aprobados para los cinco estados.
9. **Deep-link con material aprobado**: al cargar por `/w/<slug>/material/<uuid>`, ambas cards se actualizan en <1s tras la respuesta.
