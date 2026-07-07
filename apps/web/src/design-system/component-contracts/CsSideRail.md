# CsSideRail

## Propósito

Navegación contextual del espacio de trabajo con iconos locales y estados activos claros.

## Anatomía obligatoria

- Lista de enlaces con icono en `.cs-icon-box`.
- Item activo con `aria-current="page"`.
- Bloque de gobernanza al pie.

## Estados

- default, hover, focus-visible;
- activo: fondo `--cs-brand`, texto `--cs-brand-contrast`, icono invertido visible.

## Accesibilidad

- `nav` con `aria-label`.
- Icono activo debe mantener contraste AA sobre fondo de marca.
- Targets mínimos 44px.

## Rechazo visual

Rechazar si el icono del item activo es invisible sobre el fondo oscuro.
