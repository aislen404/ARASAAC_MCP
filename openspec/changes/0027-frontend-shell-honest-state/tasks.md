# Tasks — 0027

## 1. OpenSpec

- [x] Crear `proposal.md`, `design.md`, `tasks.md`, `spec.md`.
- [x] Ejecutar `make openspec-verify`.

## 2. Contexto compartido

- [x] Crear `builder-context.tsx` con `MaterialBuilderProvider` y `useMaterialBuilderContext`.
- [x] Actualizar `page.tsx` y `MaterialBuilder` para usar el provider.

## 3. Cabecera

- [x] Eliminar buscador de `CsHeader`.
- [x] Reajustar grid CSS header a 2 columnas.
- [x] Separar badges (informativos) de controles (toggle tema).
- [x] Actualizar estilos responsive.

## 4. Navegación lateral

- [x] Corregir contraste icono activo en CSS (`aria-current="page"`).

## 5. Métricas reales

- [x] Crear `workspace-metrics.ts` con funciones puras.
- [x] Convertir `CsMetricCards` a client component conectado al contexto.
- [x] Añadir `.cs-stat-block` para evitar overflow de textos.

## 6. Continuar

- [x] Convertir `CsContinueCard` a client component.
- [x] Estado vacío honesto y datos reales del builder.
- [x] Botón con scroll/focus a `#cs-builder`.

## 7. Sugerencias

- [x] Maquetación `.cs-suggestion-grid` / `.cs-suggestion-card`.
- [x] Sugerencias contextuales por fase.
- [x] "Ver todas" → `#cs-suggestions`.

## 8. Asistente IA

- [x] Mostrar `message`, `busy` y errores en sección IA de `CreationForm`.
- [x] Texto dinámico en botón generar.

## 9. Contratos

- [x] Actualizar contratos de `CsHeader`, `CsMetricCards`, `CsContinueCard`, `CsSuggestionStrip`, `CsSideRail`.

## 10. Tests

- [x] Unit: `workspace-metrics.test.ts`, componentes shell, IA en embedded.
- [x] E2E: `convergencia-serena.honest-state.spec.ts`.
- [x] Regenerar snapshots visuales.
- [x] `make lint`, `make typecheck`, `make test`.
