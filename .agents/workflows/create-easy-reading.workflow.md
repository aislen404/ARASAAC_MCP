---
name: create-easy-reading
kind: business
title: Crear documento en lectura fácil
description: >-
  Adaptar documento a lectura fácil con apoyo pictográfico ARASAAC. Requiere
  revisión humana profesional y verifica plain-language.
uses_agents: [spec, build, verify, docs]
uses_skills: [material-pipeline, arasaac-fetch, human-review-gate, export-with-manifest, compliance-scan, a11y-audit]
---

# Workflow: create-easy-reading

Especialización del workflow canónico [`spec-build-verify`](spec-build-verify.workflow.md) para adaptar documentos a **lectura fácil** con apoyo pictográfico ARASAAC.

## Cuándo usarlo
- ONG, fundación o administración necesita adaptar un documento (folleto, guía, formulario).
- El usuario final tiene dificultad lectora (discapacidad cognitiva, aprendizaje L2, etc.).

## Pasos

### 1. Intake
- **Documento origen**: texto o PDF/DOCX (sin PII: gate `privacy`).
- **Público diana**: personas con discapacidad intelectual, migrantes, mayores, etc.
- **Objetivo**: informar, orientar, formar, gestionar trámite.
- **Extensión estimada**: bloques cortos, párrafos.

### 2. Adaptación textual
Consulta persona `easy-reading`:
- Frases < 15 palabras.
- Una idea por frase.
- Voz activa.
- Vocabulario común (glosario de términos difíciles).
- Estructura sujeto-verbo-objeto.
- Ejemplos concretos.

### 3. Selección de pictogramas de apoyo (`arasaac-fetch`)
- 1–2 pictogramas por bloque temático.
- Junto al concepto clave (no decorativos).
- Skill `compliance-scan` verifica IDs reales.

### 4. Composición
- Formato con márgenes generosos.
- Tipografía sans-serif ≥ 14pt.
- Interlineado ≥ 1.5.
- Contraste AA.

### 5. Validación (`compliance-scan`)
- Plain language (WARN por frases > 20 palabras).
- License + privacy + non-commercial.

### 6. A11y (`a11y-audit`)
- Contraste AA.
- Estructura semántica (títulos jerárquicos, listas).
- Alt text en pictogramas.

### 7. Revisión humana (`human-review-gate`)
- **Doble**: profesional adaptador + validador de lectura fácil.
- Idealmente: validación con usuario final.

### 8. Exportación (`export-with-manifest`)
- PDF etiquetado (para lectores de pantalla).
- HTML accesible.
- DOCX si el destinatario necesita editarlo.
- Créditos ARASAAC + logotipo de lectura fácil si aplica.

## Salida esperada

- Documento adaptado, validado y exportado.
- Manifest ARASAAC completo.
- Registro de doble revisión.

## Gates aplicados

- `license`, `privacy`, `human_review` (con separación adaptador ≠ validador).

## Errores comunes

- ❌ Traducción literal sin simplificación real.
- ❌ Añadir pictogramas decorativos que distraen.
- ❌ Publicar sin validación con persona del colectivo diana.
- ❌ Tipografía < 14pt o interlineado insuficiente.

## Ver también

- Workflow canónico: [`spec-build-verify`](spec-build-verify.workflow.md)
- Personas: `easy-reading`, `a11y-cognitive`, `ux-accessibility`, `ngo-cee-domain`
