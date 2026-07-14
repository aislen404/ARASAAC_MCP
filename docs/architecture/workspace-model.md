# Modelo Workspace

## Objetivo

La OpenSpec `0034-materials-inbox-and-persistence` introduce `Workspace` como
unidad mínima de custodia para materiales, auditoría y futuras validaciones por
ámbito. El MVP no usa cuentas, sesiones ni tokens: el acceso depende del enlace
`/w/<slug>`.

## Entidad

`Workspace` persiste en backend con:

- `workspace_id: UUID`
- `slug: string`
- `display_name: string | null`
- `created_at`
- `updated_at`

El `slug` se genera siempre en servidor con diccionarios cerrados y formato
legible `palabra-palabra-palabra...`. No se acepta slug client-side ni datos
personales en el generador.

## Relaciones

- Cada `Material` pertenece a un único `Workspace` vía `workspace_id`.
- Cada `AuditEvent` pertenece a un único `Workspace` vía `workspace_id`.
- La API responde `404` si un material no pertenece al slug solicitado.

Esto evita listados globales y oculta existencia cruzada entre workspaces.

## Rutas oficiales

- `POST /api/workspaces`
- `GET /api/workspaces/{slug}`
- `PATCH /api/workspaces/{slug}`
- `GET /api/workspaces/{slug}/materials`
- `GET /api/workspaces/{slug}/materials/{material_id}`
- `POST /api/workspaces/{slug}/materials/{material_id}/validate`
- resto de operaciones de submit/review/export bajo el mismo prefijo

Las rutas legacy `/api/materials/*` dejan de ser el contrato oficial.

## Custodia del enlace

El frontend obliga a una acción explícita:

1. crear workspace,
2. mostrar diálogo con enlace completo,
3. copiar o descargar `.txt`,
4. marcar confirmación,
5. entrar en `/w/<slug>/mis-materiales`.

Mensaje obligatorio para la persona usuaria:

> Guarda tu enlace. Si lo pierdes, perderás el acceso.

## Persistencia

Runtime usa PostgreSQL de forma obligatoria. `DATABASE_URL` no tiene fallback
silencioso. El repositorio in-memory queda reservado a tests con override de
dependencias.

La migración crea `workspaces`, añade `workspace_id` a `materials` y
`audit_events`, y migra datos previos a un workspace `legacy-<timestamp>`.

## Frontend

El workspace actual se deriva del router y de la respuesta backend. No se usa
`localStorage`, `sessionStorage`, IndexedDB ni cookies para persistir datos de
negocio del workspace o de materiales.

Rutas visibles:

- `/`
- `/w/[slug]/mis-materiales`
- `/w/[slug]/nuevo`
- `/w/[slug]/material/[materialId]`
- `/w/[slug]/settings`

## Accesibilidad

- `404` accesible con CTA `Volver a inicio`.
- Header con slug visible y botón `Copiar enlace`.
- Diálogo de creación con advertencia `aria-live`.
- Bandeja con filtros semánticos y paginación etiquetada.
- Material aprobado en modo lectura; descarga disponible sin reabrir edición.