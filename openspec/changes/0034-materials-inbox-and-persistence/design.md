# Design — 0034 Workspaces, Materials Inbox and Real Persistence

## Principio rector

**El workspace es la unidad de acceso; una persona no lo es.** Todo material vive dentro de un workspace, todo endpoint de materiales se gaitea por `workspace_slug`, y el cliente no almacena estado de negocio: solo interpreta URLs y renderiza respuestas del backend.

## Modelo de dominio

### Entidad `Workspace`

```python
class Workspace(BaseModel):
    workspace_id: UUID                 # identificador interno estable
    slug: str                          # legible generado, único, ej. "zorro-alegre-piedra-lila"
    display_name: str | None           # opcional, editable por el usuario (nunca PII)
    created_at: datetime
    updated_at: datetime
```

- `slug` cumple `^[a-z]+(-[a-z]+){2,4}$` (3–5 palabras separadas por guion).
- El slug es la clave pública compartible; el `workspace_id` (UUID) es interno.
- `display_name` opcional para diferenciar workspaces visualmente ("Aula 3B", "Centro de día"); no obligatorio, no valida contra PII pero pasa por el validador `no_personal_data` de 0033 al crearse.

### Relación con `Material`

- Añadir `workspace_id: UUID` como FK NOT NULL en `materials`.
- Todo material pertenece a exactamente un workspace.
- Todos los endpoints de materiales pasan a estar bajo el prefijo `/api/workspaces/{slug}/materials/...`.
- Los endpoints legacy `/api/materials/*` se retiran en esta change (ver sección "Compatibilidad").

### Generación de slugs

- Diccionario cerrado de 3 listas: `[animales, adjetivos, sustantivos_naturaleza]` con ~150 palabras cada una en español, sin acentos, sin nombres propios, sin PII.
- Slug = `animal-adjetivo-sustantivo` + sufijo `adjetivo` opcional si hay colisión (`zorro-alegre-piedra-lila`).
- Espacio de nombres > 150³ = 3.4M combinaciones base; suficientemente único para MVP con retry en colisión.
- Generación server-side, nunca client-side.

## Persistencia

### Migraciones Alembic

Nueva revisión que:

1. Crea tabla `workspaces (workspace_id UUID PK, slug TEXT UNIQUE NOT NULL, display_name TEXT NULL, created_at TIMESTAMPTZ, updated_at TIMESTAMPTZ)`.
2. Añade columna `workspace_id UUID NOT NULL REFERENCES workspaces(workspace_id)` a `materials`.
3. Añade columna `workspace_id UUID NOT NULL REFERENCES workspaces(workspace_id)` a `audit_events`.
4. Índices: `materials(workspace_id, status)`, `materials(workspace_id, updated_at)`, `audit_events(workspace_id, created_at)`.
5. Migración de datos existentes: crear un workspace `legacy-<timestamp>` y asignar todos los materiales huérfanos a él (log del slug generado).

### Configuración

- `DATABASE_URL` obligatorio en `docker-compose.yml` para el servicio `api`.
- Fallback a repositorio en memoria **solo en tests unitarios** vía dependency override; el arranque del contenedor `api` **falla** si `DATABASE_URL` no apunta a Postgres real.
- Health check `GET /api/health` verifica conexión Postgres y responde 503 si falla.

## Endpoints

### Workspaces

- `POST /api/workspaces` → crea workspace, devuelve `{workspace_id, slug, display_name, created_at}`. Sin body obligatorio; `display_name` opcional.
- `GET /api/workspaces/{slug}` → metadatos del workspace. 404 si no existe.
- `PATCH /api/workspaces/{slug}` → actualiza `display_name` (validado por 0033).

### Materiales dentro de workspace

- `POST /api/workspaces/{slug}/materials/agendas` (y equivalentes por tipo) → crear material en ese workspace.
- `GET /api/workspaces/{slug}/materials?status=…&q=…&limit=…&offset=…` → listado paginado.
- `GET /api/workspaces/{slug}/materials/{material_id}` → detalle.
- `POST /api/workspaces/{slug}/materials/{material_id}/submit`
- `POST /api/workspaces/{slug}/materials/{material_id}/review`
- `POST /api/workspaces/{slug}/materials/{material_id}/validate` (integración con 0033)
- `GET /api/workspaces/{slug}/materials/{material_id}/audit`
- `GET /api/workspaces/{slug}/materials/{material_id}/export/manifest?formats=…` (integración con 0032)
- `GET /api/workspaces/{slug}/materials/{material_id}/export?format=…`

Backend valida en cada endpoint que el material pertenece al workspace del slug; 404 si no coincide (nunca revelar existencia cruzada).

### Contratos de respuesta

- `MaterialListResult` extendida: `{materials: Material[], total: int, limit: int, offset: int, workspace: WorkspaceSummary}`.
- `MaterialResult` puede incluir `workspace_slug` para conveniencia del frontend.

## Compatibilidad

- Los endpoints antiguos `/api/materials/*` **se retiran** en esta change (no hay usuarios externos ya que la Web App no los consume aún de forma persistente). Los tests existentes se actualizan al nuevo prefijo.
- Los materiales creados antes de esta change en memoria se pierden al reiniciar (comportamiento actual); no requiere migración.
- Los materiales que ya estén persistidos en Postgres (si los hubiera en algún entorno) se agrupan bajo un workspace `legacy-*` vía migración de datos.

## Frontend

### Rutas Next.js (App Router)

- `/` → **pantalla de bienvenida** con dos acciones: "Crear workspace" y "Abrir workspace existente".
- `/w/[slug]/mis-materiales` → bandeja del workspace.
- `/w/[slug]/nuevo` → constructor para crear nuevo material en el workspace.
- `/w/[slug]/material/[materialId]` → constructor cargando material existente.
- `/w/[slug]/settings` → editar `display_name` (opcional en MVP).
- Cualquier ruta con slug inválido → 404 accesible con CTA "Volver a inicio".

### Componentes clave

- `apps/web/src/features/workspaces/`:
  - `api.ts` — cliente para `POST /api/workspaces`, `GET /api/workspaces/{slug}`.
  - `welcome-page.tsx` — pantalla de bienvenida (crear u abrir).
  - `workspace-header.tsx` — muestra slug, `display_name`, botón "Copiar enlace".
  - `workspace-created-dialog.tsx` — modal/pantalla al crear workspace con: enlace copiable, botón "Descargar enlace `.txt`", checkbox "He guardado mi enlace" antes de continuar.
  - `workspace-context.tsx` — provider React que expone el workspace actual (slug, id, display_name) obtenido del router; no persiste nada.
- `apps/web/src/features/materials-inbox/` refactorizado para consumir endpoints con slug del contexto.

### Flujo de creación de workspace

1. Usuario en `/` pulsa "Crear workspace" (opcional: `display_name`).
2. `POST /api/workspaces` → respuesta con slug.
3. Frontend muestra `WorkspaceCreatedDialog` con el enlace `https://…/w/<slug>/mis-materiales`, botón copiar, botón descargar `.txt`, checkbox obligatorio "He guardado mi enlace".
4. Al confirmar, navega a `/w/<slug>/mis-materiales`.

### Flujo de apertura de workspace

1. Usuario en `/` pulsa "Abrir workspace existente".
2. Input aceptando: slug (`zorro-alegre-piedra-lila`) o URL completa (`https://…/w/zorro-alegre-piedra-lila/…`).
3. Frontend extrae slug, llama `GET /api/workspaces/{slug}`; si 200 → navega, si 404 → mensaje accesible "Este enlace no existe o ha sido eliminado. Verifica el enlace."

### Cero almacenamiento cliente

- **Prohibido** `localStorage`, `sessionStorage`, IndexedDB para datos de materiales o workspace.
- Cookies solo si son necesarias para preferencias UI intrascendentes (tema, idioma), nunca para datos de negocio.
- El `WorkspaceContext` deriva del `useParams()` de Next.js; no cachea entre navegaciones fuera de `/w/[slug]`.

### Deep-link a material

- `/w/<slug>/material/<uuid>` monta el constructor y carga vía `GET /api/workspaces/{slug}/materials/{uuid}`.
- Backend responde 404 si el material no pertenece al workspace (nunca 403 para no revelar existencia).
- Modo lectura si `status == approved` salvo subpasos de descarga.

### Auditoría visible

- Cada fila de bandeja ofrece `<details>` con últimos 5 eventos fetched de `GET /api/workspaces/{slug}/materials/{id}/audit`.
- Se reutiliza el componente timeline definido en 0032 subpaso 3.5.

## Accesibilidad

- Pantalla de bienvenida: dos acciones claras, `h1` único, foco al primer control.
- `WorkspaceCreatedDialog`: focus trap correcto, escape cierra tras confirmar checkbox, `aria-live="assertive"` para el mensaje "Este enlace no se puede recuperar".
- Filtros como `fieldset` + `legend`.
- Estado del material comunicado con texto + icono textual, nunca solo color.
- Paginación con `<nav aria-label="…">` y `<button aria-label="…">`.
- Foco al primer resultado tras aplicar filtros.
- Slug del workspace siempre visible en el header con botón "Copiar enlace" (`aria-label`, `aria-live` para feedback de copia).

## Testing

- Tests unitarios: generador de slugs (unicidad, formato, no colisiones), validación de acceso por workspace.
- Contract tests: todos los endpoints con `workspace_slug` (happy path, 404, cruzado, paginación, filtros).
- Test e2e Playwright:
  1. Crear workspace → guardar enlace → cerrar navegador → reabrir enlace → llega a la bandeja vacía → crear material → aparece en bandeja.
  2. Compartir enlace en otra sesión (navegador incógnito) → misma bandeja accesible.
  3. Deep-link a material inexistente en el workspace → 404 accesible.
  4. Deep-link a material de otro workspace → 404 accesible (nunca 403).
  5. Slug inválido → 404 accesible con CTA a inicio.
- Tests axe en welcome, dialog de creación, bandeja (vacía / con resultados / sin resultados).
- Test de seguridad: intento de listar materiales sin slug o con slug malformado → 400/404.
- Test de persistencia: reiniciar contenedor `api` sin perder materiales (verificación Postgres).

## Alternativas descartadas

- **`localStorage` para IDs recientes** (versión anterior de esta OpenSpec): descartado explícitamente. No es persistencia real.
- **Cookies de sesión anónima**: funcionalmente similar a `localStorage`, no compartible con revisor, se pierde con limpieza del navegador.
- **Bandeja global sin identificador**: expone todos los materiales del servidor a cualquier visitante.
- **Auth real en MVP**: fuera de alcance por AGENTS.md; llegará con 0021.
- **UUID opaco como slug**: descartado por confirmación PO; los slugs legibles son más humanos y compartibles verbalmente.

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| Usuario pierde el slug y pierde acceso. | Pantalla explícita al crear con checkbox obligatorio, botón descargar `.txt`, aviso persistente. Documentar en docs de usuario. |
| Slug filtrado (compartido públicamente) expone el workspace. | Documentar responsabilidad del usuario; futura 0021 introducirá auth y podrá revocar. Log de accesos server-side para trazabilidad. |
| Colisión de slugs. | Retry con sufijo adicional; monitorizar tasa de colisión. |
| Migración Alembic rompe datos existentes. | Migración crea workspace `legacy-<timestamp>` y asigna materiales huérfanos; se registra el slug generado. |
| Alguien abre el enlace en un dispositivo público. | Mismo modelo que URLs compartidas; documentar en la página de bienvenida. |
| Crecimiento no acotado de workspaces vacíos. | Job de mantenimiento futuro (fuera de MVP): eliminar workspaces sin materiales tras N días. |
| Cambio de contrato REST rompe MCP u otros clientes. | Actualizar 0004-mcp-server-core si corresponde y ajustar tests contract. Auditar consumidores antes de la retirada. |

## Decisiones tomadas (confirmadas PO 2026-07-14)

- Modelo de acceso: **Workspace por slug compartible** (P1a).
- Creación: **pantalla de bienvenida con crear/abrir** (P2a2).
- Roles internos: **sin roles en MVP**; todos con el slug pueden todo (P3).
- Formato de slug: **legible generado** tipo `zorro-alegre-piedra-lila`.
- Almacenamiento cliente: **cero uso de `localStorage`/`sessionStorage`/IndexedDB** para datos de materiales.
- Persistencia: **Postgres obligatorio en runtime**; memoria solo en tests.
