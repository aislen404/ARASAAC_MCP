# Design — 0009-accessible-document-generator

## Decisiones de diseño

- Implementar de forma incremental.
- Mantener contratos claros.
- Añadir validaciones automáticas.
- Registrar auditoría cuando haya generación, pictogramas o exportación.
- Mantener separación entre dominio, infraestructura y presentación.

## Contratos esperados

- Inputs tipados.
- Outputs serializables.
- Errores estructurados.
- Tests de contrato si la capacidad expone API o MCP.

## Seguridad y cumplimiento

- No almacenar datos personales salvo que una spec futura lo apruebe expresamente.
- No ejecutar comandos arbitrarios.
- No omitir licencia ni atribución.
- No crear ni modificar pictogramas ARASAAC.

## Observabilidad

Registrar eventos relevantes con correlation_id, material_id si existe, tool_name si existe y resultado.
