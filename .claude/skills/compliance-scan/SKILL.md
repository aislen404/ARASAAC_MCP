<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: 0141bd61fa1e -->
---
name: compliance-scan
description: >-
  Scan único que agrupa license + privacy + pictogram-ids + visual-density +
  plain-language + non-commercial-context. Reemplaza las 10 skills validate-*.
inputs:
  - target        # material_id | change_id | file_path
  - scope         # material | change | codebase
outputs:
  - Report con secciones: license, privacy, pictograms, density, language, context
  - PASS / WARN / FAIL por sección
invoked_by_agents: [spec, verify]
gates: [license, privacy]
---

# Skill: compliance-scan

## Cuándo usarla
- Antes de aprobar cambio en `spec` (evaluar riesgos de compliance).
- En cada `verify` antes del dictamen.
- Como pre-check antes de solicitar `human-review-gate`.

## Procedimiento paso a paso

Ejecuta cada check en orden. Cualquier FAIL en gate crítico → **detener** y reportar.

### 1. License (gate `license`)
- Todos los pictogramas usados tienen metadata completa (autor, owner, licencia, URL, fecha).
- Ninguna imagen del material es generada por IA (regla absoluta #1).
- Ningún pictograma modificado (regla absoluta #3).
- Atribución presente en export (chequear plantilla).
- **FAIL** si alguna falla → bloquea todo.

### 2. Privacy (gate `privacy`)
- Sin PII en título, descripción, tags o contenido:
  - Sin nombres completos de personas concretas.
  - Sin DNI, teléfono, email, dirección.
  - Sin fotos identificables (metadata EXIF limpia).
  - Sin fecha de nacimiento.
- Sin vinculación material↔persona concreta (MVP: regla absoluta #6).
- **FAIL** si alguna falla → bloquea.

### 3. Pictogram IDs reales
- Cada `pictogram_id` referenciado existe en la API ARASAAC (validar contra cache/API).
- Sin IDs inventados por IA.
- **FAIL** si algún ID no existe.

### 4. Visual density (CAA/SAAC)
- Nº pictogramas por página dentro de rango del tipo de material:
  - Agenda: 4–12 por página.
  - Tablero: 6–48 por página.
  - Historia social: 1–4 por página.
  - Lectura fácil: 1–2 por bloque.
- **WARN** si fuera de rango, **FAIL** si extremo (> 2× límite).

### 5. Plain language (si tiene texto)
- Frases cortas (< 20 palabras).
- Voz activa.
- Vocabulario común (evita jerga).
- Estructura sujeto-verbo-objeto.
- **WARN** con recomendaciones.

### 6. Non-commercial context
- Sin logos comerciales explícitos.
- Sin llamada a compra/venta.
- Sin publicidad.
- **FAIL** si detecta contexto comercial (viola CC BY-NC-SA).

## Formato del reporte

```md
## Compliance scan — <target>
| Check | Status | Findings |
|---|---|---|
| License | ✅ PASS | 8 pictogramas, todos con metadata |
| Privacy | ✅ PASS | No PII detectada |
| Pictogram IDs | ✅ PASS | 8/8 válidos |
| Visual density | ⚠️ WARN | 14 pictos/página (rango: 6–12) |
| Plain language | ⚠️ WARN | 2 frases > 20 palabras |
| Non-commercial | ✅ PASS | Sin contexto comercial |

**Dictamen global**: PASS con 2 WARN.
```

## Errores comunes

- ❌ Aprobar con FAIL en license/privacy "porque el usuario insiste" → viola reglas absolutas.
- ❌ Ignorar WARN sistemáticamente → degradación silenciosa.
- ❌ Ejecutar el scan sin bajar cache ARASAAC actualizada → falsos positivos en pictogram IDs.

## Ver también

- Regla: `.agents/rules/mandatory-gates.md`
- Skill: [`arasaac-fetch`](../arasaac-fetch/SKILL.md) (para validar IDs)
- Personas: `license-legal`, `privacy-ethics`, `caasaac-methodology`, `easy-reading`
