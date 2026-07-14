<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: 3a874a291c68 -->
---
name: human-review-gate
description: Solicitar, aprobar o rechazar revisión humana de un material con trazabilidad.
inputs:
  - material_id
  - action     # request | approve | reject
  - reviewer   # (para approve/reject)
  - reason     # (para reject)
outputs:
  - Estado del material actualizado
  - Registro de auditoría (reviewer, timestamp, versión hash, motivo si reject)
invoked_by_agents: [verify]
gates: [human_review]
---

# Skill: human-review-gate

## Cuándo usarla
- Un material está listo para revisión (estado `draft` completo).
- Un reviewer humano aprueba o rechaza.
- Antes de cualquier export (obligatorio por regla absoluta #5).

## Procedimiento paso a paso

### Acción `request`
1. Verificar que el material tiene todo el contenido necesario (no borradores vacíos).
2. Ejecutar [`compliance-scan`](../compliance-scan/SKILL.md) primero. Si hay FAIL en license/privacy, **detener** y avisar al autor.
3. Cambiar estado: `draft` → `in_review`.
4. Notificar a reviewers configurados (email/webhook según config).
5. Registrar en audit log: `material_id`, `requested_by`, `timestamp`, `version_hash`.

### Acción `approve`
1. Verificar que el reviewer no es el mismo que el autor (separation of duties).
2. Requerir input explícito: reviewer identifica su nombre y rol.
3. Registrar en audit log:
   ```json
   {
     "material_id": "abc-123",
     "reviewer": "Ana García (coordinadora CEE)",
     "action": "approve",
     "version_hash": "sha256:...",
     "timestamp": "2025-01-20T16:00:00Z"
   }
   ```
4. Cambiar estado: `in_review` → `approved`.
5. Habilitar acción de export.

### Acción `reject`
1. Requerir `reason` no vacío (mínimo 20 caracteres).
2. Registrar en audit log con reason.
3. Cambiar estado: `in_review` → `draft` (permite editar).
4. Notificar al autor con el motivo.

## Gate `human_review` — condiciones

| Condición | Requerido |
|---|---|
| Reviewer humano identificado | ✅ Sí |
| Separación autor/reviewer | ✅ Sí |
| Versión hash congelada | ✅ Sí |
| Timestamp inmutable | ✅ Sí |
| Motivo si rechazado | ✅ Sí |
| Aprobación automática por IA | ❌ Nunca |

## Errores comunes

- ❌ Aprobar sin registrar reviewer → auditoría rota, viola regla absoluta #5.
- ❌ Autor aprueba su propio material → conflicto de interés.
- ❌ Aprobar `draft` (sin pasar por `in_review`) → salta el flujo.
- ❌ Editar `approved` sin volver a `draft` → invalida la aprobación.
- ❌ Rechazar sin motivo → autor no sabe qué corregir.

## Ver también

- Persona: `.agents/personas/qa.persona.md`
- Regla: `.agents/rules/mandatory-gates.md#gate-3--human_review`
- Skill: [`material-pipeline`](../material-pipeline/SKILL.md)
