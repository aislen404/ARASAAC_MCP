# Spec — 0023-frontend-convergencia-serena

## Capability

Experiencia frontend accesible Convergencia Serena integrada con el flujo
gobernado real.

## Escenarios

### Escenario 1 — shell de producto

**Dado** que se visita `/`
**Cuando** carga la aplicación
**Entonces** se muestra una navegación de producto, orientación contextual y el
constructor gobernado existente.

### Escenario 2 — flujo guiado semántico

**Dado** el área principal
**Cuando** se consulta el recorrido
**Entonces** aparecen cinco fases con estado textual y la fase activa usa
`aria-current="step"`.

### Escenario 3 — tema accesible

**Dado** el control de tema
**Cuando** se activa
**Entonces** cambia entre claro y oscuro, actualiza `aria-pressed`, conserva foco
visible y persiste la preferencia localmente.

### Escenario 4 — flujo gobernado preservado

**Dado** el nuevo shell
**Cuando** se usa el constructor
**Entonces** siguen disponibles configuración, búsqueda/selección real, edición,
revisión humana y exportación bloqueada hasta aprobación.

### Escenario 5 — atribución y cumplimiento

**Dado** cualquier tema o viewport
**Cuando** se revisa la interfaz
**Entonces** la atribución ARASAAC y la revisión humana obligatoria permanecen
visibles, y no se introducen PII ni imágenes generadas.

### Escenario 6 — responsive y teclado

**Dado** un viewport móvil o navegación por teclado
**Cuando** se recorre la interfaz
**Entonces** no hay overflow horizontal, los controles tienen orden lógico,
targets mínimos y foco visible.

### Escenario 7 — accesibilidad automatizada

**Dado** el frontend renderizado
**Cuando** se ejecuta axe
**Entonces** no existen violaciones serious o critical en WCAG A/AA.

## Criterios de aceptación

- Diseño light/dark coherente y sin dependencias externas.
- Constructor y garantías actuales preservados.
- Navegación y flujo guiado semánticos.
- Cobertura frontend igual o superior al 75%.
- Lint, typecheck, unitarios, Playwright y OpenSpec pasan.
