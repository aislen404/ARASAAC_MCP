# Spec — 0030-azure-foundry-ai-provider

## Escenario: Azure configurado correctamente

**Dado** `AI_PROVIDER=azure`, endpoint válido `*.openai.azure.com/openai/v1` y clave presente  
**Cuando** se consulta `GET /api/ai/status`  
**Entonces** `available=true`, `provider=azure` y `model` informa el despliegue configurado

## Escenario: Endpoint no permitido

**Dado** `AI_PROVIDER=azure` y `AZURE_OPENAI_ENDPOINT=https://evil.example.com/openai/v1`  
**Cuando** se consulta `GET /api/ai/status`  
**Entonces** `available=false` y `reason` explica que el host no está permitido

## Escenario: OpenAI directo sin cambios

**Dado** `AI_PROVIDER=openai` y `OPENAI_API_KEY` presente  
**Cuando** se consulta `GET /api/ai/status`  
**Entonces** el comportamiento existente se mantiene
