# Spec — 0032 Review & Export Guided Flow

## MUST

### Estructura del Paso 3

- MUST render Paso 3 as a linear substepper with five substeps (3.1 Validation, 3.2 Submit, 3.3 Human review, 3.4 Prepare package, 3.5 Download).
- MUST expose a computed `reviewPhase` state derived from validation results, material status and local UI state.
- MUST use `aria-current="step"` on the active substep.
- MUST render each substep with a unique heading, an `aria-live="polite"` region and a description of its purpose.

### Subpaso 3.1 — Validación

- MUST block advancing to 3.2 while validation reports blocking findings.
- MUST list findings grouped as `blocker`, `warning`, `ok` (delegated to change 0033).
- MUST offer a "Volver a editar" action that returns focus to Paso 2 without losing state.

### Subpaso 3.2 — Enviar a revisión

- MUST call `POST /api/workspaces/{slug}/materials/{id}/submit` only when 3.1 has no blockers.
- MUST reflect the new status (`in_review`) in the UI immediately.
- MUST NOT allow submission if `material.status` is not `draft` or `rejected`.

### Subpaso 3.3 — Revisión humana

- MUST show a checklist with at least the five items defined in the design.
- MUST require the reviewer to check all items before enabling "Aprobar".
- MUST require a note of at least 20 characters.
- MUST send the checklist and note to `POST /api/workspaces/{slug}/materials/{id}/review`.
- MUST NOT allow approving without checklist completion.
- MUST allow rejecting with note but without full checklist; rejection returns the material to editable state.

### Subpaso 3.4 — Preparar exportación

- MUST call `GET /api/workspaces/{slug}/materials/{id}/export/manifest?formats=…` and render the manifest (attribution, pictogram IDs, version, human-review-approved flag) before any download.
- MUST allow selecting one or more formats among the supported list.
- MUST NOT download binary content in this substep.

### Subpaso 3.5 — Descarga y auditoría

- MUST expose one "Descargar paquete" action per selected format (or a single grouped action if multiple).
- MUST render a timeline of audit events fetched from `GET /api/workspaces/{slug}/materials/{id}/audit`, ordered chronologically.
- MUST make the timeline reachable by keyboard and screen readers.
- MUST show attribution string near the download control.
- MUST use the deep-link route `/w/<slug>/material/<uuid>` (never `?material=<uuid>`) so state remains addressable across sessions.

### Backend

- MUST extend `ReviewMaterialInput` with optional `checklist` field.
- MUST reject `outcome == approved` when `checklist` is missing or incomplete with HTTP 422.
- MUST persist checklist alongside `note` for traceability.
- MUST expose `GET /api/workspaces/{slug}/materials/{id}/export/manifest` returning `ExportManifest` without `content_base64`.
- MUST route all endpoints referenced by this change under `/api/workspaces/{slug}/materials/...` (introduced by 0034); no legacy `/api/materials/*` paths remain.
- MUST NOT modify existing export endpoints' contract for binary formats (beyond the prefix change).

### Trazabilidad y gobernanza

- MUST preserve all audit events emitted today (`created`, `submitted`, `reviewed`, `exported`).
- MUST attach checklist metadata to the `reviewed` event.
- MUST keep visible attribution string in the review and download substeps.

## SHOULD

- SHOULD move focus to the newly active substep heading when advancing.
- SHOULD collapse the audit timeline by default and show a summary of the latest event.
- SHOULD reuse existing Convergencia Serena components for consistency.
- SHOULD offer a "Rechazar y volver a edición" shortcut in 3.3 that reopens Paso 2.

## MUST NOT

- MUST NOT allow exporting when material status is not `approved`.
- MUST NOT bypass validation (subpaso 3.1) via UI shortcuts.
- MUST NOT rely on color alone to signal substep state.
- MUST NOT hide the attribution notice at any substep of Paso 3.
- MUST NOT collect personal data as part of the checklist or note.
- MUST NOT implement authentication or role-based gating in this change (deferred to 0021).

## Escenarios verificables

1. **Flujo completo feliz**: crear borrador válido → 3.1 sin hallazgos → enviar → checklist marcado + nota 30 chars → aprobado → manifiesto cargado con HTML+PDF seleccionados → descarga ambos → timeline muestra 5 eventos.
2. **Bloqueo por validación**: hallazgo bloqueante en 3.1 → botón "Enviar" deshabilitado con explicación textual → editar borrador → validar de nuevo → pasa.
3. **Rechazo con nota**: en 3.3, revisor rechaza con nota → material vuelve a estado `rejected` → subpaso 3.1 accesible de nuevo.
4. **Aprobación sin checklist**: intentar aprobar con 4/5 marcados → botón deshabilitado; llamada manual al endpoint devuelve 422.
5. **Descarga sin manifiesto**: no es posible; 3.5 requiere haber cargado manifiesto en 3.4.
6. **Recorrido teclado completo**: navegar 3.1 → 3.5 solo con Tab/Shift-Tab/Enter/Espacio sin quedar atrapado ni perder foco.
7. **Timeline vacía**: material recién creado (sin submit) no rompe la UI en 3.5 (subpaso no accesible aún).
