# Design — 0035 Honest Workspace Metrics v2

## Principio rector

**Cada dato mostrado en el dashboard debe provenir de una fuente auditable y llevar a la acción que lo resuelve.** Sin fuente, no se muestra; sin acción, no vale.

## Estado actual

- `apps/web/src/components/convergencia-serena/CsMetricCards.tsx` renderiza dos cards.
- `workspace-metrics.ts` calcula proxies:
  - `progressPercent = phase / 5 * 100`.
  - `pendingReview` es 0 o 1 según status.
  - `correctItems` cuenta ítems con pictograma.
- Estados vacíos honestos: `0 · 0 · 0` sin CTA.

## Cambio propuesto

### 1. `WorkspaceMetrics` extendido

Ampliar `workspace-metrics.ts` para computar:

```ts
type WorkspaceMetrics = {
  // Progreso global (Pasos 1–3, con subpasos internos del Paso 3)
  totalSteps: number;              // 5 (P1 + P2 + P3.1..P3.5 colapsado como bloques)
  completedSteps: number;
  inProgressSteps: number;
  pendingSteps: number;
  progressPercent: number;
  currentStepLabel: string;        // "Paso 3.2 · Enviar a revisión"
  currentStepHref: string | null;  // ancla al subpaso activo

  // Validación (proviene del último ValidationReport cacheado)
  hasValidationReport: boolean;
  validationBlockers: number;
  validationWarnings: number;
  validationOk: number;
  validationSummary: "no-material" | "no-report" | "blocked" | "warnings" | "clean";

  // Materiales recientes (opcional)
  recentMaterials: { id: string; title: string; status: MaterialStatus }[];
};
```

### 2. Fuentes de datos

- **Progreso**: `useMaterialFlow().phase` combinado con `useReviewPhase()` (expuesto por 0032) determina paso actual y label.
- **Validación**: hook `useValidationReport(workspaceSlug, material?.material_id, material?.version)` con caché local por versión (definido en 0033). Si no hay material → `no-material`. Si hay pero no reporte → `no-report`. Si hay bloqueantes → `blocked`. Si solo warnings → `warnings`. Si nada → `clean`.
- **Recientes**: `GET /api/workspaces/{slug}/materials?limit=3&sort=updated_at:desc` invocado desde el dashboard del workspace actual. **No hay hook `useRecentMaterials()` local ni `localStorage`**; el listado siempre proviene del backend.

### 3. `CsMetricCards` refactorizado

- **Card 1 "Progreso"**:
  - Donut con `progressPercent`.
  - Texto: "X completados · Y en curso · Z pendientes".
  - Etiqueta subpaso activo: `currentStepLabel`.
  - Link "Ir al paso" (o "Comenzar" si sin material).
- **Card 2 "Validación"**:
  - Tres cifras: bloqueantes / advertencias / ok con badge textual.
  - Mensaje contextual según `validationSummary`.
  - Botón "Ver detalle" → `#cs-review-substep-validation` (subpaso 3.1) o link a bandeja.
  - Botón "Volver a validar" (si hay material) que dispara el hook.
- **Card 3 (opcional) "Materiales recientes"**:
  - Lista con 3 filas máx: título, estado, botón "Retomar" (navega a `/w/<slug>/material/<uuid>`).
  - Enlace "Ver todos" → `/w/<slug>/mis-materiales`.
  - Datos consumidos server-side desde `GET /api/workspaces/{slug}/materials?limit=3&sort=updated_at:desc`.

### 4. Estados vacíos honestos

| Escenario | Card Progreso | Card Validación |
|-----------|---------------|-----------------|
| Sin material | "0%" · "Sin borrador activo" · CTA "Comenzar" | "Sin material para validar" · CTA "Ir al área de trabajo" |
| Material sin validar | X% + label subpaso | "Aún no has validado" · CTA "Validar ahora" |
| Material con bloqueantes | X% + label subpaso | "N bloqueantes · resolver antes de exportar" (con `aria-live="assertive"`) |
| Material solo con warnings | X% + label subpaso | "N advertencias · revisa antes de aprobar" |
| Material limpio | 100% cuando `approved` | "Colección lista para exportar" |

## Accesibilidad

- Cards con `role="region"` y `aria-labelledby`.
- Badges de severidad con texto visible + icono textual.
- CTA como `<a>` cuando navega, `<button>` cuando dispara acción; nunca solo icono.
- `aria-live="polite"` en cambios de contadores; `assertive` cuando aparecen bloqueantes.
- Contraste AA en los tres estados de severidad.

## Impacto en tests

- Tests unitarios ampliados de `computeWorkspaceMetrics` con matriz (sin material / con material sin reporte / con reporte bloqueante / con reporte limpio / material aprobado).
- Test unitario de `CsMetricCards` con mocks del report.
- Test e2e Playwright: crear material → validar con hallazgos → dashboard refleja bloqueantes → resolver → dashboard actualiza.
- Test axe en las cards con los cinco estados definidos.

## Alternativas descartadas

- **Card unificada "Estado del borrador actual"**: rompe el contrato Convergencia Serena y contrats visuales existentes.
- **Poll periódico de validación**: costo y ruido; se prefiere invalidación por versión.
- **Métricas globales del sistema**: fuera de alcance; hoy solo tiene sentido con auth y roles.

## Riesgos

| Riesgo | Mitigación |
|--------|-----------|
| Dependencia dura con 0032 y 0033. | Feature flags o degradación: si no hay hook `useValidationReport`, card muestra "Sin datos disponibles". |
| Sobreexposición de bloqueantes al usuario final (miedo a la app). | Copy claro y accionable; `assertive` solo al aparecer, no en cada render. |
| Divergencia entre estado del builder y estado persistido (0034). | Al cargar por deep-link, invalidar caché y volver a validar bajo demanda. |
