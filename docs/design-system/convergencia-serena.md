# Convergencia Serena — sistema de diseño

Convergencia Serena combina claridad editorial, calma operativa y accesibilidad
explícita. La interfaz acompaña el flujo real del producto: definir, explorar
pictogramas reales, organizar, validar y someter el material a revisión humana.

## Principios

1. La siguiente acción siempre es comprensible.
2. Los estados usan texto o forma además del color.
3. La atribución y los límites de privacidad permanecen visibles.
4. Light y dark comparten jerarquía, no solo una inversión cromática.
5. La decoración nunca imita ni sustituye pictogramas ARASAAC.

## Implementación

- Tokens: `apps/web/src/design-system/tokens.css`.
- Componentes: `apps/web/src/components/`.
- Integración: `apps/web/src/app/page.tsx`.
- Tests: unitarios, Playwright, teclado, responsive y axe.

## Límites

La capa visual no altera el origen de pictogramas, la selección humana, el gate
de revisión, la atribución, las restricciones de PII ni las tools MCP.
