# Proposal — 0030-azure-foundry-ai-provider

## Problema

La capa IA usa `api.openai.com` directamente. El equipo dispone de un recurso Azure
AI Foundry / Azure OpenAI con endpoint regional (`*.openai.azure.com/openai/v1`) que
ofrece mejor control de red, facturación y cumplimiento.

## Solución

Añadir `AI_PROVIDER=azure` con variables de entorno dedicadas y validación estricta
del host permitido (`*.openai.azure.com`). Mantener `openai` y `disabled` sin cambios.

## Alcance

- Backend: factory del planner, mensajes de error más claros para cuota/tasa.
- Config: `docker-compose.yml`, `.env.example`, README.
- Tests unitarios del factory y validación de endpoint.

## Fuera de alcance

- Autenticación con Managed Identity (futuro).
- Otros proveedores o URLs arbitrarias.
