# Proposal — 0006-material-domain-model

## Problema

Generadores, revisión, auditoría y exportación necesitan un contrato común que
impida PII y preserve la trazabilidad de cada pictograma.

## Solución

Crear modelos Pydantic estrictos para materiales, versiones, bloques,
pictogramas, revisiones y auditoría con estados explícitos.

## Alcance

- agendas visuales y tableros de comunicación;
- borradores versionados;
- referencias ARASAAC;
- estados draft, in_review, approved y rejected;
- eventos de auditoría sin identidad personal.

## Fuera de alcance

Persistencia SQL, API de generación, editor y exportación.
