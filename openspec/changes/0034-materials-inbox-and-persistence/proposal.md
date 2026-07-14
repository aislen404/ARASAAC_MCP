# Proposal — 0034 Workspaces, Materials Inbox and Real Persistence

## Problema

Hoy los materiales existen solo en la sesión del constructor: si el usuario recarga el navegador o cambia de dispositivo, pierde el borrador. El backend expone `GET /api/materials` (listado) y `GET /api/materials/{id}` (detalle), pero:

- La Web App no consume esos endpoints ni ofrece bandeja alguna.
- Los materiales quedan en repositorio en memoria por defecto, sin Postgres activo.
- No existe forma de retomar un borrador, continuar una revisión pendiente, corregir un rechazado ni descargar un aprobado desde otra sesión o dispositivo.
- No hay separación entre creador y revisor de facto sin auth.

Consecuencias:

- El flujo de revisión (0032) queda encerrado en la misma sesión que la creación.
- La auditoría es invisible al usuario final, aunque el endpoint existe.
- El dashboard no puede mostrar información honesta sobre materiales pasados (dependencia con 0035).
- El MVP no es funcional en un escenario real: una educadora crea, otra revisa, un tercero descarga.

## Cambio propuesto

Introducir el concepto de **Workspace** como unidad de acceso y contenedor de materiales, con persistencia real en Postgres y **cero almacenamiento en cliente** para datos de materiales:

1. **Modelo Workspace** (nuevo recurso backend):
   - Un workspace agrupa materiales. `workspace 1..n material`.
   - Se identifica por un `slug` **legible generado** por el servidor (ej. `zorro-alegre-piedra-lila`) que sirve como token de acceso.
   - Sin identidad personal, sin cuentas: quien tenga el slug puede operar en ese workspace.
   - Sin roles internos en MVP: todos los actores con el slug tienen las mismas acciones (los roles llegan en 0021).

2. **Persistencia real 100% server-side**:
   - Postgres activo por defecto en `docker-compose.yml`.
   - Migraciones Alembic para `workspaces`, `materials`, `audit_events`, con `workspace_id` como FK en materiales y eventos.
   - Cero uso de `localStorage`, `sessionStorage` o cookies para datos de materiales.
   - La única "memoria" del cliente es la URL (`/w/<slug>/…`); si se pierde, se pierde el acceso (mitigado con página de custodia del enlace).

3. **Pantalla de bienvenida honesta**:
   - Al abrir la app sin slug, mostrar dos acciones:
     - **Crear nuevo workspace** → backend genera slug, redirige a `/w/<slug>/mis-materiales`.
     - **Abrir workspace existente** → input para pegar slug o URL completa.
   - No se generan workspaces automáticos por cada visita: solo por acción explícita.

4. **Bandeja "Mis materiales"** (`/w/<slug>/mis-materiales`):
   - Consume `GET /api/workspaces/{slug}/materials?status=…&q=…&limit=…&offset=…`.
   - Filtros por estado, búsqueda por título, paginación server-side.
   - Acciones por fila: Retomar, Ver auditoría (colapsable), Descargar (solo si aprobado).
   - Estados vacíos honestos con CTA claros.

5. **Deep-link controlado por backend**:
   - `/w/<slug>/material/<uuid>` carga el material vía `GET /api/workspaces/{slug}/materials/{id}`.
   - Backend valida que el material pertenece al workspace; 404 en caso contrario.
   - El cliente no decide qué materiales conoce; el backend decide.

6. **Custodia del slug**:
   - Página de bienvenida al crear un workspace: "Este es tu enlace de acceso. Guárdalo. No podrás recuperarlo si lo pierdes."
   - Botón "Descargar enlace como archivo `.txt`".
   - Botón "Copiar enlace".
   - Aviso persistente en el shell del workspace: "Workspace: `zorro-alegre-piedra-lila` · Copiar enlace".

## Fuera de alcance

- Autenticación real, cuentas de usuario, roles (queda para 0021 Keycloak).
- Recuperación de slugs perdidos (imposible por diseño; documentado como responsabilidad del usuario).
- Compartición granular de materiales individuales fuera del workspace.
- Colecciones/carpetas o etiquetado dentro del workspace.
- Búsqueda full-text avanzada o filtros por rango de fechas.
- Notificaciones fuera de la app (email, colas).
- Multi-workspace desde una misma URL (cada workspace vive en su slug).

## Valor

- Habilita el proceso completo real: crear → validar → revisar → aprobar → exportar, entre sesiones, dispositivos y personas distintas.
- Permite separar de facto creador/revisor compartiendo el slug, sin construir identidad personal (cumple regla absoluta #6).
- Persistencia real end-to-end sin almacenar datos en cliente (cumple regla #7).
- Base sólida para migrar a auth real (0021) sin reescribir el modelo de acceso.
- Un MVP demostrable en un despliegue real con múltiples usuarios simultáneos.

## Referencias

- Regla absoluta: `AGENTS.md` §2 #6, #7; §5 Definition of Done.
- Change previo: `openspec/changes/archive/0018-preferences-without-pii`.
- Change previo: `openspec/changes/archive/0016-review-workflow`.
- Dependencia inversa: `openspec/changes/0032-review-export-guided-flow`, `openspec/changes/0035-honest-workspace-metrics-v2`.
- Roadmap futuro: `openspec/changes/0021-keycloak-future-auth` (migración de slug → identidad real).
