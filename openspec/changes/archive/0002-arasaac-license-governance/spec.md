# Spec — 0002-arasaac-license-governance

## Escenarios

### Metadatos válidos

**Dado** un pictograma real recuperado de ARASAAC
**Cuando** se registra su uso
**Entonces** se conservan ID, label, URL, autor, propietario, licencia y fecha.

### Metadatos inválidos

**Dado** un recurso con origen, autor, propietario o licencia distintos
**Cuando** se valida
**Entonces** la operación falla con error estructurado.

### Atribución visible

**Dado** un material que contiene pictogramas
**Cuando** se prepara para revisión o exportación
**Entonces** contiene el texto oficial visible y declara uso no comercial.

### Señalética

**Dado** un material de tipo señalética
**Cuando** se valida su cumplimiento
**Entonces** requiere la presencia declarada del logotipo ARASAAC.
