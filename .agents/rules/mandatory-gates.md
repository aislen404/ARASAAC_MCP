# Mandatory Gates — Fuente única de verdad

<!-- source of truth for the 3 critical gates: license, privacy, human_review -->

Estos son los **3 gates críticos** que se aplican en toda la plataforma ARASAAC Social MCP. Cualquier agente, skill o workflow que declare `gates` en su frontmatter YAML debe referenciarlos por nombre (`license`, `privacy`, `human_review`) y NO duplicar su texto.

Este archivo es **la única fuente**. Si un gate cambia, se cambia aquí y `sync_agent_packs.py` regenera todos los packs IDE. Cualquier drift lo detecta `verify_agent_packs_sync.py`.

---

## Gate 1 — `license`

**Propósito**: garantizar que todo uso de material ARASAAC respeta la licencia **CC BY-NC-SA 4.0** con atribución completa a Sergio Palao / Gobierno de Aragón.

### Criterios verificables

1. **Atribución visible** en toda exportación (HTML, PDF, DOCX, PPTX, ZIP):
   - Autor: `Sergio Palao`
   - Origen: `ARASAAC (http://arasaac.org)`
   - Propietario: `Gobierno de Aragón`
   - Licencia: `CC BY-NC-SA 4.0`
2. **Uso exclusivamente no comercial**: el material generado NO puede incluirse en productos, servicios o campañas con ánimo de lucro.
3. **ShareAlike**: cualquier derivado se distribuye bajo la misma licencia.
4. **No modificación de pictogramas**: los SVG/PNG originales de ARASAAC no pueden alterarse (color, forma, composición). Se permite recomposición del layout, nunca del pictograma en sí.
5. **No pictogramas generados por IA**: prohibido crear pictogramas con generadores de imagen o imitar el estilo ARASAAC con IA.
6. **Manifest completo** por material exportado con: `id ARASAAC`, `label`, `url`, `autor`, `propietario`, `licencia`, `fecha_recuperacion`, `material_id`.

### Cómo verificarlo

- Skill: `compliance-scan` (verifica presencia de atribución y ausencia de modificación).
- Persona: `license-legal`.
- Bloqueo: si falla, `verify` NO aprueba exportación.

### Referencias

- `NOTICE-ARASAAC.md` (raíz del repo)
- `docs/compliance/arasaac-license-policy.md`
- `AGENTS.md` §2 (reglas absolutas #1–#5)

---

## Gate 2 — `privacy`

**Propósito**: evitar cualquier introducción de datos personales sensibles y garantizar que el sistema no vincule materiales a personas concretas (en el MVP).

### Criterios verificables

1. **No PII en materiales**: prohibido incluir nombres reales, DNI, direcciones, teléfonos, fotos, historiales médicos, diagnósticos o cualquier identificador de persona física.
2. **No vinculación persona↔material**: los materiales generados NO deben asociarse a un usuario final concreto (paciente, alumno, etc.) en el MVP. Uso genérico y reutilizable.
3. **No uso diagnóstico**: el sistema no se usa para diagnóstico médico, psicológico, educativo o clínico. Materiales son apoyos, no herramientas de diagnóstico.
4. **No datos personales en logs**: los audit logs registran acciones y IDs opacos, nunca contenido personal.
5. **Cumplimiento RGPD/LOPDGDD** en cualquier flujo que persista datos.

### Cómo verificarlo

- Skill: `compliance-scan` (busca patrones PII: NIF/NIE, emails, teléfonos, nombres propios en campos de texto).
- Persona: `privacy-ethics`.
- Bloqueo: si falla, `verify` NO aprueba el material.

### Referencias

- `AGENTS.md` §2 (reglas absolutas #6–#8)
- `docs/architecture/mcp-dual-surface.md`

---

## Gate 3 — `human_review`

**Propósito**: ningún material se exporta sin aprobación explícita de un humano con criterio profesional (educador, terapeuta, técnico).

### Criterios verificables

1. **Estado `approved`** registrado explícitamente antes de exportar. Aprobación implícita o automática está prohibida.
2. **Trazabilidad de aprobación**: quién aprueba (o rol), cuándo, qué versión del material.
3. **Rechazo con motivo**: si un revisor rechaza, debe registrar el motivo estructurado.
4. **Re-revisión al modificar**: cualquier cambio tras aprobación invalida el estado y requiere nueva revisión.
5. **UI visible**: el flujo guiado debe mostrar claramente el paso de revisión humana y bloquear exportación mientras no exista aprobación.

### Cómo verificarlo

- Skill: `human-review-gate` (implementa el flujo de solicitud/aprobación/rechazo).
- Persona: `qa` + `product-owner-social`.
- Bloqueo: si falla, `verify` NO permite pasar a `release`.

### Referencias

- `AGENTS.md` §2 (regla absoluta #5)
- `docs/architecture/material-validation.md`

---

## Cómo referenciar estos gates

En cualquier archivo con frontmatter YAML (`*.agent.md`, `*.persona.md`, `SKILL.md`, `*.workflow.md`), declara:

```yaml
mandatory_gates: [license, privacy, human_review]
```

o solo los aplicables:

```yaml
gates: [license]
```

**Nunca copies el texto de los criterios.** Si necesitas contexto local, enlaza a `.agents/rules/mandatory-gates.md#gate-1--license` (o el ancla correspondiente).

## Invariantes

- Este archivo es el único con el texto completo de los criterios.
- `verify_agent_packs_sync.py` verifica que existe y que al menos 1 agente-fase y 1 skill lo referencian por nombre.
- El sync copia este archivo tal cual a cada pack IDE (`.cursor/rules/mandatory-gates.mdc`, `.github/instructions/mandatory-gates.instructions.md`, etc.).
