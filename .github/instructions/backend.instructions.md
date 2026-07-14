<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: db08a16d5c85 -->
---
description: Reglas backend — ARASAAC Social MCP Platform
applyTo: "apps/api/**,packages/domain/**,packages/contracts/**,services/api/**"
---

# Reglas backend

- Stack: Python + FastAPI + Pydantic.
- Contratos con OpenAPI/Pydantic; servicios de dominio aislados.
- No persistir PII en MVP.
- Toda exportación valida licencia, atribución y revisión humana.
- Tests de API y dominio obligatorios por OpenSpec.

**Globs sugeridos:** `apps/api/**`, `packages/domain/**`, `packages/contracts/**`
