# Informe de ejecución — MVP gobernado con asistente IA

Fecha: 2026-07-04

## Resultado

**PASS con smoke real del proveedor pendiente** — La implementación, contratos,
gobernanza, calidad y flujo E2E pasan. No se ejecutó una llamada real a OpenAI
porque el entorno no contiene `OPENAI_API_KEY`; no se incorporó ningún secreto
para suplirla.

| Comprobación | Resultado |
| --- | --- |
| Pytest API, IA, MCP, SQL y smoke | 60 pasan, 1 live opt-in omitido |
| Contrato live ARASAAC | 1/1 pasa |
| Cobertura Python | 89,05% |
| Vitest frontend | 7/7 pasan |
| Cobertura frontend | 91,47% statements; 77,9% branches; 91,07% functions; 94,87% lines |
| Playwright Chromium | 13/13 flujos pasan |
| Axe WCAG A/AA | sin serious/critical |
| Ruff / ESLint | pasan |
| mypy / TypeScript | pasan |
| Next.js build | pasa |
| npm audit | 0 vulnerabilidades |
| OpenSpec | pasa, 17 cambios verificados |
| Docker Compose config | válida |
| Smoke OpenAI real | no ejecutado: falta secreto de runtime |

Los umbrales automáticos están configurados al 75% y todas las métricas los
superan.

## Capa IA verificada

- Estado seguro con proveedor disponible/no disponible.
- Schema cerrado para input, plan textual y candidatos.
- Confirmación explícita de escenario genérico.
- Bloqueo previo de email, teléfono, DNI/NIE, URL y lenguaje diagnóstico.
- Responses API mediante SDK oficial, structured output y `store=False`.
- Ausencia de tools, endpoints de imagen, URL de proveedor arbitraria y logs de
  contenido.
- Segunda validación de salida, cantidad exacta y timeout/fallos controlados.
- Resolución posterior de cada término contra ARASAAC.
- Cero auto-selección, creación, aprobación o exportación por IA.
- Degradación segura: el flujo manual permanece disponible sin clave.

## Flujos E2E cubiertos

- planificación IA simulada por contrato → cero elementos seleccionados → elección
  humana de candidato ARASAAC → editor;
- búsqueda manual → selección → creación → revisión → aprobación → exportación;
- tablero con mínimo de celdas;
- bloqueo de exportación previa a aprobación;
- estado IA desactivado sin afectar healthcheck;
- contratos API/MCP, responsive, semántica, teclado y axe.

## Revisión visual

La demo se inspeccionó en navegador a 2026-07-04. El asistente se distingue como
opcional, expone que no genera pictogramas ni decide por la persona, mantiene
atribución y presenta el flujo manual cuando el proveedor está desactivado.

## Riesgos y pendientes

- Antes de una presentación externa debe inyectarse una clave efímera mediante
  `.env` o gestor de secretos y ejecutar un smoke real sin PII.
- El guard local detecta patrones evidentes, no sustituye un proceso organizativo
  de privacidad ni autoriza introducir datos personales.
- La dependencia externa puede fallar o tener coste/latencia; el producto falla
  cerrado y conserva la ruta manual.
- FastAPI emite un aviso de deprecación entre TestClient y Starlette; no afecta a
  esta versión y debe revisarse al actualizar dependencias.
- El volumen local mostró latencia de filesystem en el primer arranque de
  herramientas; los timeouts E2E admiten hasta cinco minutos y las ejecuciones
  calientes completaron con normalidad.
