# CsMetricCards

## Propósito

Progreso del flujo guiado y validación de la colección actual. Los valores deben derivarse del estado real del builder (`phase`, `items`, `material`), nunca de datos inventados.

## Anatomía obligatoria

- Tarjeta de progreso: donut dinámico, porcentaje y resumen `N completados · M en curso · P pendientes`.
- Tarjeta de validación: tres bloques `.cs-stat-block` con totales, por revisar y correctos.
- Estado inicial honesto: 0%, `0 completados · 1 en curso · 4 pendientes`, validación `0/0/0`.

## Estados

- default (datos en tiempo real según flujo);
- actualización al cambiar fase o items.

## Accesibilidad

- `aria-label="Métricas del flujo"` en la sección.
- Labels legibles sin solapamiento de texto.

## Rechazo visual

Rechazar si muestra porcentajes o conteos hardcodeados (p. ej. 66%, 126 elementos).
