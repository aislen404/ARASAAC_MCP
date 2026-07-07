# Spec — Frontend Pixel Perfect Convergencia Serena

## MUST

### Composición

- MUST render a premium app shell with header, side rail, guided workspace, contextual help and bottom strip on desktop.
- MUST serve local SVG assets from `/convergencia-serena/` in Docker and local dev runtimes.
- MUST show a five-step guided flow: Definir, Explorar, Organizar, Validar, Compartir.
- MUST display progress and validation metric cards.
- MUST embed the real material builder workflow inside Convergencia Serena cards.
- MUST provide light and dark theme with semantic tokens.

### Functional governance

- MUST preserve ARASAAC real pictogram search and selection.
- MUST preserve human selection requirement.
- MUST preserve human review before export.
- MUST preserve attribution.
- MUST prevent export before approval.
- MUST preserve no-PII guidance.

### Accessibility

- MUST meet WCAG 2.2 AA contrast for text and controls.
- MUST expose visible focus states.
- MUST support keyboard navigation.
- MUST use clear labels and landmarks.
- MUST keep touch targets at least 44px.
- MUST avoid color-only state communication.

### Visual regression

- MUST provide Playwright screenshots for desktop/mobile and light/dark.
- MUST fail if horizontal overflow appears at 390px width.
- MUST fail if required shell zones are absent.

## SHOULD

- SHOULD use local SVG assets from `/convergencia-serena/`.
- SHOULD use subtle botanical motifs as signature, not decoration overload.
- SHOULD keep operational density calm and readable.
- SHOULD use `font-display` for major headings and `font-sans` for UI.

## MUST NOT

- MUST NOT generate or modify pictograms with AI.
- MUST NOT use external icon CDNs.
- MUST NOT implement dark theme by inversion.
- MUST NOT leave the home as a plain form.
- MUST NOT hide governance disclaimers.
