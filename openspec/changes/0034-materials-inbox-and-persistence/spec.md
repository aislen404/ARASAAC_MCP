# Spec — 0034 Workspaces, Materials Inbox and Real Persistence

## MUST

### Modelo Workspace

- MUST introducir entidad `Workspace` con `workspace_id: UUID`, `slug: str`, `display_name: str | None`, timestamps.
- MUST generar `slug` server-side con formato `^[a-z]+(-[a-z]+){2,4}$` a partir de diccionarios cerrados (animales, adjetivos, sustantivos_naturaleza) sin PII.
- MUST garantizar unicidad de `slug` con retry en colisión.
- MUST asociar cada `Material` y cada `AuditEvent` a exactamente un `Workspace` vía `workspace_id` FK NOT NULL.
- MUST validar `display_name` con el validador `no_personal_data` de 0033 al crear/actualizar.

### Persistencia real

- MUST persistir workspaces, materiales y eventos en Postgres en runtime.
- MUST fallar el arranque del servicio `api` si `DATABASE_URL` no está configurado (nunca fallback silencioso).
- MUST proveer migraciones Alembic idempotentes que añaden `workspaces` y `workspace_id` en `materials`/`audit_events`.
- MUST crear índices `materials(workspace_id, status)`, `materials(workspace_id, updated_at)`, `audit_events(workspace_id, created_at)`.
- MUST migrar materiales existentes (si los hay) a un workspace `legacy-<timestamp>`.
- MUST verificar la conexión Postgres en `GET /api/health` y responder 503 si falla.

### Endpoints backend

- MUST exponer `POST /api/workspaces` devolviendo `{workspace_id, slug, display_name, created_at}`.
- MUST exponer `GET /api/workspaces/{slug}` (200 con metadatos o 404).
- MUST exponer `PATCH /api/workspaces/{slug}` para actualizar `display_name` con validación `no_personal_data`.
- MUST mover todos los endpoints de materiales bajo el prefijo `/api/workspaces/{slug}/materials/...`.
- MUST validar en cada endpoint que el material pertenece al workspace del slug y responder 404 si no coincide (nunca 403).
- MUST aceptar `status` (CSV), `q`, `limit`, `offset` en `GET /api/workspaces/{slug}/materials`.
- MUST aplicar `1 <= limit <= 100`, `offset >= 0` (HTTP 422 si no cumple).
- MUST ejecutar `q` como substring case-insensitive contra `title`.
- MUST extender `MaterialListResult` con `total`, `limit`, `offset`, `workspace`.

### Frontend — rutas

- MUST proveer `/` como welcome screen con dos acciones: "Crear workspace" y "Abrir workspace existente".
- MUST proveer `/w/[slug]/mis-materiales`, `/w/[slug]/nuevo`, `/w/[slug]/material/[materialId]`.
- MUST mostrar 404 accesible con CTA "Volver a inicio" para slugs inválidos o materiales no encontrados.
- MUST NO redirigir automáticamente `/` a la creación de un workspace; la creación exige acción explícita.

### Frontend — creación de workspace y custodia del enlace

- MUST mostrar `WorkspaceCreatedDialog` tras `POST /api/workspaces` con: enlace copiable, botón "Copiar enlace", botón "Descargar enlace `.txt`", checkbox obligatorio "He guardado mi enlace".
- MUST impedir cerrar el diálogo hasta marcar el checkbox.
- MUST anunciar mediante `aria-live="assertive"` la advertencia "Este enlace no se puede recuperar si lo pierdes".
- MUST mostrar el slug del workspace de forma persistente en el header de `/w/[slug]/*` con botón "Copiar enlace".

### Frontend — apertura de workspace

- MUST aceptar en el formulario "Abrir workspace" tanto un slug puro como una URL completa.
- MUST extraer el slug, llamar `GET /api/workspaces/{slug}` y navegar a `/w/[slug]/mis-materiales` si 200.
- MUST mostrar mensaje accesible "Este enlace no existe o ha sido eliminado. Verifica el enlace." si 404.

### Frontend — bandeja

- MUST listar materiales del workspace vía `GET /api/workspaces/{slug}/materials`.
- MUST mostrar título, estado (texto + icono textual, nunca color solo), `updated_at` (relativo + absoluto en tooltip), acciones (Retomar, Ver auditoría, Descargar solo si `approved`).
- MUST ofrecer filtros por estado (`fieldset` + `legend`) y búsqueda por título (debounce 250 ms).
- MUST paginar server-side con controles en `<nav aria-label>`.
- MUST mostrar estados vacíos honestos con CTAs claros.

### Frontend — deep-link

- MUST cargar material vía `GET /api/workspaces/{slug}/materials/{materialId}` al montar `/w/[slug]/material/[materialId]`.
- MUST entrar en modo lectura si `status == approved` salvo subpasos 3.4/3.5 de descarga (0032).
- MUST permitir edición si `status ∈ {draft, rejected}`.
- MUST mostrar 404 accesible si el material no existe o pertenece a otro workspace (nunca 403).

### Cero almacenamiento cliente

- MUST NO usar `localStorage`, `sessionStorage` ni IndexedDB para datos de materiales, IDs recientes, slugs de workspaces distintos al actual, ni información de auditoría.
- MUST derivar el workspace actual del router (`useParams`) y de la respuesta backend, nunca de storage local.
- MUST NO usar cookies para persistir datos de negocio.

### Accesibilidad

- MUST cumplir WCAG 2.2 AA en welcome, dialog de creación, header de workspace, bandeja y detalle.
- MUST usar `h1` único por página y foco al primer control interactivo tras cambio de ruta.
- MUST usar `fieldset`+`legend` para filtros; `<nav aria-label>` para paginación.
- MUST comunicar estado con texto + icono textual, jamás color solo.
- MUST permitir navegación completa con teclado en dialog, filtros, lista, paginación, disclosures.
- MUST usar `aria-live` para feedback del botón "Copiar enlace" y para la advertencia de custodia.

### Gobernanza

- MUST NO introducir cuentas de usuario, sesiones o tokens en esta change.
- MUST NO revelar existencia cruzada de materiales entre workspaces (siempre 404, nunca 403 ni 401 en MVP).
- MUST NO exponer un listado global de workspaces del servidor.
- MUST NO permitir modificar materiales `approved` desde la bandeja.
- MUST registrar en audit log la creación de workspaces y accesos a materiales (sin PII, sin IPs, sin identidad personal).
- MUST mantener el backend como única fuente de verdad para transiciones de estado.

## SHOULD

- SHOULD documentar en la welcome screen que el enlace no se puede recuperar si se pierde.
- SHOULD ofrecer edición opcional del `display_name` en `/w/[slug]/settings`.
- SHOULD implementar rate limiting básico en `POST /api/workspaces` para evitar creación masiva.
- SHOULD prefetch de auditoría lazy solo al abrir el disclosure.
- SHOULD mantener el bundle libre de referencias a claves `arasaac:recent-*` u otras claves de storage de negocio.

## MUST NOT

- MUST NOT persistir PII vinculada a workspace o material.
- MUST NOT permitir slug generado client-side.
- MUST NOT permitir arranque de `api` sin Postgres real.
- MUST NOT retener endpoints legacy `/api/materials/*` tras esta change.
- MUST NOT persistir en cliente más allá de caché HTTP estándar y state React efimero.

## Escenarios verificables

1. **Creación de workspace**: en `/`, pulsar "Crear workspace" → `POST /api/workspaces` → diálogo con slug legible → marcar checkbox → navegar a `/w/<slug>/mis-materiales` (bandeja vacía).
2. **Custodia del enlace**: sin marcar el checkbox, el botón "Ir a mi workspace" está deshabilitado con `aria-disabled` y motivo textual.
3. **Descarga del enlace**: pulsar "Descargar enlace `.txt`" produce un archivo con la URL completa del workspace.
4. **Apertura desde otra sesión**: pegar el slug en "Abrir workspace" en navegador incógnito → mismos materiales.
5. **Persistencia real**: reiniciar el contenedor `api` → los materiales del workspace siguen accesibles.
6. **Filtro y búsqueda**: filtro `approved` con `q=agenda` en un workspace con 5 borradores y 2 aprobados con "Agenda" → exactamente 2 resultados; `aria-pressed` refleja filtro.
7. **Paginación**: 45 materiales en el workspace, `limit=20` → 3 páginas navegables por teclado, `total=45` visible.
8. **Bandeja vacía**: workspace nuevo → mensaje "Aún no has creado ningún material" + CTA "Crear el primero" funcional.
9. **Deep-link válido**: navegar a `/w/<slug>/material/<uuid>` de un material del workspace → carga en el constructor.
10. **Deep-link cruzado**: navegar a `/w/<slugA>/material/<uuidDeSlugB>` → 404 accesible (nunca 403).
11. **Slug inválido**: navegar a `/w/no-existe/mis-materiales` → 404 accesible con CTA a inicio.
12. **Aprobado en deep-link**: constructor abre en modo lectura, subpasos de descarga siguen disponibles (0032).
13. **Sin storage cliente**: tras crear y ver materiales, `window.localStorage.length === 0` para claves de negocio; inspección confirma cero uso.
14. **Sin PII en display_name**: intento de `PATCH /api/workspaces/{slug}` con `display_name="Juan Pérez"` → rechazo con mensaje de 0033.
15. **Accesibilidad**: axe-core sin violaciones en welcome, diálogo de creación, bandeja vacía, bandeja con resultados, bandeja sin resultados, header de workspace.
