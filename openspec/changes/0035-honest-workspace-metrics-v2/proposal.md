# Proposal — 0035 Honest Workspace Metrics v2

## Problema

La card "Progreso del flujo guiado" y la card "Validación de la colección" del dashboard (Convergencia Serena) siguen mostrando métricas proxy débiles tras 0027:

- `Progreso` deriva solo de la fase del flujo global (0–5), sin diferenciar los subpasos internos del Paso 3 (que se estructurarán con 0032).
- `Validación de la colección` computa "totales / por revisar / correctos" con lógica local ingenua (número de ítems con pictograma), no con hallazgos reales del motor de validación.
- No hay CTA en las cards que lleve al lugar donde actuar sobre el hallazgo.
- El estado "0 · 0 · 0" es honesto pero no explica al usuario qué hacer.

Con 0032 y 0033 aterrizando, este proxy se vuelve un obstáculo: hay datos reales disponibles y las cards deben reflejarlos.

## Cambio propuesto

Recablear las cards de métricas para que:

1. **Card "Progreso del flujo guiado"**:
   - Sume los subpasos internos del Paso 3 (0032) al conteo global.
   - Muestre pasos completados / en curso / pendientes con detalle textual.
   - Refleje "Sin borrador activo" claramente cuando no hay material en curso.
   - CTA contextual: "Ir al paso actual" enlaza al subpaso activo.

2. **Card "Validación de la colección"**:
   - Consuma el último `ValidationReport` (0033) del material activo.
   - Muestre 3 contadores: `bloqueantes`, `advertencias`, `ok`.
   - Estado "Sin material activo" cuando no hay borrador.
   - Estado "Sin validar aún" cuando hay material pero no reporte cacheado.
   - CTA: "Ver detalle" enlaza al panel de validación (subpaso 3.1).

3. **Card nueva opcional "Materiales recientes"** (deferida si no cabe en MVP):
   - Últimos 3 materiales de la bandeja (0034) con estado y acción "Retomar".

## Fuera de alcance

- Rediseño visual profundo de las cards (mantiene grid Convergencia Serena).
- Nuevos indicadores no cubiertos por 0032/0033/0034.
- Panel completo de validación (vive en 0033 y 0032).
- Métricas agregadas del sistema (media de pictogramas, tiempo medio, etc.).
- Personalización de las cards por el usuario.

## Valor

- Cierra la brecha entre "dashboard vistoso" y "dashboard útil".
- Convierte las cards en accesos verificables al proceso real.
- Refuerza la coherencia entre datos backend (0033), flujo guiado (0032) y persistencia (0034).
- Reduce el riesgo de aprobación superficial (regla absoluta #5) al mostrar bloqueantes en dashboard.

## Referencias

- Change previo: `openspec/changes/0027-frontend-shell-honest-state`.
- Contratos visuales: `apps/web/src/design-system/component-contracts/CsMetricCards.md`, `CsContinueCard.md`.
- Dependencia: `openspec/changes/0032-review-export-guided-flow` (subpasos), `openspec/changes/0033-material-validation-panel` (reporte), `openspec/changes/0034-materials-inbox-and-persistence` (recientes).
