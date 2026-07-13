# Design — 0031 Embedded Draft Feedback

## Principio rector

**La acción debe confirmar su resultado en el mismo contexto visual en el que el usuario la ejecuta.**

## Estado existente

`useMaterialBuilder()` ya centraliza:

- `message`
- `busy`
- `material`
- `createMaterial()`

La lógica de dominio no requiere cambios. El problema es de presentación del estado:

- `EditorPanel` no renderiza `message`.
- `ReviewPanel` oculta `message` cuando `embedded = true`.
- `CreationForm` sí renderiza `message` en embebido, pero dentro del bloque IA, lejos del botón `Crear borrador`.

## Cambio de UI

### `EditorPanel`

- Renderizar un bloque de feedback con `aria-live="polite"` y `role="status"` cerca del botón `Crear borrador`.
- Reutilizar `message` del builder como única fuente de verdad.
- Mantener el botón deshabilitado cuando `busy` o `material !== null`.

### `ReviewPanel`

- Mostrar `message` también en modo embebido.
- Mantener visible el estado del material (`draft`, `in_review`, etc.) para reforzar el cambio de fase.

## Accesibilidad

- El feedback debe ser legible y anunciable por tecnologías asistivas.
- No depender solo del cambio de estado del botón para comunicar éxito.
- Mantener foco estable; no se introduce movimiento forzado en esta iteración.

## Testing

Añadir cobertura para comprobar que en modo embebido:

1. Al crear borrador aparece un mensaje visible.
2. El panel de revisión refleja estado `draft`.
3. El usuario puede identificar el siguiente paso (`Enviar a revisión`).
