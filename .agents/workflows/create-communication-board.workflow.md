---
name: create-communication-board
kind: business
title: Crear tablero de comunicación
description: >-
  Tablero de comunicación con categorías, pictogramas reales y balance
  CAA/SAAC. Revisión humana obligatoria antes de exportar.
uses_agents: [spec, build, verify, docs]
uses_skills: [material-pipeline, arasaac-fetch, human-review-gate, export-with-manifest, compliance-scan, a11y-audit]
---

# Workflow: create-communication-board

Especialización del workflow canónico [`spec-build-verify`](spec-build-verify.workflow.md) para tableros de comunicación aumentativa/alternativa (CAA/SAAC).

## Cuándo usarlo
- Profesional CAA necesita un tablero temático (comer, jugar, emociones, escuela…).
- Familia solicita tablero de rutina o contextual.

## Pasos

### 1. Intake guiado
- **Título** (temático, sin PII).
- **Categoría principal** (necesidades básicas, sociales, académicas…).
- **Nº casillas**: recomendado 6–48 (según usuario final).
- **Cuadrícula**: 2×3, 3×4, 4×6, 6×8.
- **Colores por categoría** (opcional, sistema Fitzgerald o similar).

### 2. Selección de pictogramas
- Balance CAA/SAAC: verbos, sustantivos, adjetivos, preguntas, sociales.
- Consultar persona `caasaac-methodology` para balance apropiado.
- Skill `arasaac-fetch` por categoría.

### 3. Edición
- Asignar pictogramas a casillas.
- Etiquetas cortas y claras.
- Aplicar color por categoría gramatical si se usa Fitzgerald.

### 4. Validación (`compliance-scan`)
- License, privacy, IDs, densidad (6–48 según cuadrícula).

### 5. A11y (`a11y-audit`)
- Contraste AA (crítico si se imprimirá en color/BN).
- Independencia del color: si usas Fitzgerald, cada categoría también tiene texto/icono distinguible.

### 6. Revisión humana (`human-review-gate`)
- Obligatoria.
- Reviewer con conocimiento CAA/SAAC preferente.

### 7. Exportación (`export-with-manifest`)
- PDF alta resolución para impresión.
- Opcional: PNG por casilla para uso digital.
- Créditos ARASAAC visibles.

## Salida esperada

- Tablero exportado con atribución.
- Manifest JSON.
- Audit log completo.

## Gates aplicados

- `license`, `privacy`, `human_review`.

## Errores comunes

- ❌ Solo sustantivos en el tablero → limita comunicación real.
- ❌ Casillas demasiado pequeñas para usuarios con dificultad motora.
- ❌ Usar solo color para distinguir categorías → falla color-independence.

## Ver también

- Workflow canónico: [`spec-build-verify`](spec-build-verify.workflow.md)
- Personas: `caasaac-methodology`, `a11y-cognitive`, `ux-accessibility`, `arasaac-liaison`
