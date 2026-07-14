# Motor de validación de materiales

## Objetivo

El motor de validación aplica reglas de gobernanza antes de que un material pase
de borrador a revisión humana. Su función es detectar incidencias de licencia,
privacidad, trazabilidad ARASAAC y densidad visual sin sustituir la revisión
humana final.

## Ubicación

- Backend: `services/api/src/arasaac_platform/services/validation.py`
- Schemas: `services/api/src/arasaac_platform/schemas/validation.py`
- Endpoint oficial: `POST /api/workspaces/{slug}/materials/{id}/validate`
- Integración frontend: `apps/web/src/features/material-builder/validation-panel.tsx`

## Contrato

La respuesta devuelve un `ValidationReport` con:

- `material_id`
- `material_version`
- `findings`
- `blocker_count`
- `warning_count`
- `ok_count`
- `is_blocking`

Cada `ValidationFinding` incluye `code`, `severity`, `message` y `field`
opcional.

## Validadores incluidos

- `validate_pictogram_ids_real`
- `validate_license_notice_visible`
- `validate_no_personal_data`
- `validate_no_modified_pictograms`
- `validate_non_commercial_context`
- `validate_visual_density`

## Flujo

1. El material se crea o edita en borrador.
2. La interfaz solicita validación explícita.
3. El backend ejecuta los validadores como fuente de verdad.
4. El endpoint registra auditoría `VALIDATED` con el resumen de findings.
5. El frontend muestra el resumen y bloquea el envío a revisión si
   `is_blocking=true`.

## Garantías

- No persiste prompts ni texto IA como parte del motor.
- No modifica pictogramas ni genera recursos nuevos.
- Mantiene el uso social no comercial.
- Refuerza la política de no PII antes de revisión/exportación.

## Estado actual

- La validación se ejecuta bajo scope de workspace.
- El contrato de `ValidationReport` no cambia con el prefijo nuevo.