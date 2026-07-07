# ADR-0003 — PostgreSQL + pgvector

## Decisión

Usar PostgreSQL con pgvector como base transaccional y vectorial open source y escalable.

## Consecuencias

- Simplifica operación frente a dos motores separados.
- Escala razonablemente para MVP y piloto.
- Puede migrarse a Qdrant si el volumen/vector search lo exige.
