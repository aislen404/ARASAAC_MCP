# Roadmap, Backlog, DoD y Matriz de Riesgos

## MVP mínimo validable

### Objetivo

Validar que una entidad puede generar, revisar y exportar materiales básicos usando pictogramas ARASAAC reales, sin datos personales y con atribución visible.

### Features obligatorias

1. Búsqueda de pictogramas.
2. Generación de agenda visual.
3. Generación de tablero de comunicación.
4. Vista previa editable.
5. Revisión humana.
6. Export HTML/PDF.
7. Atribución visible.
8. Auditoría mínima.
9. Web App AA base.
10. Docker Compose.

## Backlog priorizado

### P0 — Foundation

- Repo skeleton.
- OpenSpec base.
- AGENTS.md.
- CI básico.
- Modelo licencia.
- Modelo material.

### P1 — Core ARASAAC + MCP

- Connector API ARASAAC.
- Normalización metadatos.
- Tools MCP search/get/suggest.
- Resources license/templates.
- Prompts base.

### P2 — Materiales MVP

- Agenda visual.
- Tablero comunicación.
- Editor preview.
- Export HTML/PDF.
- Review workflow.

### P3 — Producto piloto

- Lectura fácil.
- Historia social.
- Señalética.
- DOCX/PPTX/ZIP.
- Preferencias sin PII.
- Observabilidad avanzada.

### P4 — Escalado

- Keycloak.
- Multi-entidad.
- Búsqueda semántica.
- Dossier ARASAAC.
- Publicación open source/paquete instalable.

## Criterios de aceptación MVP

- Un profesional crea una agenda visual en menos de 5 minutos.
- La agenda usa pictogramas reales recuperados por herramienta.
- El usuario puede cambiar pictogramas sugeridos.
- El material no puede exportarse sin revisión humana.
- El PDF incluye atribución visible.
- El sistema conserva trazabilidad por pictograma.
- El frontend pasa checks básicos WCAG AA automatizados y revisión manual.
- No se almacena identidad de beneficiario.

## Matriz de riesgos detallada

| Riesgo | Prob. | Impacto | Nivel | Mitigación | Owner |
|---|---:|---:|---:|---|---|
| Licencia BY-NC-SA mal aplicada | Media | Alta | Crítico | License Compliance Agent + bloqueo export | Compliance |
| Uso comercial accidental | Baja | Alta | Alto | modo non-commercial hardcoded en MVP | Product |
| Falta de bendición ARASAAC | Media | Alta | Alto | dossier antes de piloto público | Dirección |
| Material confuso | Media | Alta | Alto | revisión humana + Accessibility QA | Dominio |
| Datos de menores | Media | Alta | Alto | no PII + perfiles no identificables | Security |
| Prompt injection contra MCP | Media | Alta | Alto | allowlist + schemas + no shell | Security |
| Baja calidad de matching | Alta | Media | Alto | edición manual + métricas + semántica futura | Data |
| Export PDF inconsistente | Media | Media | Medio | snapshots visuales + tests | Export |
| Accesibilidad insuficiente | Media | Alta | Alto | WCAG gates | Frontend |
| Complejidad excesiva | Alta | Media | Alto | MVP P0/P1/P2 estricto | Product |
