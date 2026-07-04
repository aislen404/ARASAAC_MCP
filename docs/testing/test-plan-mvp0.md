# Plan de pruebas — MVP gobernado con asistente IA

## 1. Objetivo

Validar una demo reproducible que combina planificación IA textual, pictogramas
reales ARASAAC, edición, revisión humana, exportación atribuida y trazabilidad sin
PII, diagnóstico, generación de imágenes ni ejecución arbitraria.

## 2. Alcance

Incluye Web Next.js, API FastAPI, conector ARASAAC, proveedor IA opcional,
materiales, revisión, exportación HTML/PDF, persistencia, auditoría, MCP allowlisted
y Docker Compose. La llamada real a ARASAAC es opt-in; proveedores IA se prueban
mediante dobles y contrato, porque CI no recibe secretos.

Excluye autenticación, perfiles, vinculación a personas, datos sensibles,
diagnóstico, generación/modificación de pictogramas y nuevas tools MCP.

## 3. Estrategia y gates

| Nivel | Herramienta | Propósito | Gate |
| --- | --- | --- | --- |
| Unitario/contrato Python | Pytest + pytest-cov | API, IA, dominio, export, DB y MCP | ≥75% total |
| Unitario frontend | Vitest + V8 | estados y flujos React | ≥75% en cada métrica |
| Integración | Pytest + HTTPX | proveedor, ARASAAC y repositorios | obligatorio |
| E2E | Playwright Chromium | flujos manual e IA | todos pasan |
| Accesibilidad | axe + Playwright | WCAG A/AA y teclado | sin serious/critical |
| Calidad | Ruff, ESLint, mypy, TypeScript | análisis estático | sin errores |
| Supply chain | npm audit + build | vulnerabilidades y compilación | sin vulnerabilidades conocidas |

La cobertura no sustituye casos de gobernanza. Python y frontend aplican umbrales
independientes.

## 4. Entorno

- Python 3.11+, Node.js 20+, npm y Chromium Playwright.
- Docker Compose v2 solo para la validación de despliegue.
- Puertos E2E dedicados: 3100, 8100 y 8101.
- `AI_PROVIDER=disabled` en CI.
- `OPENAI_API_KEY` solo para smoke manual de proveedor real; nunca en fixtures.

## 5. Matriz de casos

| ID | Área | Caso | Resultado esperado |
| --- | --- | --- | --- |
| WEB-001 | Web | Abrir `/` | HTTP 200 y flujo completo |
| WEB-002 | Semántica | Estructura | `lang=es`, un `main`, un `h1` |
| WEB-003 | Responsive | 375×667 | Sin scroll horizontal |
| WEB-004 | Teclado | Recorrer controles | Sin trampas y foco visible |
| A11Y-001 | WCAG | Axe A/AA | Sin violaciones serious/critical |
| API-001 | API | `GET /health` | Contrato exacto y 200 |
| API-002 | API | Métodos/rutas inválidos | 405/404 sin efectos |
| AI-001 | Estado | IA desactivada | API sana, `available=false` |
| AI-002 | Estado | IA configurada | Proveedor/modelo, nunca clave |
| AI-003 | Input | Campos extra | 422 por schema cerrado |
| AI-004 | Privacidad | Email/teléfono/DNI/URL | 422 antes del proveedor |
| AI-005 | Uso | Lenguaje diagnóstico | 422 antes del proveedor |
| AI-006 | Confirmación | Falta confirmación literal | 422 |
| AI-007 | Provider | Structured output | Pydantic parse y `store=false` |
| AI-008 | Provider | Tools/imágenes | No se envían ni habilitan |
| AI-009 | Provider | Sin clave | 503 controlado; manual operativo |
| AI-010 | Provider | Timeout/fallo/refusal | 504/502 sin material |
| AI-011 | Output | Cantidad incorrecta | Rechazo antes de ARASAAC |
| AI-012 | Output | PII/diagnóstico devuelto | Rechazo por segunda validación |
| AI-013 | Resolución | Término válido | Tres candidatos ARASAAC como máximo |
| AI-014 | Decisión | Plan mostrado | Ningún elemento auto-seleccionado |
| AI-015 | Decisión | Botón elegir | Solo entonces llega al editor |
| AI-016 | Persistencia | Plan IA | Prompt/respuesta no se almacenan |
| PIC-001 | ARASAAC | Buscar | Referencias reales normalizadas |
| PIC-002 | ARASAAC | Obtener por ID | Metadatos y URL oficial |
| PIC-003 | ARASAAC | Fallo externo | 502 controlado |
| MAT-001 | Agenda | Crear borrador | Pasos ordenados y atribuidos |
| MAT-002 | Tablero | Crear borrador | Entre 2 y 24 celdas |
| MAT-003 | Editor | Editar/ordenar/eliminar | Vista previa consistente |
| REV-001 | Revisión | Enviar | `draft → in_review` |
| REV-002 | Revisión | Aprobar | Solo confirmación humana |
| REV-003 | Revisión | Rechazar/transición inválida | Estado gobernado/409 |
| EXP-001 | Export | Borrador | 409, ningún archivo |
| EXP-002 | Export | HTML aprobado | Atribución y escaping |
| EXP-003 | Export | PDF aprobado | Pictogramas reales y atribución |
| EXP-004 | Export | Manifiesto | IDs, licencia y revisión |
| AUD-001 | Auditoría | Lifecycle | Eventos append-only ordenados |
| DB-001 | Persistencia | Reinicio | Material/eventos sobreviven |
| DB-002 | Persistencia | Payload corrupto | Rechazado por Pydantic |
| MCP-001 | MCP | Allowlist | Solo tres tools aprobadas |
| MCP-002 | MCP | Schemas | Inputs/outputs cerrados |
| MCP-003 | MCP | Ejecución arbitraria | No existe shell/filesystem/eval |
| FND-001 | Fundación | Estructura | Archivos y comandos obligatorios |
| FND-002 | Secretos | Escaneo | Sin claves privadas o tokens |
| FND-003 | Assets | Repositorio | Sin imágenes de pictogramas |
| DEP-001 | Compose | `config --quiet` | Configuración válida |
| COV-001 | Cobertura | Python | Total ≥75% |
| COV-002 | Cobertura | Frontend | Lines/functions/branches/statements ≥75% |

## 6. Flujos E2E críticos

1. Manual: buscar → seleccionar → editar → crear → enviar → aprobar → exportar.
2. IA: confirmar privacidad → generar plan textual → verificar cero selección
   automática → elegir ARASAAC → editar.
3. Bloqueo: intentar exportar antes de aprobación.
4. Degradación: IA desactivada y flujo manual plenamente utilizable.
5. Accesibilidad: teclado, responsive y axe sobre la pantalla completa.

## 7. Comandos

```bash
make setup
make test
make lint
make typecheck
make openspec-verify
NEXT_TELEMETRY_DISABLED=1 npm --prefix apps/web run build
npm audit --prefix apps/web --audit-level=low
docker compose config --quiet
```

Contrato ARASAAC real opt-in:

```bash
ARASAAC_LIVE_TEST=1 .venv/bin/pytest \
  services/api/tests/test_arasaac_connector.py -m integration
```

## 8. Criterios de salida

- Todas las suites obligatorias pasan.
- Cobertura backend y frontend ≥75%.
- No hay secretos, PII, pictogramas locales ni endpoints de imagen IA.
- El plan IA no crea material y la exportación sigue bloqueada hasta aprobación.
- La atribución ARASAAC permanece visible.
- Cualquier limitación ambiental o smoke real no ejecutado queda registrada.

## 9. Riesgos

- CI no valida credenciales ni coste del proveedor real; usa dobles estructurales.
- ARASAAC y OpenAI son dependencias externas con latencia y disponibilidad.
- El guard regex reduce exposición evidente, pero no convierte texto libre en un
  canal apto para datos personales: la confirmación y formación siguen siendo
  controles obligatorios.
- En producción se requiere gestor de secretos, evaluación de privacidad,
  observabilidad sin contenido y revisión jurídica del proveedor.
