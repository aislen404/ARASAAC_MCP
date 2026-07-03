# AGENTS.md — ARASAAC Social MCP Platform

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
