<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: 12a439642a54 -->
---
name: openspec-lifecycle
description: Crear, validar y evolucionar una change OpenSpec (proposal, design, tasks, spec).
inputs:
  - change_id     # e.g. "0037"
  - short_title   # kebab-case
  - problem      # 1-3 sentences describing the need
outputs:
  - openspec/changes/<id>-<slug>/proposal.md
  - openspec/changes/<id>-<slug>/design.md
  - openspec/changes/<id>-<slug>/tasks.md
  - openspec/changes/<id>-<slug>/spec.md
invoked_by_agents: [spec, build]
gates: []
---

# Skill: openspec-lifecycle

## Cuándo usarla
- Estás creando una nueva change OpenSpec desde cero.
- Necesitas evolucionar (añadir tasks, refinar spec) una change existente.
- Vas a implementar y quieres releer el contrato antes de tocar código.

## Procedimiento paso a paso

1. **Elegir carpeta**: `openspec/changes/<change_id>-<short_title>/`. Si existe, valida antes de sobreescribir.
2. **Redactar `proposal.md`** con secciones fijas:
   - Contexto / Problema
   - Cambio propuesto (bullets accionables)
   - Fuera de alcance (explícito)
   - Valor para la comunidad
   - Referencias (issues, docs, otras changes)
3. **Redactar `design.md`** con:
   - Arquitectura (diagramas o texto)
   - Contratos (esquemas, endpoints, tipos)
   - Alternativas descartadas y por qué
   - Riesgos y mitigaciones (referencia `mandatory-gates.md`)
   - ADRs si aplica
4. **Redactar `spec.md`** con:
   - `MUST` / `SHOULD` / `MUST NOT` numerados
   - ≥ 3 escenarios verificables (Given / When / Then)
   - Referencia a gates críticos por nombre (no duplicar texto)
5. **Redactar `tasks.md`** con:
   - Fases A–H (o menos si es pequeña)
   - Tareas atómicas `- [ ] **X1.** …`
   - Dependencias explícitas si las hay
6. **Auto-revisar**: leer los 4 archivos como si fueras nuevo en el proyecto. Si algo no está claro, refinar.

## Ejemplo mínimo

```
openspec/changes/0037-guided-onboarding/
├── proposal.md     # "Los coordinadores de CEE no encuentran por dónde empezar…"
├── design.md       # "Tour de 4 pasos anclado a componentes existentes…"
├── spec.md         # "MUST: tour skippable · Scenario: usuario nuevo…"
└── tasks.md        # "A1. Añadir componente Tour · B1. Cablear en Dashboard…"
```

## Errores comunes

- ❌ `spec.md` con "debe ser rápido": no verificable → usa métrica.
- ❌ `tasks.md` con "Implementar feature X": no atómica → parte en 5.
- ❌ Duplicar la propuesta en el diseño → referencia, no copies.
- ❌ Omitir "Fuera de alcance": abre puerta a scope creep.

## Ver también

- Ejemplos reales: `openspec/changes/0035-honest-workspace-metrics-v2/`
- Guía OpenSpec: `openspec/project.md`
- Gates: `.agents/rules/mandatory-gates.md`
