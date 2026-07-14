---
name: mcp-tool-scaffold
description: Definir schema MCP estricto, implementar tool con seguridad, escribir contract test y validación.
inputs:
  - tool_name       # kebab-case
  - purpose         # 1 sentence
  - input_schema    # JSON Schema (Pydantic)
  - output_schema   # JSON Schema (Pydantic)
outputs:
  - packages/mcp-contracts/tools/<tool_name>.py (schema)
  - services/mcp/tools/<tool_name>.py (impl)
  - services/mcp/tests/test_<tool_name>.py (contract test)
invoked_by_agents: [build]
gates: []
---

# Skill: mcp-tool-scaffold

## Cuándo usarla
- Añades una nueva tool, resource o prompt MCP.
- Modificas contrato de una tool existente.

## Procedimiento paso a paso

1. **Definir schema estricto** con Pydantic v2 en `packages/mcp-contracts/tools/<tool_name>.py`:
   - Todos los campos con tipo explícito.
   - `Field(..., description="…")` en cada uno.
   - `model_config = ConfigDict(extra="forbid")` (no extra fields).
   - Ejemplo `Examples` en el schema para el descriptor MCP.
2. **Añadir a allowlist** en `services/mcp/registry.py`. Si no está en la allowlist, el server no la expone.
3. **Implementar handler** en `services/mcp/tools/<tool_name>.py`:
   - Signature: `async def handle(input: <Tool>Input) -> <Tool>Output`.
   - Sin acceso a filesystem arbitrario (usa rutas whitelisted).
   - Sin `subprocess`, sin `eval`, sin ejecución arbitraria.
   - Validar side-effects (audit log si aplica).
4. **Registrar en el server** (declarativamente, no imperativo).
5. **Contract test** en `services/mcp/tests/test_<tool_name>.py`:
   - Input válido → output válido.
   - Input inválido → error estructurado (no crash).
   - Casos límite (empty, muy grande, unicode).
   - Verificar que output cumple el schema (round-trip).
6. **Security review**: aplica checklist de `personas/security.persona.md`.
7. **Documentar** en `docs/architecture/mcp-dual-surface.md`.

## Ejemplo mínimo

```python
# packages/mcp-contracts/tools/search_pictogram.py
from pydantic import BaseModel, Field, ConfigDict

class SearchPictogramInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(..., min_length=1, max_length=100)
    locale: str = Field("es", pattern="^(es|en|fr|pt|ca|gl|eu)$")
    limit: int = Field(10, ge=1, le=50)

class SearchPictogramOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    results: list[dict]
    total: int
```

## Errores comunes

- ❌ Omitir `extra="forbid"` → inputs no controlados.
- ❌ No añadir a allowlist → tool no se expone (o peor, sí se expone sin validar).
- ❌ Handler que hace `os.system`, `subprocess`, `eval` → viola regla absoluta #9.
- ❌ Devolver dict sin schema → el cliente no sabe qué esperar.
- ❌ Sin contract test → cualquier cambio rompe integraciones silenciosamente.

## Ver también

- Regla: `.agents/rules/mcp.md`
- Persona: `.agents/personas/mcp-architect.persona.md`
- Persona: `.agents/personas/security.persona.md`
- Doc: `docs/architecture/mcp-dual-surface.md`
