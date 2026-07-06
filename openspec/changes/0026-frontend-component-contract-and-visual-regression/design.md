# Design — Convergencia Serena Component Contract

## Principio rector

La interfaz debe comunicar tres ideas en los primeros tres segundos:

1. **Aquí hay un camino guiado.**
2. **Cada decisión importante es humana.**
3. **La accesibilidad no es un añadido; es la estructura del producto.**

## Layout desktop ≥ 1280 px

```text
┌────────────────────────────────────────────────────────────────────┐
│ Header: marca + búsqueda + garantías + usuario + theme              │
├───────────────┬──────────────────────────────────────────┬─────────┤
│ SideRail      │ Main Guided Workspace                    │ Help    │
│               │ - Hero compacto                          │ Context │
│               │ - Stepper 5 fases                        │         │
│               │ - Métricas progreso/validación           │         │
│               │ - Builder funcional embebido             │         │
│               │ - Sugerencias                            │         │
├───────────────┴──────────────────────────────────────────┴─────────┤
│ Bottom strip: paleta, principios y garantías                         │
└────────────────────────────────────────────────────────────────────┘
```

## Layout tablet 768–1279 px

- Header compacto.
- SideRail se convierte en nav horizontal o drawer.
- HelpContext baja debajo del workspace.
- Builder ocupa ancho completo.

## Layout móvil < 768 px

- App real en una columna.
- Stepper horizontal con overflow controlado o versión compacta.
- Panels en una columna.
- Bottom actions sticky solo si no interfiere con lectura.

## Zonas visuales obligatorias

1. `CsHeader`: marca, búsqueda, garantías, usuario, toggle.
2. `CsSideRail`: navegación contextual con iconos, estados y ayuda.
3. `CsGuidedWorkspace`: contenedor principal con stepper, métricas y slots.
4. `CsContextHelp`: panel de ayuda, ilustración, consejo accesible.
5. `CsBottomStrip`: tokens, principios, cumplimiento.

## Estados obligatorios

Todos los componentes interactivos deben tener:

- default;
- hover;
- focus-visible;
- active/pressed;
- selected/current;
- disabled;
- loading cuando aplique;
- error/warning/success donde aplique.

## Relación con MaterialBuilder

`MaterialBuilder` deja de ser el dueño visual de la página. Debe convertirse en proveedor funcional de:

- configuración;
- búsqueda de pictogramas;
- preview editable;
- revisión/exportación.

Cada zona debe renderizarse dentro de cards Convergencia Serena.

## Dark theme

Dark theme debe tener tokens propios:

- fondo: midnight/navy;
- superficies: graphite/slate;
- texto: ivory;
- acento primario: sage/cyan;
- acento crítico: amber/copper;
- foco: cyan/blue visible;
- sombras: glow sutil + bordes.

No usar `filter: invert()` ni inversión automática.
