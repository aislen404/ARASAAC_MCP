<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: d052cc0ab578 -->
---
name: docs-generate
description: >-
  Generar README, manuales técnicos, deployment, contribution, release notes,
  dossier ARASAAC y manuales de entidad. Reemplaza las 7 skills docs-generate-*.
inputs:
  - doc_type        # readme | technical | deployment | contribution | release-notes | arasaac-dossier | entity-manual
  - scope           # ruta o change_id que motiva el doc
outputs:
  - Archivo Markdown creado o actualizado en la ubicación estándar
invoked_by_agents: [docs, release]
gates: []
---

# Skill: docs-generate

## Cuándo usarla
- Fase `docs` de una change con impacto documental.
- Fase `release` para release notes y changelog.
- Preparación de dossier ARASAAC o manual para entidad.

## Procedimiento paso a paso

1. **Detectar tipo** (`doc_type`) y ubicación:
   | doc_type | Ubicación |
   |---|---|
   | `readme` | `README.md` |
   | `technical` | `docs/architecture/<tema>.md` |
   | `deployment` | `docs/deployment/<target>.md` |
   | `contribution` | `docs/contributing.md` o `CONTRIBUTING.md` |
   | `release-notes` | `docs/releases/YYYY-MM-DD-<version>.md` |
   | `arasaac-dossier` | `docs/compliance/arasaac-validation-dossier.md` |
   | `entity-manual` | `docs/manuals/<entity-type>.md` |
2. **Cargar plantilla** correspondiente (si existe en `docs/templates/`). Si no, usa la estructura estándar:
   - Título H1
   - Resumen (2–3 líneas)
   - Índice si > 5 secciones
   - Contenido con H2/H3
   - "Ver también" al final con enlaces relativos
3. **Rellenar contenido** basado en:
   - `git diff` de la change para detectar novedades.
   - `openspec/changes/<id>/proposal.md` para el "por qué".
   - `openspec/changes/<id>/design.md` para el "cómo".
   - `spec.md` para "qué garantiza".
4. **Aplicar reglas de estilo**:
   - Frases cortas.
   - Bloques de código con lenguaje declarado.
   - Imágenes con alt text.
   - Enlaces relativos dentro del repo.
5. **Verificar**:
   - Sin enlaces rotos.
   - Sin secciones vacías (`TODO` explícito si es intencional).
   - Sección de créditos ARASAAC si el doc menciona pictogramas.
6. **Referenciar** desde índices apropiados:
   - `docs/obsidian/ARASAAC_Project-Index.md` para docs generales.
   - `README.md` para docs de usuario final.

## Estructura estándar por tipo

### `readme` (raíz o subpaquete)
```md
# <Nombre>
> Descripción en 1 línea.

## Qué es
## Cómo arrancar
## Uso
## Contribuir
## Licencia
```

### `technical`
```md
# <Tema>
## Contexto
## Decisiones
## Diagrama (opcional)
## Contratos
## Riesgos
## Referencias
```

### `release-notes`
```md
# <version> — YYYY-MM-DD
## Novedades
## Cambios técnicos
## Compliance (gates verificados)
## Contribuidores
```

## Errores comunes

- ❌ Copiar `proposal.md` tal cual como release notes.
- ❌ Documentar features que no existen (aspiracional).
- ❌ Enlaces absolutos a `github.com/…` cuando bastan relativos.
- ❌ Olvidar atribución ARASAAC en docs de export/materiales.
- ❌ README obsoleto: cada release debería re-verificarlo.

## Ver también

- Personas: `documentation`, `easy-reading`, `ux-accessibility`, `arasaac-liaison`
- Índice: `docs/obsidian/ARASAAC_Project-Index.md`
