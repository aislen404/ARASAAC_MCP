# Implementation map — del frontend actual al contrato Round 3

## Estado actual observado

- `app/page.tsx` solo envuelve `AppShell` y `MaterialBuilder`.
- `AppShell` crea header, side rail, hero, guided flow, builder intro y footer.
- `MaterialBuilder` contiene toda la lógica funcional y renderiza formulario, IA, búsqueda, preview y revisión.
- `styles.css` define paneles, grids y tokens básicos.

## Cambio requerido

| Actual | Nuevo |
| --- | --- |
| `AppShell` dueño visual | `ConvergenciaSerenaApp` dueño visual |
| `MaterialBuilder` formulario central | `MaterialBuilder` embebido en cards premium |
| CSS global genérico | CSS Convergencia Serena por tokens/zonas |
| Hero + métricas básicas | Workspace completo con stepper + métricas + ayuda + sugerencias |
| Dark theme básico | Dark theme semántico y auditado |

## Orden recomendado de refactor

1. Crear assets y CSS sin tocar lógica.
2. Crear componentes shell con datos estáticos.
3. Conectar `MaterialBuilder` como slot.
4. Refactorizar `MaterialBuilder` visualmente.
5. Añadir tests visuales.
6. Ajustar responsive.
7. Eliminar estilos antiguos que entren en conflicto.
