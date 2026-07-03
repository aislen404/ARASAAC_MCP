from pathlib import Path
import textwrap, json, zipfile, os, datetime
base = Path('/mnt/data/arasaac_mcp_master_plan')

sources = """# Fuentes verificadas y marco de referencia

Fecha de consolidación: 2026-07-03

## ARASAAC

- ARASAAC Terms of use: https://arasaac.org/terms-of-use
  - Los símbolos pictográficos son propiedad del Gobierno de Aragón.
  - Han sido creados por Sergio Palao para ARASAAC.
  - Se distribuyen bajo Creative Commons BY-NC-SA.
  - ARASAAC facilita textos oficiales de atribución.
- ARASAAC Developers API: https://arasaac.org/developers/api
  - Existen endpoints/recursos para uso por desarrolladores, incluyendo listas de palabras o frases para búsqueda/autocompletado y búsqueda de pictogramas.
- ARASAAC pictograms search: https://arasaac.org/pictograms/search
- Aula Abierta ARASAAC / señalización: https://aulaabierta.arasaac.org/en/signage-of-public-spaces-and-services-with-arasaac-pictograms

## MCP

- Model Context Protocol Specification 2025-06-18: https://modelcontextprotocol.io/specification/2025-06-18
  - El servidor puede exponer Tools, Resources y Prompts.
  - Tools son funciones que el modelo puede invocar para interactuar con sistemas externos.
  - Resources son contexto y datos para el usuario o modelo.
  - Prompts son plantillas de mensajes o workflows.
- MCP Tools: https://modelcontextprotocol.io/specification/2025-06-18/server/tools

## OpenSpec

- Fission-AI OpenSpec Getting Started: https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md
  - Flujo base: propose -> apply -> sync -> archive.
  - Flujo expandido: new -> ff/continue -> apply -> verify -> archive.
- Fission-AI OpenSpec Concepts: https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md
  - Una change folder agrupa proposal, design, tasks y specs.

## Accesibilidad web

- W3C WCAG 2.2 Recommendation: https://www.w3.org/TR/WCAG22/
- W3C WCAG Overview: https://www.w3.org/WAI/standards-guidelines/wcag/
  - WCAG se organiza bajo principios perceptible, operable, comprensible y robusto.
  - Los criterios de éxito se agrupan en niveles A, AA y AAA.
"""

plan = """# Plan Maestro — MCP ARASAAC para generación de materiales accesibles

**Nombre de trabajo:** ARASAAC Social MCP Platform  
**Versión:** 1.0 para análisis, OpenSpec y ejecución en Codex  
**Fecha:** 2026-07-03  
**Destino prioritario:** fundaciones, organizaciones sociales, CONACEE, CERMI, Centros Especiales de Empleo, centros ocupacionales, entidades de atención, educación especial y administraciones públicas.  
**Naturaleza:** proyecto social-first, no comercial en su primera etapa, gobernado, trazable, con revisión humana obligatoria y uso exclusivo de pictogramas ARASAAC.

---

## 0. Decisiones consolidadas del cuestionario

### 0.1 Producto que vamos a construir

Construiremos una solución completa, no solo un conector:

1. **Servidor MCP ARASAAC** para que agentes y clientes compatibles puedan buscar, recuperar y componer materiales con pictogramas reales.
2. **Web App accesible AA** para entidades sociales, en formato similar a Open WebUI: interfaz sencilla, guiada, conversacional y con formularios.
3. **Motor de generación de materiales accesibles**: agendas visuales, tableros, historias sociales, señalética, lectura fácil, secuencias y documentos exportables.
4. **Sistema de gobierno**: licencia, atribución, auditoría, trazabilidad, revisión humana, seguridad y control de calidad.
5. **Ecosistema OpenSpec + Codex + agentes/skills** para desarrollar el proyecto mediante workflows agénticos.

### 0.2 Principios irrenunciables

- Solo pictogramas ARASAAC. No generación de pictogramas con IA.
- No se modifica el pictograma original.
- Atribución visible en cada documento y trazabilidad completa interna.
- Revisión humana siempre antes de entrega/exportación final.
- MVP sin datos personales vinculados a personas concretas.
- Puede haber materiales para menores, pero sin asociarlos a identidad personal.
- Web App accesible con objetivo WCAG 2.2 AA.
- Primera fase: validar un MVP no comercial, social y técnicamente robusto.
- Fases posteriores: multi-entidad simple y después multi-tenant.
- Despliegue inicial: Docker Compose.
- Backend principal: Python.
- Frontend: Next.js/React.
- Auth inicial: sin autenticación en PoC; después Keycloak.
- Vector DB: open source y escalable; recomendación: Qdrant o PostgreSQL + pgvector. Para esta arquitectura se propone **PostgreSQL + pgvector** para simplificar operación y mantener una única base transaccional/vectorial en MVP escalable.

### 0.3 Hipótesis de licencia

Los pictogramas ARASAAC se utilizarán bajo un modelo **no comercial, social, educativo y de apoyo a entidades**, respetando CC BY-NC-SA. La plataforma debe estar preparada para solicitar y documentar bendición/autorización de ARASAAC antes de cualquier despliegue público relevante o evolución comercial.

---

## 1. Tesis ejecutiva

El proyecto es viable si se formula correctamente:

> No vamos a crear un “generador de pictogramas”. Vamos a crear una **plataforma de generación asistida de materiales accesibles** que utiliza pictogramas reales de ARASAAC de forma trazable, atribuida, gobernada y revisada por personas.

La plataforma debe ayudar a profesionales y entidades a producir materiales que hoy requieren tiempo, criterio, herramientas dispersas y conocimiento técnico. El objetivo no es sustituir a logopedas, terapeutas, profesionales de apoyo o especialistas en CAA/SAAC, sino acelerar su trabajo y ofrecer una base común, segura y reutilizable.

---

## 2. Alcance funcional maestro

### 2.1 Capacidades de generación

El sistema deberá generar:

1. Agendas visuales.
2. Secuencias paso a paso.
3. Tableros de comunicación.
4. Historias sociales.
5. Documentos de lectura fácil con pictogramas.
6. Señalética cognitiva.
7. Kits completos por entidad, área, contexto o proceso.

### 2.2 Contextos elegibles

El usuario podrá elegir contexto:

- Salud.
- Educación.
- Empleo protegido / Centros Especiales de Empleo.
- Autonomía personal.
- Atención ciudadana.
- Transporte y movilidad.
- Vida diaria en centros.
- Protocolos internos.
- Sensibilización y derechos.
- Prevención de riesgos laborales.
- Comunicación institucional accesible.

### 2.3 Prioridad CONACEE / CEE

Para CONACEE y Centros Especiales de Empleo se priorizará:

1. Incorporación laboral accesible.
2. Prevención de riesgos laborales con pictogramas.
3. Instrucciones de tareas productivas.
4. Protocolos internos: horarios, comedor, descansos, uniforme, fichaje, EPIs.
5. Comunicación entre persona trabajadora y unidad de apoyo.
6. Materiales de acogida y onboarding.
7. Señalética de espacios de trabajo.

### 2.4 Prioridad CERMI / entidades representativas

Para CERMI y entidades miembro se priorizará:

1. Accesibilidad de trámites.
2. Guías de derechos en lectura fácil con pictogramas.
3. Materiales de sensibilización.
4. Comunicación institucional accesible.
5. Kits reutilizables para entidades.
6. Plantillas de campañas.
7. Materiales para participación y consulta.

---

## 3. Arquitectura objetivo

```text
[Usuario entidad]
      |
      v
[Web App AA: Next.js]
      |
      v
[API Backend Python]
      |
      +--> [MCP Server ARASAAC]
      |        |-- Tools
      |        |-- Resources
      |        |-- Prompts
      |
      +--> [ARASAAC Connector]
      |        |-- API ARASAAC
      |        |-- Cache
      |        |-- Normalización metadatos
      |
      +--> [Material Generation Engine]
      |        |-- Plantillas
      |        |-- Layouts
      |        |-- Export PDF/DOCX/PPTX/HTML/PNG/ZIP
      |
      +--> [Governance Layer]
      |        |-- Licencia
      |        |-- Atribución
      |        |-- Auditoría
      |        |-- Revisión humana
      |        |-- Guardrails
      |
      +--> [Data Layer]
               |-- PostgreSQL
               |-- pgvector
               |-- Object Storage configurable
               |-- Audit log
```

### 3.1 Principios de arquitectura

- **API-first**: toda funcionalidad crítica se expone por API.
- **MCP-first para agentes**: el servidor MCP es la puerta estándar para clientes LLM/agentic.
- **Web-first para entidades**: las fundaciones no deben depender de Codex, Cursor o consola.
- **License-by-design**: todo material nace con atribución y restricciones.
- **Human-review-by-design**: no hay material final sin aprobación humana.
- **No personal data by default**: preferencias y perfiles no se vinculan a identidad concreta en MVP.
- **Composable generation**: cada material se construye como estructura de pasos, conceptos, pictogramas y reglas de maquetación.
- **Auditability**: cada material exportado conserva IDs ARASAAC, fecha, versión, usuario operativo y revisión.

---

## 4. Componentes técnicos

### 4.1 Frontend Web App

Stack recomendado:

- Next.js.
- TypeScript.
- React.
- Componentes accesibles.
- Formularios progresivos.
- Chat guiado.
- Vista previa editable.
- Tests de accesibilidad con axe.
- Objetivo WCAG 2.2 AA.

Funciones:

- Crear material desde petición libre.
- Crear material desde formulario.
- Seleccionar plantilla.
- Elegir contexto.
- Editar texto, pictogramas, orden, maquetación y densidad.
- Ver atribución antes de exportar.
- Aprobar/rechazar material.
- Exportar formatos.

### 4.2 Backend Python

Stack recomendado:

- Python 3.12+.
- FastAPI.
- Pydantic.
- SQLAlchemy/SQLModel.
- Alembic.
- PostgreSQL.
- pgvector.
- Redis opcional para cache caliente.
- Celery/RQ/Arq para trabajos de exportación si se requiere.

Funciones:

- Orquestación de generación.
- API REST.
- Control de materiales.
- Exportación.
- Auditoría.
- Guardrails.
- Integración ARASAAC.
- Conector MCP.

### 4.3 MCP Server

Implementación recomendada:

- Python, alineado con backend principal.
- Transporte local STDIO para Codex/desarrollo.
- Transporte remoto HTTP/Streamable HTTP para plataforma cuando esté maduro.
- Allowlist estricta de tools.
- Sin ejecución arbitraria.
- Sin shell tools.
- Todas las tools con schema Pydantic estricto.

### 4.4 Datos

Entidades principales:

- `PictogramReference`.
- `PictogramMetadataSnapshot`.
- `Material`.
- `MaterialVersion`.
- `MaterialStep`.
- `MaterialPictogramUsage`.
- `Template`.
- `EntityPreferences`.
- `GenerationRun`.
- `ReviewDecision`.
- `AuditEvent`.
- `LicenseNotice`.
- `ExportJob`.

### 4.5 Exportaciones

Formatos objetivo:

- HTML.
- PDF.
- DOCX.
- PPTX.
- PNG/JPG imprimible.
- ZIP con recursos y manifiesto.
- Markdown técnico para trazabilidad.

---

## 5. Diseño MCP

### 5.1 Tools obligatorias

1. `search_pictograms`.
2. `get_pictogram`.
3. `suggest_pictograms_for_text`.
4. `generate_visual_sequence`.
5. `generate_communication_board`.
6. `generate_social_story`.
7. `generate_accessible_document`.
8. `generate_signage_pack`.
9. `validate_license_notice`.
10. `validate_material_accessibility`.
11. `validate_pictogram_usage`.
12. `export_material`.
13. `get_templates`.
14. `get_context_options`.
15. `create_material_draft`.
16. `submit_material_for_review`.

### 5.2 Resources obligatorios

- `arasaac://license`.
- `arasaac://attribution-template`.
- `arasaac://categories`.
- `arasaac://templates/visual-agenda`.
- `arasaac://templates/communication-board`.
- `arasaac://templates/social-story`.
- `arasaac://templates/accessible-document`.
- `arasaac://templates/signage`.
- `arasaac://style-guide/accessibility-cognitive`.
- `arasaac://style-guide/plain-language`.
- `arasaac://guardrails`.
- `arasaac://review-policy`.

### 5.3 Prompts obligatorios

- `crear_agenda_visual`.
- `crear_tablero_comunicacion`.
- `crear_historia_social`.
- `adaptar_documento_lectura_facil_pictogramas`.
- `crear_senaletica_cognitiva`.
- `crear_kit_cee`.
- `crear_kit_entidad_social`.
- `crear_material_prevencion_riesgos`.
- `crear_material_atencion_ciudadana`.
- `revisar_material_accesible`.

---

## 6. Gobierno, licencia y cumplimiento

### 6.1 Política de licencia

El sistema debe aplicar siempre:

- Uso no comercial en MVP.
- Atribución visible en cada documento.
- Trazabilidad interna de todos los pictogramas usados.
- Prohibición de uso de IA generativa para crear pictogramas.
- Prohibición de modificación del pictograma original.
- Prohibición de ocultar atribución.
- Modo de cumplimiento antes de exportar.

### 6.2 Atribución mínima visible

Cada exportación debe incluir un bloque visible de créditos:

```text
Los símbolos pictográficos utilizados son propiedad del Gobierno de Aragón y han sido creados por Sergio Palao para ARASAAC (https://arasaac.org), que los distribuye bajo licencia Creative Commons BY-NC-SA.
```

También se guardará una atribución estructurada por cada pictograma:

```json
{
  "origin": "ARASAAC",
  "author": "Sergio Palao",
  "owner": "Gobierno de Aragón",
  "license": "CC BY-NC-SA",
  "pictogram_id": "...",
  "retrieved_at": "..."
}
```

### 6.3 Relación institucional con ARASAAC

La estrategia decidida es:

1. Diseñar MVP.
2. Documentar estrictamente licencia y atribución.
3. Preparar dossier institucional.
4. Solicitar validación/bendición de ARASAAC antes de piloto público significativo.
5. No hacer explotación comercial sin autorización expresa.

---

## 7. Revisión humana

La revisión humana es obligatoria siempre antes de exportar el material como final.

Estados del material:

1. `draft_generated`.
2. `draft_edited`.
3. `pending_review`.
4. `approved`.
5. `exported`.
6. `rejected`.
7. `archived`.

Criterios mínimos de aprobación:

- Texto claro.
- Pictogramas reales.
- Atribución visible.
- Licencia correcta.
- Sin datos personales.
- Sin contenido médico/educativo sensible no revisado.
- Coherencia secuencial.
- Densidad visual adecuada.
- Formato accesible.

---

## 8. Roadmap por fases

### Fase 0 — Preparación y base documental

Objetivo: dejar el proyecto listo para Codex/OpenSpec.

Entregables:

- Plan Maestro.
- AGENTS.md.
- OpenSpec map.
- ADRs iniciales.
- Política de licencia.
- Política de revisión humana.
- Repo skeleton.

### Fase 1 — MVP técnico validable

Objetivo: alcanzar un MVP tipo C sobre base B: usable por una entidad real, con gobierno y trazabilidad suficientes.

Incluye:

- Backend Python.
- Conector ARASAAC.
- Búsqueda básica literal.
- Referencias reales a pictogramas.
- MCP local.
- Web App básica AA.
- Generador de agenda visual.
- Generador de tablero básico.
- Export HTML/PDF.
- Atribución visible.
- Revisión humana obligatoria.
- Auditoría mínima.

### Fase 2 — Producto piloto gobernado

Incluye:

- Plantillas por contexto.
- Señalética.
- Historias sociales.
- Lectura fácil con pictogramas.
- Export DOCX/PPTX/ZIP.
- Preferencias de entidad.
- Búsqueda semántica inicial.
- Observabilidad completa.
- Keycloak.
- Multi-entidad simple.

### Fase 3 — Plataforma social escalable

Incluye:

- Multi-tenant.
- Sincronización periódica catálogo ARASAAC.
- pgvector avanzado.
- Evaluación automática de calidad.
- Kits para CONACEE/CERMI.
- Administración de plantillas.
- Dossier ARASAAC.
- Piloto institucional.

### Fase 4 — Ecosistema abierto

Incluye:

- Publicación open source si procede legalmente.
- Guía de implantación.
- Formación.
- Soporte profesional.
- Comunidad de entidades.
- Contribución externa con revisión y versionado.

---

## 9. Definition of Done maestro

Una tarea solo se considera terminada si:

1. Tiene OpenSpec asociado.
2. Tiene tests unitarios o de integración según aplique.
3. No rompe lint/typecheck.
4. Mantiene atribución y trazabilidad.
5. Respeta guardrails.
6. No introduce datos personales innecesarios.
7. Documenta decisiones relevantes.
8. Actualiza README o docs si cambia comportamiento.
9. Añade criterios de aceptación verificables.
10. Pasa revisión humana cuando afecta a generación de materiales.

---

## 10. Riesgos maestros

| Riesgo | Severidad | Mitigación |
|---|---:|---|
| Uso comercial no autorizado | Alta | Modo no comercial, autorización previa, bloqueos de exportación comercial |
| Atribución incompleta | Alta | Validador automático obligatorio antes de exportar |
| Pictogramas inventados | Alta | Solo IDs reales ARASAAC, tool-based retrieval |
| Material inadecuado para usuario final | Alta | Revisión humana obligatoria |
| Sustitución de profesionales CAA | Alta | Disclaimer + workflow de apoyo, no diagnóstico |
| Datos sensibles | Alta | MVP sin vinculación a personas concretas |
| Baja accesibilidad web | Alta | WCAG 2.2 AA como criterio de aceptación |
| API externa inestable | Media | Caché, snapshots y sincronización controlada |
| Complejidad de exportación | Media | Primero HTML/PDF, luego DOCX/PPTX/ZIP |
| Reputación institucional | Alta | Validación con ARASAAC antes de piloto público amplio |

---

## 11. Métricas

### Adopción

- Materiales generados.
- Entidades activas.
- Usuarios activos.
- Materiales reutilizados.
- Tiempo ahorrado.

### Calidad

- Acierto pictograma-concepto.
- Comprensión por usuarios/profesionales.
- Satisfacción de profesionales.
- Reducción de tiempo de creación.
- Menor necesidad de corrección.

### Impacto social

- Mayor autonomía.
- Mejor comprensión.
- Mejor inclusión laboral.
- Mejor comunicación.
- Mejor accesibilidad institucional.

---

## 12. Decisión final de ejecución

La ejecución debe comenzar por un MVP mínimo validable, con foco en:

1. Conector ARASAAC.
2. MCP Server.
3. Web App accesible.
4. Agenda visual.
5. Tablero de comunicación.
6. Atribución/licencia.
7. Revisión humana.
8. Export PDF/HTML.

Este MVP permitirá validar valor, riesgos y encaje institucional antes de aumentar complejidad.
"""

agents = """# Agentes, Skills y Workflows Agénticos — ARASAAC Social MCP Platform

## 1. Modelo operativo

El desarrollo se ejecutará con un equipo agéntico coordinado por OpenSpec y Codex. Cada agente tiene ámbito, entradas, salidas, restricciones y Definition of Done. Ningún agente puede saltarse licencia, revisión humana o trazabilidad.

Flujo base:

```text
Intake -> Discovery -> OpenSpec Proposal -> Design -> Tasks -> Codex Implementation -> Tests -> Review -> Archive
```

Flujo para materiales:

```text
Petición usuario -> Interpretación -> Estructura -> Búsqueda ARASAAC -> Propuesta pictográfica -> Validación -> Revisión humana -> Exportación
```

---

## 2. Agentes de producto y dominio

### 2.1 Product Owner Agent

**Misión:** convertir necesidades de fundaciones, CONACEE, CERMI y CEE en capacidades priorizadas.

**Entradas:** objetivos sociales, feedback de entidades, roadmap, restricciones de licencia.  
**Salidas:** épicas, capacidades, criterios de aceptación, prioridad.  
**No puede:** aprobar uso comercial ni cambiar licencia.  
**DoD:** cada capacidad tiene usuario, valor, alcance, fuera de alcance y métrica.

### 2.2 Accessibility Expert Agent

**Misión:** asegurar que Web App y materiales cumplen criterios de accesibilidad digital y cognitiva.

**Entradas:** pantallas, componentes, flujos, materiales.  
**Salidas:** checklist WCAG 2.2 AA, recomendaciones de accesibilidad cognitiva, bloqueos.  
**DoD:** todo flujo tiene navegación teclado, foco visible, contraste, semántica, errores claros y lenguaje comprensible.

### 2.3 CAA/SAAC Methodology Agent

**Misión:** guiar criterios de comunicación aumentativa y alternativa.

**Entradas:** material, contexto, perfil no identificable, tipo de apoyo.  
**Salidas:** estructura recomendada, densidad, nivel de abstracción, revisión necesaria.  
**DoD:** material no sobrecarga, usa conceptos claros y no sustituye criterio profesional.

### 2.4 Foundation/NGO Domain Agent

**Misión:** adaptar el producto a la realidad de entidades pequeñas y medianas.

**Entradas:** contexto organizativo, recursos, perfiles, procesos.  
**Salidas:** flujos simples, plantillas útiles, documentación no técnica.  
**DoD:** una entidad puede crear un material sin conocimiento técnico.

---

## 3. Agentes técnicos

### 3.1 MCP Architect Agent

**Misión:** diseñar servidor MCP seguro, tool schemas, resources y prompts.

**Entradas:** capacidades, OpenSpecs, modelo de datos.  
**Salidas:** contratos MCP, schemas Pydantic, tests de tool calls.  
**DoD:** cada tool es determinista, allowlisted, tipada, auditada y sin ejecución arbitraria.

### 3.2 Backend Agent

**Misión:** implementar API Python/FastAPI, servicios de dominio, persistencia y orquestación.

**Entradas:** specs técnicas, modelo de datos, tests.  
**Salidas:** endpoints, services, repositories, migrations, tests.  
**DoD:** API documentada, validada, testeada y sin datos personales innecesarios.

### 3.3 Frontend Agent

**Misión:** implementar Web App Next.js accesible AA.

**Entradas:** flujos UX, tokens, componentes, API contracts.  
**Salidas:** páginas, componentes, formularios, chat guiado, preview editable.  
**DoD:** pasa checks de accesibilidad, keyboard nav y estados de error.

### 3.4 Data/Indexing Agent

**Misión:** diseñar sincronización, caché, metadatos y búsqueda semántica futura.

**Entradas:** API ARASAAC, metadatos, categorías, palabras clave.  
**Salidas:** schema, embeddings, pgvector, ranking.  
**DoD:** no guarda pictogramas sin metadatos de licencia y trazabilidad.

### 3.5 Export/Document Agent

**Misión:** generar HTML, PDF, DOCX, PPTX, PNG/JPG y ZIP.

**Entradas:** material estructurado, plantilla, licencia.  
**Salidas:** documentos exportados, manifiesto, créditos.  
**DoD:** toda exportación incluye atribución visible y manifiesto técnico.

---

## 4. Agentes de calidad, seguridad y cumplimiento

### 4.1 QA Agent

**Misión:** asegurar pruebas funcionales y regresión.

**Salidas:** test plan, pruebas E2E, smoke tests, criterios de aceptación ejecutados.

### 4.2 Accessibility QA Agent

**Misión:** probar accesibilidad web y de materiales.

**Salidas:** informe WCAG, issues, bloqueos.

### 4.3 License Compliance Agent

**Misión:** validar CC BY-NC-SA, atribución, no comercialidad y ausencia de modificaciones.

**Salidas:** reporte de cumplimiento, bloqueo de exportación si falla.

### 4.4 Security Agent

**Misión:** seguridad MCP/API, privacidad, threat modeling, no ejecución arbitraria.

**Salidas:** threat model, controles, tests de abuso.

### 4.5 Test Automation Agent

**Misión:** automatizar unit, integration, contract, E2E y accessibility tests.

**Salidas:** suites CI-ready.

---

## 5. Agentes de gobierno

### 5.1 OpenSpec Steward

**Misión:** mantener la coherencia de proposals, designs, tasks y spec deltas.

### 5.2 Architecture Reviewer

**Misión:** revisar decisiones técnicas, ADRs, acoplamientos y escalabilidad.

### 5.3 Risk & Compliance Agent

**Misión:** mantener matriz de riesgos, DPIA/EIPD de diseño aunque no se traten datos personales.

### 5.4 Documentation Agent

**Misión:** mantener README, manual técnico, manual entidad, guía contribución y despliegue.

### 5.5 Release Manager Agent

**Misión:** preparar releases, changelog, versionado y checklist de piloto.

---

## 6. Skills

### 6.1 Skills de generación

| Skill | Entrada | Salida | Validadores |
|---|---|---|---|
| `skill.create_visual_agenda` | objetivo, contexto, nivel, idioma | agenda estructurada | pictogramas reales, secuencia, atribución |
| `skill.create_communication_board` | dominio, categorías, vocabulario | tablero | densidad, categorías, pictogramas reales |
| `skill.create_social_story` | situación, persona no identificable, pasos | historia social | tono, secuencia, revisión |
| `skill.convert_to_easy_reading` | texto fuente, nivel | texto fácil + pictos | lectura fácil, no pérdida crítica |
| `skill.create_signage_pack` | espacios, formato | carteles | consistencia, créditos |
| `skill.create_cee_kit` | proceso CEE | kit | utilidad, contexto laboral, PRL si aplica |

### 6.2 Skills técnicas

| Skill | Función |
|---|---|
| `skill.query_arasaac_api` | consultar API ARASAAC |
| `skill.normalize_pictogram_metadata` | normalizar autoría/licencia/categorías |
| `skill.rank_pictogram_candidates` | ranking literal/semántico/contextual |
| `skill.cache_pictogram_reference` | caché con trazabilidad |
| `skill.export_pdf_docx_pptx` | exportación multi-formato |
| `skill.validate_license` | validación BY-NC-SA |
| `skill.sync_catalog` | sincronización periódica |

### 6.3 Skills de evaluación

| Skill | Función |
|---|---|
| `skill.evaluate_plain_language` | claridad textual |
| `skill.evaluate_pictogram_match` | adecuación concepto-pictograma |
| `skill.evaluate_visual_density` | carga visual |
| `skill.evaluate_license_attribution` | créditos y licencia |
| `skill.evaluate_sensitive_content` | salud, menores, CAA, PRL |
| `skill.evaluate_export_readiness` | bloqueo/aprobación exportación |

### 6.4 Skills de documentación

- `skill.generate_readme`.
- `skill.generate_entity_manual`.
- `skill.generate_technical_manual`.
- `skill.generate_deployment_guide`.
- `skill.generate_contribution_guide`.
- `skill.generate_arasaac_validation_dossier`.

---

## 7. Workflows

### 7.1 Workflow maestro de desarrollo

```text
1. Intake de necesidad
2. OpenSpec Steward crea change folder
3. Product Owner Agent redacta proposal
4. Architecture Reviewer redacta design
5. Backend/Frontend/MCP/Data agents refinan tasks
6. License Compliance Agent añade restricciones
7. Codex implementa task atómica
8. Test Automation Agent ejecuta pruebas
9. QA + Accessibility QA validan
10. Release Manager prepara entrega
11. OpenSpec Steward archiva
```

### 7.2 Workflow de creación de material

```text
1. Usuario elige tipo de material
2. Sistema guía con preguntas simples
3. LLM estructura intención y pasos
4. MCP busca pictogramas ARASAAC
5. Ranking propone candidatos
6. Usuario/profesional edita y selecciona
7. Validadores verifican licencia, accesibilidad, coherencia
8. Material pasa a revisión humana
9. Revisor aprueba
10. Sistema exporta con créditos y manifiesto
```

### 7.3 Workflow de validación antes de exportar

```text
validate_material
  -> validate_pictogram_ids_real
  -> validate_no_modified_pictograms
  -> validate_license_notice_visible
  -> validate_no_personal_data
  -> validate_plain_language
  -> validate_visual_density
  -> validate_review_approval
  -> export_allowed
```

### 7.4 Workflow para dossier ARASAAC

```text
1. Documentar propósito social
2. Documentar arquitectura y limitaciones
3. Documentar uso no comercial
4. Incluir política de atribución
5. Incluir ejemplos de materiales
6. Incluir mecanismos de bloqueo
7. Solicitar revisión/bendición institucional
```
"""

repo = """# Repo Skeleton — ARASAAC Social MCP Platform

```text
arasaac-social-mcp/
  README.md
  LICENSE.md
  NOTICE-ARASAAC.md
  AGENTS.md
  docker-compose.yml
  .env.example
  .gitignore
  Makefile

  openspec/
    project.md
    adr/
      ADR-0001-python-backend.md
      ADR-0002-nextjs-frontend.md
      ADR-0003-postgres-pgvector.md
      ADR-0004-license-by-design.md
      ADR-0005-human-review-by-design.md
    changes/
      0001-project-foundation/
      0002-arasaac-license-governance/
      0003-arasaac-connector/
      0004-mcp-server-core/
      0005-pictogram-search-tools/
      0006-material-domain-model/
      0007-visual-agenda-generator/
      0008-communication-board-generator/
      0009-accessible-document-generator/
      0010-social-story-generator/
      0011-signage-generator/
      0012-export-engine/
      0013-web-app-shell-aa/
      0014-guided-creation-flow/
      0015-preview-editor/
      0016-review-workflow/
      0017-audit-observability/
      0018-preferences-without-pii/
      0019-testing-quality-gates/
      0020-docker-compose-deployment/
      0021-keycloak-future-auth/
      0022-semantic-search-future/
      0023-multientity-future/
      0024-arasaac-validation-dossier/

  apps/
    web/
      package.json
      next.config.js
      src/
        app/
        components/
        features/
        lib/
        styles/
        tests/

  services/
    api/
      pyproject.toml
      src/arasaac_platform/
        main.py
        api/
        domain/
        services/
        repositories/
        schemas/
        mcp/
        arasaac/
        export/
        governance/
        audit/
      tests/
      alembic/

  packages/
    shared-contracts/
      schemas/
      openapi/
      mcp-tools/

  docs/
    architecture/
    deployment/
    user-manual/
    entity-manual/
    accessibility/
    compliance/
    arasaac-dossier/

  scripts/
    sync_arasaac_catalog.py
    export_material.py
    validate_license.py

  tests/
    e2e/
    accessibility/
    fixtures/
```

## Comandos esperados

```bash
make setup
make dev
make test
make lint
make typecheck
make accessibility-test
make openspec-verify
make docker-up
```

## Política de ramas

- `main`: estable.
- `develop`: integración.
- `feature/openspec-XXXX-name`: implementación por OpenSpec.
- `release/x.y.z`: preparación de piloto/release.

## Convención de commits

```text
feat(mcp): add search_pictograms tool
fix(license): enforce visible attribution before export
test(export): add pdf license notice checks
docs(openspec): add visual agenda spec
```
"""

agents_md = """# AGENTS.md — ARASAAC Social MCP Platform

## 1. Identidad del proyecto

Este repositorio implementa una plataforma social no comercial para generar materiales accesibles usando exclusivamente pictogramas reales de ARASAAC, con MCP, Web App accesible AA, revisión humana, atribución visible y trazabilidad completa.

## 2. Reglas absolutas

1. No generar pictogramas con IA.
2. No imitar el estilo ARASAAC con IA.
3. No modificar pictogramas ARASAAC.
4. No eliminar ni ocultar atribución.
5. No exportar material final sin revisión humana aprobada.
6. No vincular materiales a personas concretas en MVP.
7. No introducir datos personales sensibles.
8. No usar el sistema para diagnóstico médico, psicológico, educativo o CAA.
9. No implementar ejecución arbitraria en MCP.
10. No añadir tools MCP sin schema estricto, tests y revisión de seguridad.

## 3. Stack aprobado

- Backend: Python + FastAPI + Pydantic.
- Frontend: Next.js + React + TypeScript.
- DB: PostgreSQL + pgvector.
- Cache: Redis opcional.
- Deploy MVP: Docker Compose.
- Auth MVP: sin auth; futuro Keycloak.
- Export: HTML/PDF primero; DOCX/PPTX/ZIP después.

## 4. Flujo OpenSpec obligatorio

Antes de escribir código:

1. Crear change folder en `openspec/changes/<id>/`.
2. Redactar `proposal.md`.
3. Redactar `design.md` si hay arquitectura o decisión técnica.
4. Redactar `tasks.md` con tareas atómicas.
5. Redactar `spec.md` con escenarios verificables.
6. Ejecutar verificación.
7. Implementar con Codex.
8. Ejecutar tests.
9. Actualizar docs.
10. Archivar OpenSpec al completar.

## 5. Definition of Done

Una implementación está completa si:

- Tiene OpenSpec aprobado.
- Tiene tests.
- Pasa lint/typecheck.
- No viola licencia ARASAAC.
- Incluye atribución si toca materiales.
- Mantiene audit log si genera/exporta.
- No introduce PII.
- Cumple accesibilidad AA si toca frontend.
- Actualiza documentación.

## 6. Seguridad MCP

- Usar allowlist de tools.
- Validar todos los inputs con Pydantic.
- No shell execution.
- No filesystem arbitrary access.
- No network calls fuera de conectores aprobados.
- No secretos en logs.
- Registrar tool calls relevantes.

## 7. Política ARASAAC

Cada uso de pictograma debe almacenar:

- ID ARASAAC.
- Label usado.
- URL/origen.
- Autor: Sergio Palao.
- Propietario: Gobierno de Aragón.
- Licencia: CC BY-NC-SA.
- Fecha de recuperación.
- Material donde se usó.

Cada exportación debe incluir atribución visible.

## 8. Accesibilidad

El frontend debe aspirar a WCAG 2.2 AA:

- Navegación por teclado.
- Foco visible.
- Contraste suficiente.
- Estructura semántica.
- Labels y errores claros.
- No depender solo del color.
- Textos comprensibles.
- Componentes testeables con axe.

## 9. Agentes autorizados

- Product Owner Agent.
- Accessibility Expert Agent.
- CAA/SAAC Methodology Agent.
- Foundation/NGO Domain Agent.
- MCP Architect Agent.
- Backend Agent.
- Frontend Agent.
- Data/Indexing Agent.
- Export/Document Agent.
- QA Agent.
- Accessibility QA Agent.
- License Compliance Agent.
- Security Agent.
- Test Automation Agent.
- OpenSpec Steward.
- Architecture Reviewer.
- Risk & Compliance Agent.
- Documentation Agent.
- Release Manager Agent.

## 10. Instrucción a Codex

Codex debe trabajar siempre contra una task atómica de OpenSpec. Si una tarea no tiene spec, no se implementa. Si se detecta conflicto entre productividad y cumplimiento, gana cumplimiento.
"""

open_map = """# Mapa de OpenSpecs — ARASAAC Social MCP Platform

## Convención

Cada OpenSpec se ubica en:

```text
openspec/changes/<id>/
  proposal.md
  design.md
  tasks.md
  spec.md
```

## Releases

### Release 0 — Foundation

| ID | Nombre | Objetivo | Bloquea |
|---|---|---|---|
| 0001 | project-foundation | Repo, convenciones, tooling, Docker base | Todo |
| 0002 | arasaac-license-governance | Licencia, atribución, políticas | Generación/export |
| 0006 | material-domain-model | Modelo de materiales y trazabilidad | Generadores |
| 0019 | testing-quality-gates | CI, tests, DoD | Todo |
| 0020 | docker-compose-deployment | Despliegue local | MVP |

### Release 1 — MVP Validable

| ID | Nombre | Objetivo | Depende de |
|---|---|---|---|
| 0003 | arasaac-connector | Conectar API ARASAAC y normalizar | 0001, 0002 |
| 0004 | mcp-server-core | Servidor MCP local | 0001 |
| 0005 | pictogram-search-tools | search/get/suggest | 0003, 0004 |
| 0007 | visual-agenda-generator | Agenda visual | 0005, 0006 |
| 0008 | communication-board-generator | Tablero comunicación | 0005, 0006 |
| 0012 | export-engine | HTML/PDF + créditos | 0002, 0006 |
| 0013 | web-app-shell-aa | Web AA base | 0001 |
| 0014 | guided-creation-flow | flujo guiado | 0013, 0007, 0008 |
| 0015 | preview-editor | vista previa editable | 0014 |
| 0016 | review-workflow | revisión humana | 0006, 0015 |
| 0017 | audit-observability | auditoría mínima | 0006 |

### Release 2 — Producto piloto

| ID | Nombre | Objetivo |
|---|---|---|
| 0009 | accessible-document-generator | lectura fácil + pictos |
| 0010 | social-story-generator | historias sociales |
| 0011 | signage-generator | señalética |
| 0018 | preferences-without-pii | preferencias entidad/plantilla/perfil no personal |
| 0022 | semantic-search-future | ranking semántico con pgvector |
| 0024 | arasaac-validation-dossier | dossier de bendición ARASAAC |

### Release 3 — Escalado

| ID | Nombre | Objetivo |
|---|---|---|
| 0021 | keycloak-future-auth | autenticación/roles |
| 0023 | multientity-future | multi-entidad simple y camino multi-tenant |

---

## Precedencias críticas

```text
0001 -> 0002 -> 0003 -> 0005 -> 0007/0008 -> 0012 -> 0016
0001 -> 0013 -> 0014 -> 0015 -> 0016
0006 -> 0007/0008/0009/0010/0011 -> 0017
0019 atraviesa todas las specs
```
"""

risk = """# Roadmap, Backlog, DoD y Matriz de Riesgos

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
"""

# Write top-level docs
for name, content in {
    '00_PLAN_MAESTRO.md': plan,
    '01_MAPA_OPENSPEC.md': open_map,
    '02_AGENTES_SKILLS_WORKFLOWS.md': agents,
    '03_REPO_SKELETON.md': repo,
    '04_ROADMAP_BACKLOG_DOD_RIESGOS.md': risk,
    'AGENTS.md': agents_md,
    '99_FUENTES_Y_REFERENCIAS.md': sources,
}.items():
    (base / name).write_text(content.strip() + '\n', encoding='utf-8')

# Generate openspec change folders
change_specs = [
    ('0001-project-foundation','Base del proyecto, repo skeleton, tooling y convenciones','Crear estructura de repositorio, Makefile, Docker Compose inicial, CI básico y documentación raíz.','No implementa lógica ARASAAC ni generación.','Repo arranca en local; make test/lint existen; README y AGENTS.md presentes.'),
    ('0002-arasaac-license-governance','Gobierno de licencia ARASAAC y atribución','Implementar política CC BY-NC-SA, atribución visible, bloqueos de exportación y NOTICE.','No decide uso comercial; no sustituye revisión legal.','Toda exportación contiene créditos visibles; toda referencia guarda autoría/licencia.'),
    ('0003-arasaac-connector','Conector API ARASAAC','Consultar API ARASAAC, normalizar resultados y metadatos, cachear referencias con trazabilidad.','No descarga masiva sin control; no modifica pictogramas.','search/get devuelven IDs reales y metadatos normalizados.'),
    ('0004-mcp-server-core','Servidor MCP core','Exponer servidor MCP local con tools/resources/prompts, schemas estrictos y allowlist.','No shell execution; no tools no aprobadas.','Cliente MCP puede listar tools/resources/prompts y ejecutar health/tool básica.'),
    ('0005-pictogram-search-tools','Tools MCP de búsqueda pictográfica','Implementar search_pictograms, get_pictogram, suggest_pictograms_for_text.','No inventa pictogramas; no genera imágenes.','Tool calls devuelven resultados reales o vacío con error estructurado.'),
    ('0006-material-domain-model','Modelo de dominio de materiales','Definir Material, Version, Step, PictogramUsage, ReviewDecision, ExportJob, AuditEvent.','No almacena PII de beneficiarios.','Modelo permite trazabilidad completa de pictogramas por material.'),
    ('0007-visual-agenda-generator','Generador de agenda visual','Crear agendas visuales por contexto, pasos, nivel cognitivo y pictogramas sugeridos.','No exporta final sin revisión.','Agenda draft generada, editable y validable.'),
    ('0008-communication-board-generator','Generador de tablero de comunicación','Crear tableros por dominio/categoría/vocabulario con densidad guiada.','No presupone diagnóstico ni perfil personal.','Tablero draft con categorías, pictogramas y validación de densidad.'),
    ('0009-accessible-document-generator','Generador de documento accesible','Adaptar documentos a lectura fácil con pictogramas ARASAAC.','No altera obligaciones legales; requiere revisión humana.','Documento draft con texto simplificado, pictogramas y avisos de revisión.'),
    ('0010-social-story-generator','Generador de historias sociales','Crear historias sociales con estructura clara, secuencial y revisable.','No sustituye intervención profesional.','Historia social draft lista para revisión.'),
    ('0011-signage-generator','Generador de señalética cognitiva','Crear carteles/señales para espacios, servicios, procesos y CEE.','No modifica pictogramas originales.','Pack de señalética con créditos visibles.'),
    ('0012-export-engine','Motor de exportación','Exportar HTML/PDF primero y preparar DOCX/PPTX/PNG/ZIP.','No exporta si no hay review approved ni atribución.','Export generado contiene manifiesto y créditos.'),
    ('0013-web-app-shell-aa','Shell Web App accesible AA','Implementar interfaz Next.js base con navegación accesible, layout y componentes.','No incluye auth en MVP.','Pantallas base pasan revisión AA automatizada inicial.'),
    ('0014-guided-creation-flow','Flujo guiado de creación','Implementar wizard + chat guiado + formularios por material/contexto.','No salta revisión humana.','Usuario puede crear borrador de agenda/tablero desde UI.'),
    ('0015-preview-editor','Vista previa editable','Permitir editar texto, pictogramas, orden, densidad y maquetación antes de revisión.','No altera pictogramas; solo composición.','Preview refleja cambios y conserva trazabilidad.'),
    ('0016-review-workflow','Workflow de revisión humana','Estados pending_review, approved, rejected; bloqueo export si no approved.','No autoaprueba materiales.','Export solo habilitado si estado approved.'),
    ('0017-audit-observability','Auditoría y observabilidad','Registrar generación, tool calls, pictogramas usados, exportaciones, errores y métricas.','No guarda prompts con PII; sanitiza datos.','AuditEvent disponible para trazabilidad y métricas.'),
    ('0018-preferences-without-pii','Preferencias sin PII','Guardar preferencias de entidad, plantilla y perfil no identificable.','No vincula a persona concreta.','Preferencias reutilizables sin datos personales.'),
    ('0019-testing-quality-gates','Quality gates y testing','Configurar unit/integration/contract/E2E/accessibility/license tests.','No permite merges sin gates mínimos.','CI ejecuta pruebas críticas y reporta fallos.'),
    ('0020-docker-compose-deployment','Despliegue Docker Compose','Levantar web, api, db, redis opcional y servicios base en local.','No producción multi-tenant.','docker compose up inicia MVP local.'),
    ('0021-keycloak-future-auth','Auth futura con Keycloak','Diseñar autenticación y roles para fases posteriores.','No se implementa en MVP salvo stubs.','ADR y diseño listos para fase 2/3.'),
    ('0022-semantic-search-future','Búsqueda semántica futura','Diseñar e implementar progresivamente ranking por embeddings con pgvector.','No sustituye edición humana.','Ranking semántico mejora matching y es evaluable.'),
    ('0023-multientity-future','Multi-entidad futura','Preparar modelo para entidad simple y futura multi-tenancy.','No activar multi-tenant en MVP.','Diseño evita bloqueos estructurales.'),
    ('0024-arasaac-validation-dossier','Dossier de validación ARASAAC','Generar dossier institucional para solicitar bendición de ARASAAC.','No implica autorización automática.','Dossier contiene propósito, límites, atribución, ejemplos y controles.'),
]

for cid, title, goal, outscope, acceptance in change_specs:
    d = base / 'openspec' / 'changes' / cid
    d.mkdir(parents=True, exist_ok=True)
    proposal = f"""# Proposal — {cid}

## Problema

{title} es necesario para cumplir el Plan Maestro y permitir una evolución trazable mediante OpenSpec y Codex.

## Solución propuesta

{goal}

## Alcance

- Implementar la capacidad descrita.
- Añadir pruebas y documentación.
- Respetar licencia ARASAAC, revisión humana y no PII cuando aplique.

## Fuera de alcance

{outscope}

## Riesgos

- Incumplimiento de licencia.
- Falta de trazabilidad.
- Complejidad excesiva.
- Pérdida de accesibilidad.

## Métrica de éxito

{acceptance}
"""
    design = f"""# Design — {cid}

## Decisiones de diseño

- Implementar de forma incremental.
- Mantener contratos claros.
- Añadir validaciones automáticas.
- Registrar auditoría cuando haya generación, pictogramas o exportación.
- Mantener separación entre dominio, infraestructura y presentación.

## Contratos esperados

- Inputs tipados.
- Outputs serializables.
- Errores estructurados.
- Tests de contrato si la capacidad expone API o MCP.

## Seguridad y cumplimiento

- No almacenar datos personales salvo que una spec futura lo apruebe expresamente.
- No ejecutar comandos arbitrarios.
- No omitir licencia ni atribución.
- No crear ni modificar pictogramas ARASAAC.

## Observabilidad

Registrar eventos relevantes con correlation_id, material_id si existe, tool_name si existe y resultado.
"""
    tasks = f"""# Tasks — {cid}

- [ ] Revisar dependencias OpenSpec.
- [ ] Definir interfaces y modelos.
- [ ] Implementar funcionalidad mínima.
- [ ] Añadir validaciones.
- [ ] Añadir tests unitarios.
- [ ] Añadir tests de integración/contrato si aplica.
- [ ] Añadir documentación.
- [ ] Ejecutar lint/typecheck/test.
- [ ] Revisar licencia/accesibilidad/seguridad si aplica.
- [ ] Actualizar changelog o notas de release.
"""
    spec = f"""# Spec — {cid}

## Capability

{title}

## Scenarios

### Scenario 1 — ejecución nominal

**Given** el sistema está configurado correctamente  
**When** se ejecuta la capacidad  
**Then** produce una salida válida y trazable.

### Scenario 2 — entrada inválida

**Given** una entrada incompleta o inválida  
**When** se invoca la capacidad  
**Then** el sistema devuelve error estructurado sin efectos secundarios peligrosos.

### Scenario 3 — cumplimiento

**Given** la capacidad afecta a pictogramas, materiales, exportación o usuario  
**When** se genera o transforma información  
**Then** se respetan licencia, atribución, no PII y revisión humana si aplica.

## Acceptance Criteria

- {acceptance}
- Hay tests automatizados.
- Hay documentación mínima.
- No se incumplen reglas absolutas del AGENTS.md.
"""
    (d/'proposal.md').write_text(proposal, encoding='utf-8')
    (d/'design.md').write_text(design, encoding='utf-8')
    (d/'tasks.md').write_text(tasks, encoding='utf-8')
    (d/'spec.md').write_text(spec, encoding='utf-8')

# Create ADRs
adr_dir = base / 'openspec' / 'adr'
adr_dir.mkdir(parents=True, exist_ok=True)
adrs = {
'ADR-0001-python-backend.md': '# ADR-0001 — Python backend\n\n## Decisión\n\nUsar Python/FastAPI como backend principal y MCP server, alineado con la preferencia del proyecto y facilidad para IA, validación, exportación y servicios.\n\n## Consecuencias\n\n- Menor fricción para servicios IA.\n- Pydantic como contrato fuerte.\n- Ecosistema amplio para exportación y datos.\n',
'ADR-0002-nextjs-frontend.md': '# ADR-0002 — Next.js frontend\n\n## Decisión\n\nUsar Next.js/React/TypeScript para la Web App AA.\n\n## Consecuencias\n\n- Buen soporte de componentes, SSR/SPA y accesibilidad.\n- Permite una experiencia tipo Open WebUI adaptada a entidades.\n',
'ADR-0003-postgres-pgvector.md': '# ADR-0003 — PostgreSQL + pgvector\n\n## Decisión\n\nUsar PostgreSQL con pgvector como base transaccional y vectorial open source y escalable.\n\n## Consecuencias\n\n- Simplifica operación frente a dos motores separados.\n- Escala razonablemente para MVP y piloto.\n- Puede migrarse a Qdrant si el volumen/vector search lo exige.\n',
'ADR-0004-license-by-design.md': '# ADR-0004 — License by design\n\n## Decisión\n\nLa licencia ARASAAC se modela como parte del dominio, no como texto decorativo.\n\n## Consecuencias\n\n- No se exporta sin atribución.\n- Se guarda trazabilidad por pictograma.\n- El sistema puede preparar dossier institucional.\n',
'ADR-0005-human-review-by-design.md': '# ADR-0005 — Human review by design\n\n## Decisión\n\nTodo material requiere aprobación humana antes de exportarse como final.\n\n## Consecuencias\n\n- Reduce riesgo de materiales inadecuados.\n- Refuerza rol de profesionales.\n- Añade estados de workflow y auditoría.\n'
}
for name, content in adrs.items():
    (adr_dir/name).write_text(content, encoding='utf-8')

# Create project.md
(base/'openspec'/'project.md').write_text('# OpenSpec Project — ARASAAC Social MCP Platform\n\nEste proyecto usa OpenSpec como fuente de verdad para cambios. Cada cambio vive en `openspec/changes/<id>/` con proposal, design, tasks y spec.\n', encoding='utf-8')

# Zip everything, excluding script itself maybe include okay? remove script from zip
zip_path = Path('/mnt/data/arasaac_mcp_master_plan.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in base.rglob('*'):
        if p.is_file() and p.name != 'generate_files.py':
            z.write(p, p.relative_to(base.parent))
print(zip_path)
