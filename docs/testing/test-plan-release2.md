# Plan de pruebas — Release 2

## Generadores

| ID | Tipo | Casos |
|----|------|-------|
| GEN-001 | Lectura fácil | Crear → revisar → exportar HTML/PDF/DOCX |
| GEN-002 | Historia social | Secuencia narrativa ≥1 escena |
| GEN-003 | Señalética | ≥2 señales, sin logo ARASAAC |
| GEN-004 | Preferencias sin PII | Plantillas genéricas |

## Exportación avanzada

- DOCX, PPTX y ZIP con manifiesto y atribución.
- Bloqueo 409 si material no está aprobado.

## Regresión MVP-0

Ejecutar `make test lint typecheck openspec-verify` antes de archivar changes Release 2.
