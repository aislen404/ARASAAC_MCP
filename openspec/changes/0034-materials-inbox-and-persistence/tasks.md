# Tasks — 0034 Workspaces, Materials Inbox and Real Persistence

> **Orden de implementación global**: 0033 primero → 0032 y 0034 en paralelo → 0035 al final.
> Esta change (0034) puede empezar en paralelo a 0032 en cuanto 0033 haya definido el contrato de validación. Bloquea a 0035.

## 1. OpenSpec

- [x] Crear `proposal.md`, `design.md`, `tasks.md`, `spec.md`.
- [x] Confirmar decisiones (PO 2026-07-14): workspace por slug legible, welcome screen, sin roles internos, cero client-storage, Postgres obligatorio.

## 2. Backend — modelo Workspace

- [ ] Crear entidad `Workspace` (Pydantic + SQLAlchemy) en `services/api/src/arasaac_platform/domain/workspaces.py`.
- [ ] Implementar generador de slugs con 3 diccionarios cerrados (animales, adjetivos, sustantivos_naturaleza) en `services/api/src/arasaac_platform/domain/slug_generator.py`.
- [ ] Test unitario: unicidad, formato `^[a-z]+(-[a-z]+){2,4}$`, retry en colisión, sin PII en el diccionario.
- [ ] Repositorio `WorkspaceRepository` (Postgres + in-memory para tests).

## 3. Backend — migraciones Alembic

- [ ] Nueva revisión: tabla `workspaces (workspace_id UUID PK, slug TEXT UNIQUE NOT NULL, display_name TEXT NULL, timestamps)`.
- [ ] Añadir columna `workspace_id UUID NOT NULL REFERENCES workspaces` a `materials`.
- [ ] Añadir columna `workspace_id UUID NOT NULL REFERENCES workspaces` a `audit_events`.
- [ ] Índices: `materials(workspace_id, status)`, `materials(workspace_id, updated_at)`, `audit_events(workspace_id, created_at)`.
- [ ] Migración de datos: crear workspace `legacy-<timestamp>` y asignar materiales huérfanos.
- [ ] Test de migración: aplicar/revertir sin pérdida.

## 4. Backend — endpoints workspaces

- [ ] `POST /api/workspaces` (crea, devuelve slug).
- [ ] `GET /api/workspaces/{slug}` (metadatos; 404 si no existe).
- [ ] `PATCH /api/workspaces/{slug}` (edita `display_name`; validado por 0033 `no_personal_data`).
- [ ] Test contract: creación, obtención, actualización, 404, rechazo de PII en `display_name`.

## 5. Backend — refactor endpoints de materiales

- [ ] Mover todos los endpoints de materiales bajo el prefijo `/api/workspaces/{slug}/materials/...`:
  - `POST /api/workspaces/{slug}/materials/agendas` (y equivalentes por tipo).
  - `GET /api/workspaces/{slug}/materials?status=&q=&limit=&offset=`.
  - `GET /api/workspaces/{slug}/materials/{material_id}`.
  - `POST /api/workspaces/{slug}/materials/{material_id}/submit`.
  - `POST /api/workspaces/{slug}/materials/{material_id}/review`.
  - `POST /api/workspaces/{slug}/materials/{material_id}/validate` (integración con 0033).
  - `GET /api/workspaces/{slug}/materials/{material_id}/audit`.
  - `GET /api/workspaces/{slug}/materials/{material_id}/export/manifest` (integración con 0032).
  - `GET /api/workspaces/{slug}/materials/{material_id}/export`.
- [ ] Retirar endpoints legacy `/api/materials/*` (actualizar tests y consumidores).
- [ ] Validar en cada endpoint que el material pertenece al workspace del slug → 404 si no coincide.
- [ ] Extender `MaterialListResult` con `total`, `limit`, `offset`, `workspace`.
- [ ] Test contract: happy path, 404, cruzado (material de otro workspace), paginación, filtros.

## 6. Backend — persistencia y despliegue

- [ ] Marcar `DATABASE_URL` como obligatorio; el arranque de `api` falla sin él.
- [ ] Actualizar `docker-compose.yml`: servicio `api` con `DATABASE_URL` apuntando a Postgres.
- [ ] Health check `GET /api/health` verifica conexión Postgres; 503 si falla.
- [ ] Fallback in-memory solo vía dependency override en tests.

## 7. Backend — seguridad y auditoría

- [ ] Registrar creación de workspace en audit log (sin PII).
- [ ] Registrar accesos a materiales por slug (para futura 0021).
- [ ] Rate limiting básico en `POST /api/workspaces` para evitar creación masiva de slugs.
- [ ] Nunca revelar existencia cruzada: 404, nunca 403 ni 401 en MVP.

## 8. Frontend — rutas y contexto

- [ ] Nueva ruta `apps/web/src/app/page.tsx` (welcome screen; ya no redirige al constructor).
- [ ] Rutas `apps/web/src/app/w/[slug]/mis-materiales/page.tsx`, `apps/web/src/app/w/[slug]/nuevo/page.tsx`, `apps/web/src/app/w/[slug]/material/[materialId]/page.tsx`.
- [ ] Ruta 404 accesible con CTA "Volver a inicio" para slugs inválidos.
- [ ] `apps/web/src/features/workspaces/workspace-context.tsx` (provider deriva de `useParams`; sin persistencia).

## 9. Frontend — welcome + creación de workspace

- [ ] `apps/web/src/features/workspaces/welcome-page.tsx` con dos acciones claras.
- [ ] `apps/web/src/features/workspaces/create-workspace-form.tsx` (opcional `display_name`).
- [ ] `apps/web/src/features/workspaces/open-workspace-form.tsx` (acepta slug o URL completa).
- [ ] `apps/web/src/features/workspaces/workspace-created-dialog.tsx`: enlace, botón copiar, botón descargar `.txt`, checkbox obligatorio "He guardado mi enlace".
- [ ] `apps/web/src/features/workspaces/api.ts` — cliente para endpoints de workspaces.

## 10. Frontend — header y navegación del workspace

- [ ] `apps/web/src/features/workspaces/workspace-header.tsx`: muestra slug + `display_name`, botón "Copiar enlace" con `aria-live` para feedback.
- [ ] Integrar `workspace-header` en el shell Convergencia Serena bajo `/w/[slug]/*`.
- [ ] Enlaces del shell ("Mis materiales", "Nuevo") respetan el slug actual.

## 11. Frontend — bandeja "Mis materiales"

- [ ] Refactor `apps/web/src/features/materials-inbox/` para consumir `GET /api/workspaces/{slug}/materials`.
- [ ] `api.ts` — cliente parametrizado por slug (obtenido de contexto/router, nunca cliente-local).
- [ ] `use-materials-inbox.ts` — hook: estado, fetch, paginación, debouncing búsqueda (250 ms).
- [ ] `inbox-page.tsx`, `inbox-filters.tsx`, `inbox-list.tsx`, `inbox-item.tsx`.
- [ ] Estados vacíos honestos: sin materiales / sin resultados con CTAs.

## 12. Frontend — constructor cableado al workspace

- [ ] Ruta `/w/[slug]/nuevo` monta el constructor y crea materiales vía `POST /api/workspaces/{slug}/materials/...`.
- [ ] Ruta `/w/[slug]/material/[materialId]` monta el constructor cargando vía `GET /api/workspaces/{slug}/materials/{materialId}`.
- [ ] Modo lectura si `status == approved`, salvo subpasos de descarga (integrar con 0032).
- [ ] Modo edición si `status ∈ {draft, rejected}`.
- [ ] 404 accesible si el material no existe o no pertenece al workspace.

## 13. Frontend — eliminación de client-storage residual

- [ ] Auditar `apps/web/src/` y eliminar cualquier uso de `localStorage`, `sessionStorage`, IndexedDB para datos de negocio.
- [ ] Regla lint (custom o comentario) prohibiendo `localStorage` en carpetas `features/` de materiales.
- [ ] Test unitario de humo: buscar en el bundle referencias a `arasaac:recent-*` (no deben existir).

## 14. Accesibilidad

- [ ] Welcome screen: `h1` único, foco al primer control, dos acciones claras.
- [ ] `WorkspaceCreatedDialog`: focus trap, escape solo tras confirmar checkbox, `aria-live="assertive"` para "No se puede recuperar".
- [ ] `fieldset` + `legend` en filtros de bandeja.
- [ ] Estado del material con texto + icono textual, nunca color solo.
- [ ] Paginación `<nav>` etiquetado.
- [ ] Foco al primer resultado tras aplicar filtros.
- [ ] Slug visible en header con botón copiar (`aria-label`, feedback `aria-live`).
- [ ] axe-core sin violaciones en welcome, dialog de creación, bandeja vacía, bandeja con resultados, bandeja sin resultados.

## 15. Contratos visuales (Convergencia Serena)

- [ ] Añadir/actualizar contratos en `apps/web/src/design-system/component-contracts/` para: `WelcomeScreen`, `WorkspaceCreatedDialog`, `WorkspaceHeader`, `InboxPage` (variantes).
- [ ] Snapshots visuales Playwright.

## 16. Docker Compose y despliegue

- [ ] `docker-compose.yml`: servicio `api` con `DATABASE_URL` obligatorio.
- [ ] Servicio `postgres` con volumen persistente.
- [ ] Servicio `api` corre migraciones Alembic al arrancar.
- [ ] `docs/deployment/docker-compose.md` actualizado.

## 17. Tests e2e

- [ ] Playwright: crear workspace → guardar enlace → cerrar navegador → reabrir enlace → bandeja vacía → crear material → aparece.
- [ ] Playwright: abrir el mismo slug en incógnito → mismos materiales.
- [ ] Playwright: deep-link a material inexistente → 404 accesible.
- [ ] Playwright: deep-link a material de otro workspace → 404 accesible.
- [ ] Playwright: slug inválido → 404 con CTA a inicio.
- [ ] Playwright: no queda `localStorage` de negocio tras crear/ver materiales (inspeccionar `page.evaluate`).
- [ ] Playwright: descarga del `.txt` con el enlace funciona.
- [ ] Contract tests backend: todos los endpoints con casos happy y 404.
- [ ] Test de persistencia real: reiniciar contenedor `api`, materiales siguen accesibles.

## 18. Documentación

- [ ] `docs/architecture/workspace-model.md` (nuevo) describiendo el modelo Workspace + slug.
- [ ] `apps/web/README.md`: welcome, creación de workspace, apertura, bandeja.
- [ ] `docs/deployment/docker-compose.md`: Postgres obligatorio.
- [ ] `docs/testing/test-plan-mvp0.md`: casos workspace.
- [ ] `docs/compliance/arasaac-license-policy.md`: revisar si el slug afecta atribución (no lo hace).
- [ ] Nota de usuario en welcome: "Guarda tu enlace. Si lo pierdes, perderás el acceso".

## 19. Coordinación con otras OpenSpecs

- [ ] 0032: confirmar que todos los endpoints de submit/review/export/manifest están bajo el prefijo workspace.
- [ ] 0033: confirmar que `POST /api/workspaces/{slug}/materials/{id}/validate` es la ruta oficial.
- [ ] 0035: notificar que "materiales recientes" consume `GET /api/workspaces/{slug}/materials?limit=3&sort=updated_at:desc` (sin hook local).

## 20. Validación final

- [ ] `make agent-packs-verify`.
- [ ] Lint/typecheck backend y frontend.
- [ ] Suite completa de tests + axe.
- [ ] Revisión por Product Owner Social + Security Agent + Architecture Reviewer antes de archivar.
