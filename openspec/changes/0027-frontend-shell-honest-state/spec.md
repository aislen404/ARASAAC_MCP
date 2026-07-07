# Spec — Shell Honest State

## MUST

### Cabecera

- MUST NOT render a search input in `CsHeader`.
- MUST distinguish accessibility badges (informational) from the theme toggle (interactive button).
- MUST prevent badge overflow from obscuring controls on tablet/desktop breakpoints.

### Navegación

- MUST keep the active side-rail icon visible against the active background in light and dark themes.

### Métricas y estado honesto

- MUST derive progress metrics from the real flow phase (0% at start).
- MUST show `0 completados · 1 en curso · 4 pendientes` when no progress exists.
- MUST show validation counts `0 / 0 / 0` when no items exist.
- MUST NOT display invented collection names, percentages or item counts.

### Continuar

- MUST show "Sin borrador activo" when no title or material exists.
- MUST navigate to the builder (`#cs-builder`) and focus the title field on Continue click.

### Sugerencias

- MUST use consistent spacing between icons and text in suggestion cards.
- MUST link "Ver todas" to `#cs-suggestions`, not `#cs-builder`.
- MUST use actionable guidance aligned with the guided workflow, not fake popularity claims.

### Asistente IA

- MUST show AI server status, loading and error feedback in the creation step.
- MUST show dynamic button text while generating a plan.

### Gobernanza (sin cambios)

- MUST preserve ARASAAC real pictogram search and human review requirements.
- MUST NOT generate or modify pictogramas with AI.

## SHOULD

- SHOULD derive suggestions from current flow phase.
- SHOULD keep all metric and continue sections visible with honest empty state.

## MUST NOT

- MUST NOT introduce PII or fake user activity data.
- MUST NOT hide governance disclaimers.
