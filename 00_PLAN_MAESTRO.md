# Plan Maestro — MCP ARASAAC para generación de materiales accesibles

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
