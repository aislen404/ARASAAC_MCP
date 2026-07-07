# Proposal — 0021-governed-ai-assistant

## Problema

El MVP permite construir materiales mediante búsqueda manual, pero no demuestra cómo
una capa de IA puede reducir el trabajo de convertir una situación genérica en una
estructura accesible. La IA no puede generar, imitar ni modificar pictogramas
ARASAAC, decidir por una persona ni saltarse la revisión humana.

## Propuesta

Añadir un asistente opcional que:

1. transforma una descripción genérica y no personal en un plan textual estructurado;
2. valida la salida del modelo con un schema estricto;
3. busca cada concepto exclusivamente en la API oficial de ARASAAC;
4. presenta varios candidatos reales para selección humana explícita;
5. entrega los elementos seleccionados al editor y flujo de revisión existentes.

La integración será desacoplada del proveedor, desactivada cuando no exista una
clave de servidor y no tendrá acceso a generación de imágenes, herramientas, web,
filesystem, MCP ni ejecución de código.

## Fuera de alcance

- Generación, edición o imitación de pictogramas.
- Selección automática del pictograma definitivo.
- Diagnóstico o recomendación individual.
- Entrada o persistencia de PII o datos sensibles.
- Creación, aprobación o exportación automática de materiales.
- Nuevas tools MCP.
