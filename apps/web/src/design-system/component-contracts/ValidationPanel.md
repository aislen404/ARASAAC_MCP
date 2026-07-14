# ValidationPanel

## Propósito

Presentar la validación gobernada del material antes del envío a revisión,
haciendo visibles los bloqueos, avisos y comprobaciones correctas sin depender
solo del color.

## Anatomía obligatoria

- Eyebrow con paso visible.
- Título accesible `Validación del material`.
- Resumen con `role="status"` y `aria-live` dinámico.
- Acción primaria `Validar material`.
- Grupo de findings con heading propio.
- Etiqueta textual de severidad en cada finding.

## Estados

- inicial: invita a validar antes de enviar a revisión;
- loading: botón deshabilitado mientras se ejecuta la validación;
- ok: solo comprobaciones correctas;
- warning: permite continuar, pero exige revisión del contenido;
- blocker: impide enviar a revisión hasta corregir los findings.

## Accesibilidad

- El resumen usa `aria-live="assertive"` cuando existen bloqueos.
- Los findings se agrupan con `role="group"` y `aria-labelledby`.
- La severidad debe mostrarse siempre con texto visible: `Bloqueo`, `Aviso`,
  `Correcto`.
- El botón mantiene target mínimo de 44 px y foco visible.
- El componente no puede comunicar el estado solo con color.

## Contenido y gobernanza

- Nunca afirmar que la validación sustituye la revisión humana.
- Mantener lenguaje claro y accionable.
- No ocultar avisos de licencia, privacidad o uso no comercial.
- Si hay bloqueos, el flujo debe impedir el envío a revisión.

## Rechazo visual

Rechazar si el resumen no se entiende sin color, si los findings no están
agrupados semánticamente o si el estado bloqueante no es evidente por texto.