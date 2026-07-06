# Proposal — 0023-frontend-convergencia-serena

## Problema

El frontend ya implementa el flujo gobernado de creación, selección de
pictogramas reales, revisión y exportación, pero su presentación sigue siendo
principalmente técnica. No ofrece todavía una identidad visual consistente,
orientación de producto ni tema claro/oscuro.

El paquete recibido `arasaac_frontend_convergencia_serena` define una dirección
visual válida, pero fue redactado para un MVP-0 anterior. Copiarlo literalmente
ocultaría capacidades reales y entraría en conflicto con OpenSpecs existentes.

## Solución propuesta

Adaptar la línea **Convergencia Serena** al producto actual:

- incorporar tokens light/dark y componentes accesibles reutilizables;
- envolver el constructor gobernado existente en una experiencia guiada;
- mostrar navegación, progreso, métricas y ayuda contextual sin convertir datos
  ficticios en afirmaciones operativas;
- conservar selección humana, atribución, controles de privacidad y bloqueos de
  exportación;
- mantener ARASAAC como única fuente de pictogramas y no generar recursos
  visuales con IA.

## Alcance

- Sistema visual y documentación Convergencia Serena.
- App shell responsive con navegación principal.
- Theme toggle accesible y persistente.
- Flujo guiado de cinco fases adaptado al flujo real.
- Métricas descriptivas, ayuda contextual y badges de accesibilidad.
- Integración visual del `MaterialBuilder` sin alterar sus contratos.
- Tests unitarios, Playwright y axe.

## Fuera de alcance

- Cambios en backend, API ARASAAC, MCP, modelos de dominio o exportadores.
- Nuevos pictogramas, transformación de pictogramas o generación de imágenes.
- Autenticación, PII o personalización por persona.
- Nuevas tools MCP.

## Riesgos y mitigaciones

- **Regresión del flujo real:** mantener `MaterialBuilder` y sus tests de contrato.
- **Sobrecarga cognitiva:** navegación compacta, jerarquía clara y ayuda breve.
- **Estados dependientes del color:** reforzar con texto, forma y semántica.
- **Flicker de tema:** inicialización local sin dependencias ni llamadas externas.
- **Confundir métricas demo con telemetría:** etiquetarlas como estado del flujo,
  no como datos de usuarios o impacto real.
