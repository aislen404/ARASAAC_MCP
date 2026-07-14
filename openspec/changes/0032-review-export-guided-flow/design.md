# Design — 0032 Review & Export Guided Flow

## Principio rector

**La revisión humana es un proceso guiado y verificable, no un botón.** Cada subpaso debe hacer explícita la condición de avance, el actor responsable y el rastro que deja.

## Estado actual

- `apps/web/src/features/material-builder/review-panel.tsx`: 8 botones planos, condicionados solo por `material.status`. No hay progreso interno.
- `apps/web/src/features/material-builder/use-material-builder.ts`: expone `submitReview`, `decide`, `download`. Descargas directas sin previsualización del paquete.
- Backend (`services/api/src/arasaac_platform/api/materials.py`): `POST /submit`, `POST /review`, `GET /export`, `GET /audit`, `GET /` disponibles y probados.

> **Nota (0034)**: tras 0034, todos los endpoints de materiales viven bajo `/api/workspaces/{slug}/materials/...`. Esta change debe consumir y exponer sus endpoints bajo ese prefijo, y el deep-link del constructor pasa a ser `/w/<slug>/material/<uuid>` (no `?material=<uuid>`).

## Arquitectura propuesta

### 1. Subestado `reviewPhase` en el builder

Añadir a `use-material-builder.ts` un estado derivado `reviewPhase: 0 | 1 | 2 | 3 | 4` que representa los subpasos 3.1–3.5. Se computa a partir de:

- Resultado de la última llamada a validación (0033).
- `material.status`.
- Estado local de manifiesto pre-cargado.
- Estado local de descarga completada.

Reglas de transición:

| De | A | Condición |
|----|---|-----------|
| 3.1 | 3.2 | Validación sin hallazgos bloqueantes. |
| 3.2 | 3.3 | `status === "in_review"`. |
| 3.3 | 3.4 | `status === "approved"` con nota registrada. |
| 3.4 | 3.5 | Manifiesto cargado y formatos seleccionados ≥ 1. |
| 3.5 | 3.1 | Rechazo o edición posterior reinicia el subflujo. |

### 2. Componente `ReviewPanel` refactorizado

- Reemplaza el bloque plano por `CsWorkflowSubStepper` (nuevo, subcomponente accesible con `role="list"`, cada paso `role="listitem"` con `aria-current` cuando activo).
- Cada subpaso es una tarjeta `CsPanel` con:
  - Encabezado `hX` numerado.
  - Descripción breve del propósito del subpaso.
  - Región `aria-live="polite"` para feedback del subpaso.
  - Acciones (solo las relevantes al subpaso activo; el resto están en modo lectura o deshabilitadas con explicación textual).
- Los subpasos completados muestran resumen (no botones), permitiendo retroceder solo mediante acciones explícitas ("Editar borrador", "Rechazar y devolver").

### 3. Nuevos endpoints/contratos backend

Todos los endpoints viven bajo el prefijo `/api/workspaces/{slug}/materials/{id}/...` (introducido por 0034).

Se añade un endpoint ligero para desacoplar la vista del proceso de descarga:

- `GET /api/workspaces/{slug}/materials/{id}/export/manifest?formats=html,pdf` — devuelve `ExportManifest` sin generar contenido binario. Reutiliza el modelo `ExportManifest` existente pero sin `content_base64`. Coste: bajo (no invoca `export_pdf` etc.).

Además se extiende el endpoint existente de revisión:

- `POST /api/workspaces/{slug}/materials/{id}/review` — acepta `ReviewMaterialInput` extendido con `checklist: list[ChecklistItem]` opcional. Backend valida que el checklist esté completo cuando `outcome == approved`.

### 4. UX de subpaso 3.3 (revisión humana explícita)

Checklist mínima renderizada como grupo `fieldset`:

- [ ] He verificado que todos los pictogramas provienen de ARASAAC.
- [ ] He confirmado que la atribución es visible.
- [ ] He revisado que ningún texto contiene datos personales.
- [ ] He revisado la coherencia de la secuencia.
- [ ] Asumo la responsabilidad de esta revisión.

El botón `Aprobar` está deshabilitado hasta que todas estén marcadas. La nota es obligatoria (min 20 caracteres). El backend recibe el checklist y lo persiste en `ReviewDecision.note` (estructurado) para trazabilidad.

### 5. Timeline de auditoría en 3.5

Consumir `GET /api/workspaces/{slug}/materials/{id}/audit` al entrar en 3.5 y renderizar como `ol` ordenada por timestamp, con roles semánticos. Colapsable por defecto (`<details>`), pero anunciable.

## Accesibilidad

- Cada subpaso tiene título único (`hX` con id) y `aria-labelledby` en su contenedor.
- El stepper interno usa `aria-current="step"` en el subpaso activo.
- Ningún avance depende del color (los estados usan texto + icono textual como `✓`, `⧗`, `⋯`).
- Foco estable: al avanzar a un subpaso, el foco se mueve al `hX` del subpaso con `tabindex="-1"`.
- Feedback vía `aria-live="polite"`; errores bloqueantes con `aria-live="assertive"`.
- Botones nunca solo icono; siempre con texto.
- Checklist con `fieldset` + `legend`, cada `input type="checkbox"` con `label` asociado.

## Impacto en tests

- Nuevos tests unitarios para `computeReviewPhase()`.
- Nuevo test e2e Playwright: flujo completo 3.1–3.5 con validación pasada, revisión con checklist, descarga.
- Nuevo test e2e negativo: no se puede aprobar sin checklist completo.
- Actualizar `material-flow.spec.ts` y `accessibility-full-keyboard.spec.ts` para navegar por subpasos.
- Contract test backend: `ReviewMaterialInput` con `checklist` opcional; `approved` sin checklist devuelve 422.

## Alternativas descartadas

- **Tab bar horizontal en el paso 3**: rompe la métafora de "flujo lineal" y complica el foco.
- **Modal para revisión**: choca con la accesibilidad y con la naturaleza continua del proceso.
- **Persistir checklist en tabla nueva**: sobreingeniería para MVP; el `note` estructurado es suficiente.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| El usuario percibe el flujo más "pesado". | Documentación en línea breve, valor explícito ("es tu firma de responsabilidad"). |
| Backend rechaza payloads antiguos. | Nuevo campo `checklist` es opcional; solo se requiere para `outcome == approved`. |
| Timeline sobrecarga el paso 3.5. | Colapsable por defecto, mostrar solo últimos 5 eventos con "Ver más". |
