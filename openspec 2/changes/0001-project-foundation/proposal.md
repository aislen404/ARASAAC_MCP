# Proposal — 0001-project-foundation

## Problema

Base del proyecto, repo skeleton, tooling y convenciones es necesario para cumplir el Plan Maestro y permitir una evolución trazable mediante OpenSpec y Codex.

## Solución propuesta

Crear estructura de repositorio, Makefile, Docker Compose inicial, CI básico y documentación raíz.

## Alcance

- Implementar la capacidad descrita.
- Añadir pruebas y documentación.
- Respetar licencia ARASAAC, revisión humana y no PII cuando aplique.

## Fuera de alcance

No implementa lógica ARASAAC ni generación.

## Riesgos

- Incumplimiento de licencia.
- Falta de trazabilidad.
- Complejidad excesiva.
- Pérdida de accesibilidad.

## Métrica de éxito

Repo arranca en local; make test/lint existen; README y AGENTS.md presentes.
