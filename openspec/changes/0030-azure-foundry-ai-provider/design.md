# Design — 0030-azure-foundry-ai-provider

## Configuración

| Variable | Obligatoria | Descripción |
|----------|-------------|-------------|
| `AI_PROVIDER` | Sí | `disabled`, `openai` o `azure` |
| `AZURE_OPENAI_ENDPOINT` | Si `azure` | Base HTTPS del recurso, p. ej. `https://<recurso>.openai.azure.com/openai/v1` |
| `AZURE_OPENAI_API_KEY` | Si `azure` | Clave del recurso Azure (solo servidor) |
| `AZURE_OPENAI_MODEL` | No | Nombre del despliegue; por defecto `gpt-5.4-mini` |

## Seguridad

- Solo se aceptan endpoints `https://*.openai.azure.com` con ruta `/openai/v1`.
- Se normaliza la URL (sin barra final, añade `/openai/v1` si falta).
- La clave nunca sale del servidor ni aparece en logs.
- No se permite URL arbitraria para evitar exfiltración.

## Cliente

`AsyncOpenAI` del SDK oficial con `base_url` apuntando al endpoint Azure v1
compatible con Responses API y salida estructurada.
