# Proposal — 0029 CI Quality Gate Repair

## Problema

El workflow GitHub Actions **Quality** falla de forma determinística en
`make agent-packs-verify` con `ModuleNotFoundError: No module named 'yaml'`
desde que se integró ese gate en `.github/workflows/quality.yml` (commit
`a23c84e`). El workflow `agent-packs.yml` instala `pyyaml` por separado, pero
Quality ejecuta `make setup` sin esa dependencia y los targets de packs usan
`python3` del sistema en lugar del venv del proyecto.

Además, los snapshots visuales de Playwright están versionados solo para macOS
(`*-chromium-darwin.png`), mientras CI corre en `ubuntu-latest` (Linux). Tras
corregir PyYAML, los tests visuales fallarán por snapshots inexistentes.

Por último, Quality no refleja la paridad completa de `make test-uat`
(falta `docker compose config` y `npm audit --audit-level=low`), no hay branch
protection en `main`, y las versiones de GitHub Actions emiten warnings de
deprecación Node 20.

## Cambio propuesto

1. Instalar `pyyaml` en `make setup` y ejecutar scripts de agent packs con
   `.venv/bin/python3`.
2. Alinear `quality.yml` con `make test-uat` (gates, timeout, cache Playwright).
3. Regenerar snapshots visuales en entorno Linux reproducible.
4. Unificar `agent-packs.yml` para reutilizar el mismo contrato de setup/verify.
5. Actualizar acciones de GitHub y documentar migración Node 24.
6. Configurar branch protection en `main` exigiendo Quality en verde.

## Fuera de alcance

- Nuevos workflows de despliegue o CD a producción.
- Cambios funcionales en Convergencia Serena o MaterialBuilder.
- Integración live ARASAAC/OpenAI en CI.

## Valor

CI vuelve a ser confiable como gate de merge, con paridad local/CI y snapshots
visuales reproducibles en el mismo SO que GitHub Actions.
