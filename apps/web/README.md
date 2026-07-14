# Web App ARASAAC Social MCP Platform

## Flujo Workspace

La raíz `/` ya no abre el constructor directamente. Ahora actúa como pantalla de
bienvenida para dos acciones explícitas:

- `Crear workspace`
- `Abrir workspace existente`

Mensaje de custodia obligatorio:

> Guarda tu enlace. Si lo pierdes, perderás el acceso.

## Rutas principales

- `/` — welcome screen
- `/w/[slug]/mis-materiales` — bandeja del workspace
- `/w/[slug]/nuevo` — constructor de nuevo material
- `/w/[slug]/material/[materialId]` — deep-link a material existente
- `/w/[slug]/settings` — edición opcional de nombre visible

## Crear workspace

1. Pulsar `Crear workspace`.
2. El backend llama a `POST /api/workspaces`.
3. Se muestra `WorkspaceCreatedDialog`.
4. La persona usuaria debe copiar o descargar el enlace y marcar
   `He guardado mi enlace`.
5. Solo entonces puede continuar al workspace.

## Abrir workspace

El formulario acepta:

- slug puro
- URL completa del workspace

Si el backend devuelve `404`, la interfaz muestra un mensaje accesible y no
revela más información.

## Bandeja de materiales

La bandeja consume `GET /api/workspaces/{slug}/materials` con:

- filtros por estado
- búsqueda por título con debounce
- paginación server-side
- estados vacíos honestos

Cada fila ofrece:

- `Retomar` o `Ver`
- `Ver auditoría`
- `Descargar` solo si el material está `approved`

## Deep-link

`/w/[slug]/material/[materialId]` carga desde backend. Si el material está:

- `draft` o `rejected`: edición permitida
- `approved`: modo lectura y exportación disponible

Si el material no existe o pertenece a otro workspace, la app muestra `404`
accesible con CTA a inicio.

## Restricciones

- No usar storage cliente para datos de negocio.
- No persistir slugs recientes.
- No introducir PII en `display_name`.
- No modificar pictogramas ARASAAC.

## Comandos

```bash
npm run lint
npm run typecheck
npm test
npm run test:e2e
```