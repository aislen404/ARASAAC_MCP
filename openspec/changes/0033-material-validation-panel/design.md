# Design — 0033 Material Validation Panel

## Principio rector

**Las reglas absolutas son ejecutables o no existen.** Todo gate del pipeline (revisión, exportación, dashboard) debe apoyarse en el mismo motor de validación, con la misma semántica de severidad.

## Modelo de dominio

```python
class Severity(str, Enum):
    BLOCKER = "blocker"
    WARNING = "warning"
    OK = "ok"

class ValidationFinding(BaseModel):
    validator_id: str        # ej. "pictogram_ids_real"
    severity: Severity
    title: str               # texto corto localizable
    detail: str              # explicación accionable
    subject: Literal["material", "item", "pictogram"] = "material"
    subject_ref: str | None = None  # id de item o pictograma cuando aplica

class ValidationReport(BaseModel):
    material_id: UUID
    material_version: int
    validators_run: list[str]
    findings: list[ValidationFinding]
    generated_at: datetime
    is_blocking: bool        # True si algún finding es BLOCKER
```

## Motor de validación

- Módulo `services/api/src/arasaac_platform/services/validation.py`.
- Registro de validadores como funciones puras `(material: Material, ctx: ValidationContext) -> Iterable[ValidationFinding]`.
- `ValidationContext` inyecta dependencias necesarias (repositorio de pictogramas ARASAAC, config de límites).
- Ejecución secuencial en MVP; futuro `asyncio.gather` para paralelizar.
- Composición: `run_validators(material, ctx, validators=DEFAULT_VALIDATORS)`.

## Validadores MVP

### 1. `pictogram_ids_real`
- Para cada `PictogramReference`, verifica que exista en el catálogo ARASAAC local (`services/api/src/arasaac_platform/arasaac/pictograms.py`).
- Fallback: si no está en caché local y `ARASAAC_ONLINE_LOOKUP=true`, consulta MCP; si no, degrada a `WARNING` y explica.
- Severidad: `BLOCKER` si el ID no existe; `WARNING` si no se pudo verificar.

### 2. `license_notice_visible`
- Verifica que `material.attribution_text` contenga "Sergio Palao", "ARASAAC", "Gobierno de Aragón" y "CC BY-NC-SA".
- Severidad: `BLOCKER`.

### 3. `no_personal_data`
- Aplica regex/heurísticas sobre todos los textos del material:
  - Emails (`\b[\w.+-]+@[\w-]+\.[\w.-]+\b`).
  - Teléfonos ES (regex específico).
  - DNI/NIE.
  - Direcciones postales simples (patrón "C/ ...", "Avda. ...").
  - Nombres propios (heurística: dos palabras capitalizadas seguidas fuera de inicio de frase) → `WARNING`.
- Severidad: `BLOCKER` para emails/teléfonos/DNI; `WARNING` para nombres propios.

### 4. `no_modified_pictograms`
- Verifica que `pictogram.source_url` coincida con el patrón oficial ARASAAC sin query params de transformación.
- Severidad: `BLOCKER`.

### 5. `non_commercial_context`
- Verifica que el material tenga un flag/campo `usage_context: non_commercial` (a añadir al modelo `Material` si no existe, con default `non_commercial`).
- Severidad: `BLOCKER`.

### 6. `visual_density`
- Límites por tipo (configurable, valores iniciales):
  - agenda: 1–12 pasos
  - board: 2–24 celdas
  - document: 1–20 secciones
  - story: 1–16 escenas
  - signage: 2–12 signos
- Severidad: `WARNING` si excede; hasta ahora el schema ya limita el máximo, pero podemos advertir cuando >80% del límite.

## Endpoint

```
POST /api/workspaces/{slug}/materials/{id}/validate
Response: ValidationReport
```

- Vive bajo el prefijo introducido por 0034; el material debe pertenecer al workspace del slug (404 si no coincide).
- No modifica el material.
- Idempotente.
- Registra un evento de auditoría `VALIDATED` con contador de findings por severidad.

Adicionalmente, esta change expone el validador `no_personal_data` como función reusable para validar el `display_name` de un workspace en 0034 (`PATCH /api/workspaces/{slug}`).

## Frontend

### Cliente

- `validateMaterial(id: string): Promise<ValidationReport>` en `features/material-builder/api.ts`.
- Cache local por versión de material (evita re-validar si `material.version` no cambió).

### Componente `ValidationPanel`

- Props: `report: ValidationReport | null`, `loading: boolean`, `onRevalidate: () => void`.
- Renderiza:
  - Resumen: X bloqueantes · Y advertencias · Z OK.
  - Lista `<ul>` con findings; cada `<li>` con badge textual (`BLOQUEA`, `AVISO`, `OK`), título y detalle.
  - Botón "Volver a validar".
- Accesibilidad:
  - Cada badge tiene texto visible además de color.
  - Contraste AA verificado.
  - Findings agrupados con `role="group"` y `aria-labelledby`.
  - Si `is_blocking`, el resumen usa `aria-live="assertive"`.

## Reutilización

- Subpaso 3.1 (change 0032) monta `ValidationPanel` con el report vinculado al material actual.
- Card "Validación de la colección" (change 0035) muestra un resumen compacto del último report; enlaza al panel completo.

## Testing

- Tests unitarios por validador con material canónico + variantes (con email, con pictograma desconocido, etc.).
- Contract test del endpoint: shape del `ValidationReport`, códigos HTTP, idempotencia.
- Tests de frontend: `ValidationPanel` con distintos reports; teclado + axe.
- Test e2e: crear material con email en un texto → validación bloquea → mensaje visible → editar y re-validar → pasa.

## Alternativas descartadas

- **Ejecutar validadores en cliente**: rompe la fuente única de verdad y dificulta auditar.
- **Motor de reglas configurable por YAML en MVP**: sobreingeniería; las reglas absolutas son fijas.
- **NLP avanzado para PII**: costo desproporcionado; heurísticas cubren MVP y se documentan como best-effort.

## Riesgos

| Riesgo | Mitigación |
|--------|-----------|
| Falsos positivos en `no_personal_data` (nombres propios comunes). | Severidad `WARNING` para nombres, `BLOCKER` solo para patrones inequívocos. |
| Costo de verificar IDs contra MCP en cada validación. | Caché local + versión de material; degradación a `WARNING`. |
| Ambigüedad sobre "contexto no comercial". | Campo explícito con default `non_commercial` y bloqueo si cambia. |
