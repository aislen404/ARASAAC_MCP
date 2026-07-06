# CsWorkflowStepper

## Propósito

Cinco pasos. Debe comunicar progreso sin depender solo del color. Estados: active, done, pending.

## Anatomía obligatoria

- Header interno o título accesible.
- Icono local cuando aporte reconocimiento.
- Copy breve y accionable.
- Estado visual claro.
- Focus visible en controles.

## Estados

- default;
- hover;
- focus-visible;
- selected/current si aplica;
- disabled si aplica;
- loading/error/success si aplica.

## Accesibilidad

- Usar `aria-label` cuando el texto visible no baste.
- No comunicar estado solo por color.
- Mantener targets mínimos de 44px.
- Orden de tabulación lógico.
- Contraste AA mínimo.

## Rechazo visual

Rechazar si el componente parece genérico, si pierde el lenguaje Convergencia Serena o si rompe la composición premium.
