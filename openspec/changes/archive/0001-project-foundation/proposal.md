# Proposal — 0001-project-foundation

## Problema

El repositorio contiene documentación de planificación, pero no una base ejecutable
para desarrollar y validar la plataforma de forma incremental.

## Solución propuesta

Crear el fundamento técnico mínimo del MVP-0:

- API FastAPI con healthcheck.
- interfaz Next.js con una pantalla estática de estado;
- placeholder MCP sin tools ni capacidades de ejecución;
- orquestación local con Docker Compose;
- pruebas smoke y comandos de calidad;
- documentación de arranque local.

## Alcance

Esta unidad solo establece estructura, contratos de salud y tooling. No procesa
pictogramas, materiales, exportaciones, identidades ni datos personales.

## Fuera de alcance

- Integración o consultas a ARASAAC.
- Generación, edición o exportación de materiales.
- Autenticación, persistencia y perfiles.
- Tools MCP, ejecución arbitraria o acceso genérico a red o filesystem.

## Riesgos y mitigaciones

- **Deriva de alcance:** los servicios solo publican estado y healthchecks.
- **Placeholder MCP interpretado como funcional:** responde con una allowlist vacía.
- **Dependencias inconsistentes:** se definen versiones y comandos reproducibles.
- **Accesibilidad insuficiente:** la pantalla usa HTML semántico, foco visible y
  contraste legible como línea base.

## Métrica de éxito

Los tres servicios se pueden iniciar localmente, los healthchecks responden, la
pantalla de estado se renderiza y los smoke tests pasan sin secretos, PII,
pictogramas ni llamadas externas.
