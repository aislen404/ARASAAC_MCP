# Proposal — 0033 Material Validation Panel

## Problema

La card "Validación de la colección" del dashboard y el paso 3 del constructor usan proxies débiles como "número de ítems con pictograma" para simular una validación. No hay un motor real que aplique las políticas de licencia ARASAAC, privacidad, atribución, densidad y coherencia definidas en las reglas absolutas del proyecto (`AGENTS.md` §2).

Consecuencias:

- El usuario puede aprobar y exportar materiales con hallazgos silenciosos.
- La revisión humana (0032, subpaso 3.3) no tiene un checklist accionable respaldado por chequeos automáticos.
- Los skills `validate-*` definidos en `.agents/skills/` no tienen contrapartida ejecutable en el backend ni en la UI.

## Cambio propuesto

Introducir un **motor de validación** invocable desde backend y consumible desde frontend, que produce un reporte tipificado por severidad.

### Backend

- Nuevo módulo `services/api/src/arasaac_platform/services/validation.py` con validadores puros y componibles.
- Nuevo endpoint `POST /api/materials/{id}/validate` que ejecuta los validadores contra el material persistido y devuelve `ValidationReport`.
- Validadores incluidos en el MVP (todos bloqueantes salvo indicación contraria):
  1. `validate_pictogram_ids_real` — cada `pictogram_id` referencia un ID real de ARASAAC (usa `arasaac.pictograms` local con fallback a MCP).
  2. `validate_license_notice_visible` — el material serializa la cadena de atribución obligatoria.
  3. `validate_no_personal_data` — heurística sobre textos (correos, teléfonos, nombres propios detectables, DNIs) → bloqueante.
  4. `validate_no_modified_pictograms` — cada referencia mantiene URL original y no incluye transformaciones (`?bg=`, edits).
  5. `validate_non_commercial_context` — presencia de declaración no comercial en metadatos del material.
  6. `validate_visual_density` — nº de ítems por tipo dentro de límites recomendados → **advertencia**.

### Frontend

- Cliente `validateMaterial()` en `features/material-builder/api.ts`.
- Panel `ValidationPanel` reutilizable, consumido por subpaso 3.1 (0032) y por card del dashboard (0035).
- Presentación por severidad con badges accesibles (icono + texto + color, nunca solo color).

## Fuera de alcance

- Validadores adicionales: coherencia semántica, lectura fácil, focus order, contraste (quedan para fases posteriores).
- IA generativa para asistir a la corrección de hallazgos.
- Modificación automática del material (los validadores solo reportan).
- Reglas dinámicas configurables por usuario.

## Valor

- Convierte las reglas absolutas del proyecto en gates ejecutables y auditables.
- Habilita 0032 (revisión guiada) con datos reales, y 0035 (dashboard honesto) con métricas verdaderas.
- Reduce el riesgo de exportar materiales que violen licencia, atribución o privacidad.
- Ofrece a los skills `validate-*` un endpoint estable al que anclar contract tests.

## Referencias

- Reglas absolutas: `AGENTS.md` §2, §7 (Política ARASAAC).
- Skills: `.agents/skills/validate-*/SKILL.md` (los 9 validadores definidos).
- Change previo: `openspec/changes/archive/0002-arasaac-license-governance`.
- Dependencia UX: `openspec/changes/0032-review-export-guided-flow`.
- Dependencia UX: `openspec/changes/0035-honest-workspace-metrics-v2`.
