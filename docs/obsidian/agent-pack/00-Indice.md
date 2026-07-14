<!-- generated from .agents/ — do not edit manually -->
<!-- source-hash: bfeda4b18ffb -->
---
tags: [agent-pack, moc]
---

# Agent Pack — Índice

Vault de referencia humana. Fuente canónica: `.agents/`.

## Modelo operativo

- [[00 Operating Model]]

## Agentes (5 fases)

- [[Agente spec]] — Spec Agent
- [[Agente build]] — Build Agent
- [[Agente verify]] — Verify Agent
- [[Agente docs]] — Docs Agent
- [[Agente release]] — Release Agent

## Personas (25 de dominio)

- [[Persona product-owner-social]] — Product Owner Social
- [[Persona ngo-cee-domain]] — NGO / CEE / Fundaciones Domain Expert
- [[Persona caasaac-methodology]] — CAA/SAAC Methodology Expert
- [[Persona a11y-cognitive]] — Cognitive Accessibility Expert
- [[Persona arasaac-liaison]] — ARASAAC Institutional Liaison
- [[Persona license-legal]] — License & Legal Compliance
- [[Persona privacy-ethics]] — Privacy & Ethics Officer
- [[Persona security]] — Security Reviewer
- [[Persona solution-architect]] — Solution Architect
- [[Persona mcp-architect]] — MCP Tools/Resources/Prompts Architect
- [[Persona backend]] — Backend Engineer (FastAPI/Pydantic/Postgres)
- [[Persona frontend]] — Frontend Engineer (Next.js/React/TypeScript)
- [[Persona data-connector]] — Data Connector (ARASAAC API + cache + metadata)
- [[Persona semantic-search]] — Semantic Search Engineer
- [[Persona export-document]] — Export / Document Engineer (HTML/PDF/DOCX/PPTX/ZIP)
- [[Persona devops]] — DevOps (Docker Compose, CI, deploy)
- [[Persona qa]] — Functional QA
- [[Persona accessibility-qa]] — Accessibility QA (WCAG 2.2 AA + cognitive)
- [[Persona test-automation]] — Test Automation (unit + contract + E2E)
- [[Persona observability]] — Observability (events, metrics, audit logs)
- [[Persona documentation]] — Documentation Writer
- [[Persona easy-reading]] — Easy Reading / Plain Language Editor
- [[Persona ux-accessibility]] — UX Accessibility Designer
- [[Persona openspec-steward]] — OpenSpec Steward
- [[Persona release-manager]] — Release Manager

## Skills (10)

- [[Skill openspec-lifecycle]] — Crear, validar y evolucionar una change OpenSpec (proposal, design, tasks, spec).
- [[Skill openspec-archive]] — Cerrar tasks.md, mover a openspec/changes/archive/, actualizar índices y release notes.
- [[Skill arasaac-fetch]] — Consultar API de ARASAAC, normalizar metadata, cachear y generar entrada de manifest.
- [[Skill mcp-tool-scaffold]] — Definir schema MCP estricto, implementar tool con seguridad, escribir contract test y validación.
- [[Skill material-pipeline]] — Pipeline unificado de materiales: intake → search pictograms → edit → validate → human-review → export. Absorbe todas las skills create-* y editor-*.
- [[Skill export-with-manifest]] — Generar HTML/PDF/DOCX/PPTX/ZIP con atribución visible y manifest ARASAAC completo.
- [[Skill human-review-gate]] — Solicitar, aprobar o rechazar revisión humana de un material con trazabilidad.
- [[Skill compliance-scan]] — Scan único que agrupa license + privacy + pictogram-ids + visual-density + plain-language + non-commercial-context. Reemplaza las 10 skills validate-*.
- [[Skill a11y-audit]] — Auditoría WCAG 2.2 AA + keyboard + focus + color-independence + labels + cognitive.
- [[Skill docs-generate]] — Generar README, manuales técnicos, deployment, contribution, release notes, dossier ARASAAC y manuales de entidad. Reemplaza las 7 skills docs-generate-*.

## Workflows (4)

- [[Workflow spec-build-verify]] — OpenSpec Lifecycle (canonical)
- [[Workflow create-visual-agenda]] — Crear agenda visual accesible
- [[Workflow create-communication-board]] — Crear tablero de comunicación
- [[Workflow create-easy-reading]] — Crear documento en lectura fácil

## Prompts (4)

- [[Prompt new-spec]] — `/new-spec`
- [[Prompt implement-task]] — `/implement-task`
- [[Prompt verify-change]] — `/verify-change`
- [[Prompt archive-change]] — `/archive-change`

## Reglas

- [[Regla platform]]
- [[Regla mandatory-gates]]
- [[Regla backend]]
- [[Regla frontend]]
- [[Regla mcp]]
- [[Regla export-license]]
