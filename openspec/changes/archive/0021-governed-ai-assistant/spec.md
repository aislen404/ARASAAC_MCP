# Spec — 0021-governed-ai-assistant

## Estado

- `GET /api/ai/status` devuelve si la IA está configurada, el proveedor activo,
  el modelo y los límites de gobernanza.
- La ausencia de `OPENAI_API_KEY` no impide arrancar API, web, MCP ni el flujo
  manual.
- Ninguna respuesta expone claves o valores secretos.

## Planificación

- `POST /api/ai/plan` exige tipo de material, escenario genérico, número limitado
  de elementos, locale soportado y confirmación literal de ausencia de datos
  personales.
- El input rechaza campos extra, texto vacío, longitud excesiva, contacto,
  identificadores evidentes y lenguaje de diagnóstico.
- El proveedor solo puede devolver texto mediante un JSON Schema estricto con el
  número solicitado de elementos, cada uno con texto visible y término de búsqueda.
- La salida del modelo se valida de nuevo y se rechaza si contiene patrones
  prohibidos o incumple límites.
- Cada término se resuelve por el conector aprobado y devuelve candidatos que son
  referencias ARASAAC completas e inmutables.
- La respuesta declara selección humana obligatoria y que no crea material.

## Gobernanza

- No se invoca ningún modelo o endpoint de generación/edición de imágenes.
- El modelo no dispone de tools, web, filesystem, shell ni MCP.
- El servicio no selecciona automáticamente un pictograma.
- El servicio no persiste prompt, respuesta ni plan.
- El servicio no crea, envía a revisión, aprueba ni exporta materiales.
- Cualquier material posterior continúa sujeto al flujo de revisión humana.
- No se añade ninguna tool MCP.

## UX y accesibilidad

- El asistente se identifica como opcional y no sustituye criterio profesional.
- La UI avisa que solo admite escenarios genéricos sin nombres, contacto,
  diagnósticos ni datos sensibles.
- La persona confirma el cumplimiento antes de solicitar un plan.
- Los candidatos se presentan agrupados por concepto y con controles de selección
  etiquetados para teclado y lector de pantalla.
- El estado de carga, los rechazos de privacidad y los fallos del proveedor se
  anuncian mediante una región viva sin perder el trabajo.
- El flujo manual permanece disponible aunque la IA esté desactivada.

## Verificación

- Tests cubren proveedor disponible/no disponible, schema inválido, timeout,
  guard de privacidad, fallo ARASAAC, respuesta segura y no auto-selección.
- Playwright cubre planificación, selección humana, edición, revisión y bloqueo de
  exportación previo a aprobación.
- Cobertura backend y frontend se mantiene por encima del 75%.
- Lint, typecheck, build, OpenSpec y Docker Compose pasan.
