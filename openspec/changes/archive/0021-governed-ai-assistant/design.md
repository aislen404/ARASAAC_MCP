# Design — 0021-governed-ai-assistant

## Flujo

```text
escenario genérico
  → guard local de privacidad y uso
  → proveedor IA de texto con JSON Schema estricto
  → validación Pydantic de salida no confiable
  → búsquedas acotadas en ARASAAC
  → grupos de candidatos reales
  → selección humana
  → editor existente
  → revisión humana existente
  → exportación gobernada existente
```

## Componentes

- `AIPlanner` define el puerto interno y evita acoplar dominio y rutas a un SDK.
- `OpenAIPlanner` usa Responses API, salida estructurada, `store=False`, timeout
  acotado y el modelo configurado solo en servidor.
- `UnavailablePlanner` mantiene el API y el flujo manual disponibles sin secreto.
- `PrivacyGuard` rechaza patrones evidentes de contacto, identificadores y
  lenguaje diagnóstico antes de cualquier llamada externa. La UI exige además una
  confirmación explícita de que el escenario es genérico y no contiene PII.
- `AIPlanningService` vuelve a validar la salida, limita cantidad y longitud, y
  resuelve términos mediante el conector ARASAAC aprobado.
- El frontend muestra procedencia IA, límites y candidatos por concepto. Cada
  incorporación al material requiere pulsar un botón de selección.

## Límites de confianza

- El texto del usuario y la salida del modelo son datos no confiables.
- No se envía al proveedor el catálogo ARASAAC ni se solicitan imágenes.
- El modelo no recibe tools y no puede efectuar llamadas de red.
- No se acepta una URL configurable del proveedor para evitar exfiltración.
- No se registran prompts ni respuestas; solo estado técnico sin contenido.
- La clave nunca se expone al frontend, a respuestas HTTP ni a logs.
- Un rechazo, timeout, schema inválido o fallo ARASAAC produce un error controlado
  y no crea material.

## Configuración

- `AI_PROVIDER=disabled|openai` (por defecto `disabled`).
- `OPENAI_API_KEY` solo en entorno de servidor.
- `OPENAI_MODEL=gpt-5.4-mini` configurable sin cambios de código.
- `AI_TIMEOUT_SECONDS` limitado a un rango seguro.

La imagen Docker admite la dependencia del SDK, pero el servicio puede arrancar y
pasar healthcheck sin clave. Docker Compose reenvía las variables sin incluir
secretos en el repositorio.

## Observabilidad

`GET /api/ai/status` informa disponibilidad, proveedor y modelo, nunca credenciales.
Las respuestas de planificación identifican el proveedor y declaran
`requires_human_selection=true` y `creates_material=false`.
