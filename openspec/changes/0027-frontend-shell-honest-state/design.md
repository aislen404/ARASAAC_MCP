# Design — Shell Honest State

## Principio rector

**Nunca mostrar progreso, colecciones o métricas que no provengan del estado real del builder.**

## Arquitectura de estado

```text
page.tsx
  MaterialFlowProvider
    MaterialBuilderProvider  ← useMaterialBuilder() único
      ConvergenciaSerenaApp
        CsMetricCards      ← useMaterialBuilderContext()
        CsContinueCard     ← useMaterialBuilderContext()
        CsSuggestionStrip  ← useMaterialBuilderContext() + useMaterialFlow()
      MaterialBuilder      ← useMaterialBuilderContext()
```

## Fórmulas de métricas (`workspace-metrics.ts`)

Basadas en 5 pasos del flujo y fase activa (`phase` 0–4):

| Campo | Fórmula |
|-------|---------|
| completados | `phase` |
| enCurso | `phase < 5 ? 1 : 0` |
| pendientes | `Math.max(0, 5 - phase - 1)` |
| progressPercent | `Math.round((phase / 5) * 100)` |
| totalItems | `items.length` |
| pendingReview | `material?.status === 'draft' \|\| 'rejected' ? 1 : 0` |
| correctItems | `items.filter(i => i.pictogram).length` |

## Cabecera

- Grid de 2 columnas: marca | acciones.
- `.cs-badge-row`: badges informativos, `role="list"`, no focusables.
- `.cs-header-controls`: chip editorial + toggle tema (`.cs-button`).

## Navegación lateral

Iconos SVG como `<img>` requieren `filter: brightness(0) invert(1)` en `[aria-current="page"]` para contraste sobre fondo `--cs-brand`.

## Sugerencias contextuales

Cuatro tarjetas derivadas de `workflowSteps` y `phase`, con anclas reales (`#crear`, `#cs-workflow`, `#cs-review`, `#cs-accessibility`). "Ver todas" apunta a `#cs-suggestions`.

## Feedback IA

`message`, `busy` y `aiStatus` visibles en la sección IA de `CreationForm`, no solo en `ReviewPanel`.

## Relación con 0026

0026 define composición visual; 0027 define veracidad funcional del shell sin alterar gobernanza del builder.
