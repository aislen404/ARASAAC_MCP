# CsSuggestionStrip

## Propósito

Sugerencias contextuales alineadas con el flujo guiado. Cada tarjeta enlaza a una ancla real del workspace.

## Anatomía obligatoria

- Título "Sugerencias para ti" y enlace "Ver todas →" a `#cs-suggestions`.
- Grid `.cs-suggestion-grid` con tarjetas `.cs-suggestion-card`.
- Espaciado mínimo 12px entre ilustración y título.
- Cuatro sugerencias derivadas de `workflowSteps` y fase activa.

## Estados

- default;
- hover/focus en tarjetas enlazadas.

## Accesibilidad

- Enlaces con texto descriptivo.
- Focus visible en tarjetas.

## Rechazo visual

Rechazar si "Ver todas" apunta a `#cs-builder`, si hay claims falsos de popularidad o si el texto se solapa con los iconos.
