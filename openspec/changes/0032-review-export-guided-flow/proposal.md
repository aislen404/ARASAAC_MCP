# Proposal — 0032 Review & Export Guided Flow

## Problema

El Paso 3 "Revisión y exportación" del constructor de materiales se presenta hoy como un bloque de botones aislados (`Enviar a revisión`, `Aprobar`, `Rechazar`, `Exportar HTML/PDF/DOCX/PPTX/ZIP`) sin narrativa, sin subpasos, sin checklist verificable y sin retroalimentación sobre lo que ocurre entre transiciones.

Consecuencias:

- El usuario no comprende qué constituye "revisión humana" y puede aprobar con un clic, violando la intención de la regla absoluta #5.
- No hay separación visible entre validar, revisar, empaquetar y descargar.
- Los formatos de exportación se ofrecen todos a la vez sin permitir elegir un paquete ni ver el manifiesto que se descargará.
- El estado del material solo aparece como texto plano ("Estado: Sin borrador"), sin progreso ni siguiente acción explícita.
- No hay historial visible de las transiciones (creado → enviado → revisado → exportado), pese a existir el endpoint `/audit`.

## Cambio propuesto

Reestructurar el Paso 3 como un **stepper interno accesible** de cinco subpasos secuenciales, cada uno con estado propio, condiciones de avance explícitas y feedback vía `aria-live`:

1. **3.1 Validación previa** — ejecutar validadores (cambio 0033) y mostrar hallazgos bloqueantes/advertencias antes de permitir avanzar.
2. **3.2 Enviar a revisión** — botón activo solo si 3.1 no tiene bloqueantes; transición a `in_review`.
3. **3.3 Revisión humana** — checklist explícita firmada por la persona revisora, nota obligatoria, decisión aprobar/rechazar.
4. **3.4 Preparar exportación** — vista previa del manifiesto (atribución, IDs ARASAAC, versión), selección de formatos, sin descargar aún.
5. **3.5 Descarga y auditoría** — botón único de descarga por paquete, timeline visible con eventos de auditoría del material.

El backend ya expone `POST /submit`, `POST /review`, `GET /export`, `GET /audit`, `GET /` (list). Esta propuesta es principalmente frontend + cableado, con dos ajustes menores de contrato para exponer manifiesto sin descarga y ejecutar validación previa (delegada a 0033).

## Fuera de alcance

- Autenticación o roles reales (queda para 0021 Keycloak futuro).
- Persistencia y bandeja de materiales (cubierto por 0034).
- Motor de validadores en sí mismo (cubierto por 0033).
- Rediseño de las cards del dashboard (cubierto por 0035).
- Nuevos formatos de exportación o modificación de plantillas.
- Notificaciones fuera de la sesión (email, colas, etc.).

## Valor

- Convierte la revisión humana en un proceso verificable, no en un botón, alineándose con la regla absoluta #5.
- Reduce el riesgo de exportaciones no atribuidas o con hallazgos pendientes.
- Aporta trazabilidad visible al usuario final (no solo en logs backend).
- Prepara la superficie UX para roles y bandeja (0034) sin bloquear su implementación.

## Referencias

- Regla absoluta: `AGENTS.md` §2, especialmente #5, #6, #7, #9.
- Change previo: `openspec/changes/archive/0016-review-workflow` (backend workflow).
- Change previo: `openspec/changes/archive/0012-export-engine` (motor de export).
- Change previo: `openspec/changes/0027-frontend-shell-honest-state` (métricas honestas).
- Dependencia inmediata: `openspec/changes/0033-material-validation-panel` (validadores).
