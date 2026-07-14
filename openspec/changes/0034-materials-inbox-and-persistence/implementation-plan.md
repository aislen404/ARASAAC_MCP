## Plan: Cierre integral OpenSpec 0034

Cerrar `0034-materials-inbox-and-persistence` en un único round completando backend, frontend, persistencia real, contratos visuales/e2e, documentación y validación final. El enfoque recomendado es: primero consolidar backend y runtime Postgres como fuente de verdad, después cablear frontend completo por slug sin storage cliente, y finalmente ejecutar verificación integral + cierre OpenSpec. Se retiran los endpoints legacy `/api/materials/*` en este round. Se incluye `/w/[slug]/settings`.

**Steps**
1. **Fase 1 — Auditoría de gap exacto contra spec.** Revisar `openspec/changes/0034-materials-inbox-and-persistence/spec.md` y contrastar cada MUST con el estado actual de backend, frontend, Docker, docs y tests. Generar checklist ejecutable y marcar como bloqueantes: runtime Postgres, retirada legacy, manifest endpoint, auditoría de accesos, zero client-storage, welcome flow, settings UI, e2e persistencia. Esto bloquea el resto.
2. **Fase 2 — Consolidación backend de persistencia real.** Completar `services/api/alembic/versions/0002_workspaces.py` y `services/api/src/arasaac_platform/repositories/sql.py` para alinear esquema/consultas con la spec: validar FKs, índices, backfill `legacy-*`, listado por `workspace_id`, filtros `status` CSV, `q` case-insensitive y paginación con `1 <= limit <= 100`, `offset >= 0`. Añadir verificación real de arranque sin `DATABASE_URL` en `services/api/src/arasaac_platform/main.py` y dependencia estricta en `services/api/src/arasaac_platform/api/materials.py`. *Bloquea Fases 3–7.*
3. **Fase 2.1 — Seguridad y gobernanza backend.** En `services/api/src/arasaac_platform/api/materials.py` registrar creación de workspace y accesos a materiales sin PII; mantener 404 en acceso cruzado; añadir rate limiting básico a `POST /api/workspaces` si el proyecto ya tiene patrón reutilizable, o dejarlo como middleware mínimo si no existe patrón. Añadir `GET /api/workspaces/{slug}/materials/{material_id}/export/manifest` si todavía no existe, reusando el flujo de export/manifiesto de `0032`. *Depende de 2.*
4. **Fase 2.2 — Retirada de legacy backend.** Buscar y eliminar rutas `/api/materials/*` residuales, referencias de tests y consumidores internos. Verificar compatibilidad explícita con la ruta oficial de validación `POST /api/workspaces/{slug}/materials/{material_id}/validate` definida en `0033`. *Depende de 2.*
5. **Fase 2.3 — Pruebas backend completas.** Extender tests en `services/api/tests/` para migración apply/downgrade, contrato workspaces, límites de paginación, filtro `q`, filtro `status`, acceso cruzado, rechazo PII en `display_name`, manifest endpoint, health 503, arranque sin `DATABASE_URL`, persistencia tras reinicio con Postgres. Incluir test explícito de migración de datos legacy. *Depende de 2–4; puede correr en paralelo con Fase 3 cuando backend esté estable.*
6. **Fase 3 — Descubrimiento de frontend existente y reutilización.** Localizar componentes y flujos existentes en `apps/web/src/app/`, `apps/web/src/features/materials-inbox/`, shell Convergencia Serena y contratos visuales para reutilizar patrones de routing, fetch, empty states y axe/playwright ya presentes. Identificar dónde vive hoy el constructor y qué componentes deben quedar parametrizados por slug. *Puede empezar cuando backend de rutas esté definido, paralelo con 5.*
7. **Fase 4 — Routing frontend y contexto de workspace.** Implementar `/`, `/w/[slug]/mis-materiales`, `/w/[slug]/nuevo`, `/w/[slug]/material/[materialId]` y `/w/[slug]/settings` en `apps/web/src/app/**`. Crear `apps/web/src/features/workspaces/workspace-context.tsx` derivando slug de router, sin `localStorage` ni cookies de negocio. Añadir 404 accesible con CTA “Volver a inicio” para slug/material inexistente. *Depende de 3.*
8. **Fase 4.1 — Welcome, apertura y custodia del enlace.** Implementar `apps/web/src/features/workspaces/welcome-page.tsx`, `create-workspace-form.tsx`, `open-workspace-form.tsx`, `workspace-created-dialog.tsx`, `workspace-header.tsx` y `api.ts`. Soportar apertura por slug o URL completa; tras creación, mostrar enlace, copiar, descargar `.txt`, checkbox obligatorio y advertencia `aria-live="assertive"`. Integrar header persistente con slug + botón copiar en el shell bajo `/w/[slug]/*`. *Depende de 7.*
9. **Fase 4.2 — Bandeja y constructor cableados a workspace.** Refactorizar `apps/web/src/features/materials-inbox/` para usar `GET /api/workspaces/{slug}/materials`, server-side pagination, filtros `fieldset/legend`, debounce 250 ms y estados vacíos honestos. Conectar constructor en `/w/[slug]/nuevo` y `/w/[slug]/material/[materialId]` a los endpoints workspace-scoped; modo lectura para `approved`, modo edición para `draft/rejected`, y descarga solo si procede. *Depende de 7 y 8.*
10. **Fase 4.3 — Eliminación de storage cliente residual.** Auditar `apps/web/src/**` para eliminar `localStorage`, `sessionStorage` e IndexedDB de datos de negocio; añadir protección por lint o test de humo para ausencia de claves `arasaac:recent-*`. *Depende de 7–9.*
11. **Fase 5 — Accesibilidad y contratos visuales.** Añadir o actualizar contratos en `apps/web/src/design-system/component-contracts/` para `WelcomeScreen`, `WorkspaceCreatedDialog`, `WorkspaceHeader`, `InboxPage` y `SettingsPage`. Cubrir foco inicial, `aria-live`, navegación por teclado, `h1` único, `<nav aria-label>`, estado no dependiente de color. Añadir validaciones axe y snapshots visuales Playwright. *Depende de 8–10.*
12. **Fase 6 — Docker Compose y runtime real.** Actualizar `docker-compose.yml` para Postgres persistente, `DATABASE_URL` obligatorio en `api`, y migraciones Alembic al arranque. Confirmar que `make start` o el comando de despliegue del repo levanta API con Postgres real y falla si falta configuración. *Puede avanzar en paralelo con Fases 4–5 tras backend estable; bloquea validación final.*
13. **Fase 7 — E2E y persistencia cross-session.** Implementar escenarios Playwright en `apps/web/tests/` o la carpeta usada por el proyecto: crear workspace, guardar enlace, reabrir en otra sesión/incógnito, bandeja vacía, crear material, deep-link válido, deep-link cruzado 404, slug inválido 404, descarga `.txt`, ausencia de storage local, persistencia tras reinicio del contenedor `api`. *Depende de 6 y del frontend funcional.*
14. **Fase 8 — Documentación y coordinación OpenSpec.** Actualizar `docs/architecture/workspace-model.md` (nuevo), `apps/web/README.md`, `docs/deployment/docker-compose.md`, `docs/testing/test-plan-mvp0.md` y referencias de coordinación con `0032`, `0033`, `0035`. Documentar explícitamente que el enlace no se puede recuperar si se pierde y que Postgres es obligatorio. *Depende de 2–7; puede ejecutarse en paralelo al final.*
15. **Fase 9 — Validación final y cierre.** Ejecutar backend/frontend lint, typecheck, tests unitarios/integración/e2e, axe, verificación de migración upgrade/downgrade, validación con Docker Compose real, y `make agent-packs-verify`. Luego actualizar `openspec/changes/0034-materials-inbox-and-persistence/tasks.md` con estado real y dejar lista la change para archivado. *Bloquea cierre de spec.*

**Relevant files**
- `openspec/changes/0034-materials-inbox-and-persistence/spec.md` — fuente de verdad de MUST/SHOULD a cerrar.
- `openspec/changes/0034-materials-inbox-and-persistence/tasks.md` — checklist OpenSpec a sincronizar al final.
- `services/api/alembic/versions/0002_workspaces.py` — migración crítica de workspaces, FKs, índices y backfill legacy.
- `services/api/src/arasaac_platform/repositories/sql.py` — persistencia SQL real y filtros workspace-aware.
- `services/api/src/arasaac_platform/repositories/memory.py` — paridad de comportamiento para tests.
- `services/api/src/arasaac_platform/api/materials.py` — endpoints de workspaces/materiales, 404 cruzado, manifest, validación y auditoría.
- `services/api/src/arasaac_platform/main.py` — arranque/health con `DATABASE_URL` obligatorio.
- `services/api/tests/` — contract tests, repositorio, migración y persistencia.
- `apps/web/src/app/**` — rutas welcome y workspace-scoped.
- `apps/web/src/features/workspaces/**` — nuevo flujo de creación/apertura/custodia/settings.
- `apps/web/src/features/materials-inbox/**` — bandeja parametrizada por slug.
- `apps/web/src/design-system/component-contracts/**` — contratos visuales a ampliar.
- `apps/web/tests/**` — Playwright y checks de accesibilidad/zero storage.
- `docker-compose.yml` — Postgres persistente y runtime obligatorio.
- `docs/architecture/workspace-model.md` — nueva documentación de arquitectura.
- `docs/deployment/docker-compose.md` — despliegue con Postgres real.
- `docs/testing/test-plan-mvp0.md` — casos workspace.

**Verification**
1. Verificar matriz MUST de `spec.md` contra implementación final sin huecos abiertos.
2. Ejecutar tests backend de dominio/API/repositorio/migración con `.venv/bin/pytest` en `services/api` incluyendo casos de Postgres real cuando exista fixture o contenedor.
3. Ejecutar lint/typecheck backend según scripts del repo y confirmar ausencia de errores.
4. Ejecutar tests frontend unitarios/contract y Playwright para welcome, settings, inbox, deep-links, 404, zero client-storage y descarga `.txt`.
5. Ejecutar pruebas axe sobre welcome, diálogo, bandeja vacía/con resultados/sin resultados, header y settings.
6. Levantar `docker-compose.yml`, comprobar migración automática, `GET /api/health`=200 con DB operativa y 503 cuando DB no responde.
7. Reiniciar el servicio `api` con Postgres persistente y verificar que workspace/materiales siguen accesibles.
8. Confirmar que no quedan referencias activas a `/api/materials/*` ni a claves `arasaac:recent-*` en frontend/backend/tests.
9. Ejecutar `make agent-packs-verify` y actualizar `tasks.md` antes del archivado.

**Decisions**
- Se cierra `0034` completa en este round: backend, frontend, Docker, docs, tests y cierre OpenSpec.
- Los endpoints legacy `/api/materials/*` se retiran ya para cumplir la spec.
- Se incluye `/w/[slug]/settings` en este round aunque sea SHOULD, para evitar dejar la UX de `display_name` incompleta.
- El orden recomendado prioriza primero fuente de verdad backend/runtime y después UX/e2e, para evitar retrabajo de contratos.

**Further Considerations**
1. El punto de mayor riesgo es la alineación entre índices/consultas SQL y el modelo actual basado en `payload`; conviene resolver cualquier duplicidad de columnas (`status`, `updated_at`) antes de tocar más frontend.
2. Si no existe aún patrón de rate limiting en el repo, implementar uno mínimo y acotado a `POST /api/workspaces`.
3. `GET /export/manifest` debe reutilizar la lógica existente de `0032`, no crear otro contrato paralelo.
