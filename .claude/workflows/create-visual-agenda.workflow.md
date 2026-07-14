<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: 51b5ebf7efcf -->
---
name: create-visual-agenda
kind: business
title: Crear agenda visual accesible
description: >-
  Agenda visual con pictogramas ARASAAC reales, intake guiado, validación
  CAA/SAAC, revisión humana y exportación con manifest.
uses_agents: [spec, build, verify, docs]
uses_skills: [material-pipeline, arasaac-fetch, human-review-gate, export-with-manifest, compliance-scan, a11y-audit]
---

# Workflow: create-visual-agenda

Especialización del workflow canónico [`spec-build-verify`](spec-build-verify.workflow.md) para producir agendas visuales accesibles.

## Cuándo usarlo
- Un/a coordinador/a o profesional necesita generar una agenda visual (día, semana, actividad concreta).
- Contexto CEE, aula, fundación, familia.

## Pasos

### 1. Intake guiado (agente `spec` / `build`)
Recoger:
- **Título** (sin PII, ver gate `privacy`).
- **Propósito**: rutina diaria, salida, actividad puntual.
- **Duración**: día completo, mañana, actividad.
- **Nº pasos**: recomendado 4–8 pictos.
- **Audiencia**: edad, perfil comunicativo.
- **Locale**: `es`, `en`, …

### 2. Selección de pictogramas (skill `material-pipeline` → `arasaac-fetch`)
- Buscar por keyword.
- **Nunca** generar con IA.
- Verificar IDs reales (skill `compliance-scan`).

### 3. Edición
- Ordenar pasos (drag & drop en UI).
- Etiquetas cortas (lenguaje llano).
- Layout: horizontal (mañana/tarde) o vertical (lista).

### 4. Validación automática (skill `compliance-scan`)
- License, privacy, IDs, densidad visual (4–8/página), lenguaje.
- Si FAIL: volver a paso 3.

### 5. Auditoría a11y (skill `a11y-audit`)
- Contraste ≥ AA.
- Iconos con texto asociado.
- Navegable por teclado si es HTML interactivo.

### 6. Revisión humana (skill `human-review-gate`)
- Estado → `in_review`.
- Reviewer (profesional o coordinador) aprueba o rechaza con motivo.
- **Obligatorio** antes de exportar (regla absoluta #5).

### 7. Exportación (skill `export-with-manifest`)
- Formatos recomendados: PDF (impresión), HTML (proyección), ZIP (paquete completo).
- Manifest de atribución adjunto.
- Créditos visibles.

## Salida esperada

- Archivo exportado con atribución ARASAAC visible.
- Manifest JSON completo.
- Audit log con reviewer + timestamp + versión.

## Gates aplicados

- `license` (arasaac-fetch + export-with-manifest)
- `privacy` (intake + compliance-scan)
- `human_review` (obligatorio antes de export)

## Errores comunes

- ❌ Vincular la agenda a "la agenda de Pedro" (PII) → violar gate `privacy`.
- ❌ Exportar sin revisión humana → violar regla absoluta #5.
- ❌ Densidad > 12 pictos/página → carga cognitiva excesiva.

## Ver también

- Workflow canónico: [`spec-build-verify`](spec-build-verify.workflow.md)
- Personas: `caasaac-methodology`, `a11y-cognitive`, `easy-reading`, `product-owner-social`
