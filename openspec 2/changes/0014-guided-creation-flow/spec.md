# Spec — 0014-guided-creation-flow

## Capability

Flujo guiado de creación

## Scenarios

### Scenario 1 — ejecución nominal

**Given** el sistema está configurado correctamente  
**When** se ejecuta la capacidad  
**Then** produce una salida válida y trazable.

### Scenario 2 — entrada inválida

**Given** una entrada incompleta o inválida  
**When** se invoca la capacidad  
**Then** el sistema devuelve error estructurado sin efectos secundarios peligrosos.

### Scenario 3 — cumplimiento

**Given** la capacidad afecta a pictogramas, materiales, exportación o usuario  
**When** se genera o transforma información  
**Then** se respetan licencia, atribución, no PII y revisión humana si aplica.

## Acceptance Criteria

- Usuario puede crear borrador de agenda/tablero desde UI.
- Hay tests automatizados.
- Hay documentación mínima.
- No se incumplen reglas absolutas del AGENTS.md.
