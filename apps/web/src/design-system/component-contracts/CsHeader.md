# CsHeader

## Propósito

Marca, garantías de accesibilidad y acciones globales (chip editorial y toggle de tema). Debe permanecer sticky en desktop y estático en móvil. No incluye buscador global en MVP.

## Anatomía obligatoria

- Marca ARASAAC con monograma local.
- Fila de badges informativos (`role="list"`), no interactivos.
- Controles en `.cs-header-controls`: chip editorial y botón de tema.
- Focus visible en el toggle de tema.

## Estados

- Badges: solo default (informativos).
- Toggle tema: default, hover, focus-visible, pressed (`aria-pressed`).

## Accesibilidad

- Badges no deben ser focusables ni confundirse con botones.
- Toggle debe distinguirse visualmente de los badges.
- Contraste AA mínimo.

## Rechazo visual

Rechazar si aparece un buscador sin función, si los badges desbordan los controles o si el toggle parece otro badge.
