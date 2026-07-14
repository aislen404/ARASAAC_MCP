# Spec — 0033 Material Validation Panel

## MUST

### Modelo

- MUST expose `Severity` with values `blocker`, `warning`, `ok`.
- MUST expose `ValidationFinding` with `validator_id`, `severity`, `title`, `detail`, `subject`, `subject_ref`.
- MUST expose `ValidationReport` with `material_id`, `material_version`, `validators_run`, `findings`, `generated_at`, `is_blocking`.

### Endpoint

- MUST expose `POST /api/workspaces/{slug}/materials/{id}/validate` returning `ValidationReport` with HTTP 200.
- MUST return HTTP 404 when the workspace does not exist, when the material does not exist, or when the material does not belong to the workspace (never 403).
- MUST be idempotent: calling twice with the same material version returns equivalent reports (timestamps may differ).
- MUST NOT mutate the material.
- MUST emit an audit event `VALIDATED` including counts by severity, scoped to the material's workspace.
- MUST expose the `no_personal_data` validator as a reusable service consumed by 0034's `PATCH /api/workspaces/{slug}` for `display_name` validation.

### Validadores MVP

- MUST run the six MVP validators listed in the design.
- MUST classify `no_personal_data` findings as `blocker` for emails, phone numbers and national IDs.
- MUST classify `visual_density` findings as `warning` only.
- MUST set `is_blocking = true` if any finding has severity `blocker`.
- MUST tolerate missing optional pictogram lookups: if the ID cannot be verified online, the finding is `warning` with a clear detail explaining the degradation.

### Frontend

- MUST expose a `ValidationPanel` component consumed by the review substep 3.1 (change 0032) and by the dashboard card (change 0035).
- MUST render each finding with a textual severity badge in addition to any color coding.
- MUST expose a "Volver a validar" action that re-fetches the report.
- MUST cache the report by `material_version` to avoid redundant requests.

### Accesibilidad

- MUST meet WCAG 2.2 AA contrast for badges and text.
- MUST group findings semantically (`role="group"` + `aria-labelledby`).
- MUST announce blocking summaries via `aria-live="assertive"`.
- MUST keep the panel fully operable by keyboard.

### Gobernanza

- MUST persist `usage_context` on materials with default `non_commercial`.
- MUST include validation results in the audit trail queried by `GET /api/materials/{id}/audit`.

## SHOULD

- SHOULD reuse local ARASAAC pictogram cache before falling back to MCP.
- SHOULD group findings by validator in the UI for clarity.
- SHOULD document each finding's `detail` with an actionable next step ("Elimina el email en el paso 2 · texto 3").
- SHOULD localize `title` and `detail` (default `es`, prepared for future `en`).

## MUST NOT

- MUST NOT auto-modify the material based on findings.
- MUST NOT rely solely on color to communicate severity.
- MUST NOT block the endpoint on remote calls beyond a configurable timeout (default 3s); degrade gracefully with `warning`.
- MUST NOT emit personal data content in findings' `detail`; describe the finding without echoing the offending text verbatim.
- MUST NOT run validators in the client for gating purposes; the endpoint is the source of truth.

## Escenarios verificables

1. **Material canónico limpio** → `is_blocking = false`, todos los validadores devuelven un finding `ok`.
2. **Material con email en un texto** → `is_blocking = true`, finding `no_personal_data` con `subject = "item"` y `subject_ref` correcto.
3. **Material con pictograma desconocido offline** → finding `pictogram_ids_real` con severidad `warning` y detalle explicando la degradación (o `blocker` si el ID no existe en catálogo local).
4. **Material con atribución alterada** → finding `license_notice_visible` `blocker`.
5. **Material con URL de pictograma modificada** → finding `no_modified_pictograms` `blocker`.
6. **Material con densidad al 90%** → finding `visual_density` `warning`, `is_blocking = false`.
7. **Endpoint idempotente**: dos llamadas consecutivas devuelven mismo conjunto de findings (order-insensitive).
8. **Audit event emitido**: tras validar, `GET /audit` incluye un evento `VALIDATED` con conteos por severidad.
9. **Panel accesible**: axe-core sin violaciones en los tres estados; recorrido completo con teclado.
