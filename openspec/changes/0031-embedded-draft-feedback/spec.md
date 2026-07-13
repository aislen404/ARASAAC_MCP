# Spec — Embedded Draft Feedback

## MUST

### Confirmación de creación

- MUST show visible feedback near `Crear borrador` when the draft is created in embedded mode.
- MUST announce that feedback through an accessible live region.
- MUST keep using the shared builder message as the source of truth.

### Paso de revisión

- MUST show the current builder message in embedded `ReviewPanel`.
- MUST reflect material status as `draft` after successful creation.
- MUST make the next available action perceivable after draft creation.

### Gobernanza

- MUST preserve existing backend endpoints and workflow transitions.
- MUST NOT change ARASAAC governance, attribution or human review rules.

## SHOULD

- SHOULD keep feedback text close to the action that triggered it.
- SHOULD reduce ambiguity without forcing automatic focus movement.

## MUST NOT

- MUST NOT introduce fake progress or synthetic success states.
- MUST NOT depend only on button disabled state to communicate success.
