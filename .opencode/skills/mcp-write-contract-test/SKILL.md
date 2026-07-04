---
name: mcp-write-contract-test
description: Skill mcp/write contract test para ARASAAC Social MCP Platform. Requiere OpenSpec aprobada.
metadata:
  domain: mcp
  requires_openspec: true
---

# skill.mcp.write_contract_test

## Propósito

Ejecutar la capacidad `skill.mcp.write_contract_test` dentro del flujo OpenSpec del proyecto.

## Entradas esperadas

- Contexto de la change OpenSpec activa.
- Artefactos relevantes (`proposal.md`, `design.md`, `tasks.md`, `spec.md`).
- Datos de dominio necesarios para `mcp/write_contract_test`.

## Salida esperada

```text
status: pass | warn | fail
summary: <resumen>
artifacts: <artefactos generados o modificados>
risks: <riesgos>
next_actions: <acciones>
```

## Gates

- Trabajar siempre contra OpenSpec aprobada.
- No generar ni modificar pictogramas ARASAAC.
- No exportar sin revisión humana aprobada.
- No introducir datos personales en MVP.
- Preservar atribución visible CC BY-NC-SA.
