# CsContinueCard

## Propósito

Retomar el borrador actual o invitar al área de trabajo cuando no hay progreso. Debe reflejar el título real del builder o mostrar "Sin borrador activo".

## Anatomía obligatoria

- Ilustración landscape (light/dark).
- Título del borrador o mensaje de estado vacío.
- Contador `{phase} de 5 pasos completados`.
- Botón que hace scroll a `#cs-builder` y enfoca `#material-title`.

## Estados

- Sin borrador: "Sin borrador activo", botón "Ir al área de trabajo".
- Con borrador: título visible, botón "Continuar".

## Accesibilidad

- Botón con target mínimo 44px.
- Texto comprensible sin datos personales.

## Rechazo visual

Rechazar si muestra colecciones ficticias o un botón sin acción.
