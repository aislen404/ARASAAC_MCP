# Asistente IA gobernado

## Propósito

La IA aporta planificación semántica sin convertirse en fuente de pictogramas ni
en decisor. Convierte una situación genérica en textos breves y términos de
búsqueda; el conector aprobado resuelve después esos términos contra ARASAAC y la
persona selecciona cada resultado.

## Límite de confianza

1. La UI exige confirmar que no existen datos personales o diagnósticos.
2. El backend aplica un guard local antes de enviar texto al proveedor.
3. Responses API recibe solo texto, sin tools, imágenes, URLs configurables ni
   acceso a MCP.
4. `store=False` solicita que la respuesta no se almacene en el endpoint.
5. La respuesta se valida mediante el schema Pydantic `AITextPlan`.
6. El servicio vuelve a validar texto y cantidad antes de consultar ARASAAC.
7. Los resultados ARASAAC conservan ID, origen, autor, propietario, licencia y
   fecha de recuperación.
8. La persona selecciona candidatos y continúa en el editor gobernado existente.

El prompt y la respuesta no se guardan en la base de datos ni se escriben en
logs. Una planificación fallida nunca crea material.

## Proveedor

El puerto `AIPlanner` permite sustituir el adaptador sin cambiar el dominio. La
implementación actual usa el SDK oficial de OpenAI, Responses API y structured
outputs. `gpt-5.4-mini` es el valor por defecto por latencia/coste para esta tarea
acotada y soporta structured outputs.

Referencias oficiales:

- <https://developers.openai.com/api/docs/guides/structured-outputs>
- <https://developers.openai.com/api/docs/models/gpt-5.4-mini>

## Operación segura

- `AI_PROVIDER=disabled` es el valor por defecto.
- La clave solo existe en `.env` local o en el gestor de secretos del despliegue.
- `/api/ai/status` no devuelve credenciales.
- No se admite una base URL arbitraria.
- El timeout se limita entre 2 y 60 segundos.
- Un fallo del proveedor devuelve 502/503/504 controlado y conserva el flujo manual.
