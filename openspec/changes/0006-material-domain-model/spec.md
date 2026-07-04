# Spec — 0006-material-domain-model

## Escenarios

### Crear borrador

**Dado** un título genérico y bloques válidos
**Cuando** se crea un material
**Entonces** nace en estado `draft`, versión 1 y sin identidad personal.

### Registrar pictograma

**Dado** un bloque con pictograma
**Cuando** se valida el material
**Entonces** la referencia incluye toda la trazabilidad de licencia.

### Rechazar PII

**Dado** un payload con campos adicionales como nombre, email o diagnóstico
**Cuando** se valida
**Entonces** Pydantic lo rechaza por schema estricto.

### Controlar revisión

**Dado** un borrador
**Cuando** se solicita revisión
**Entonces** pasa a `in_review`; solo una decisión humana explícita puede
convertirlo en `approved`.
