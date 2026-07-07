# Design — 0029 CI Quality Gate Repair

## Decisión 1: PyYAML en el venv del proyecto

`scripts/sync_agent_packs.py` y `verify_agent_packs_sync.py` requieren PyYAML.
Se instala en `make setup` junto a las dependencias dev de API/MCP:

```makefile
.venv/bin/pip install -e "services/api[dev]" -e "services/mcp[dev]" pyyaml
```

Los targets `agent-packs-sync` y `agent-packs-verify` usan `.venv/bin/python3`
para alinear local y CI.

## Decisión 2: Quality ejecuta `make test-uat`

Un único paso `make test-uat` sustituye los pasos individuales duplicados.
`test-uat` ya incluye lint, typecheck, tests, openspec, packs, build, audit y
`docker compose config --quiet`. `docker compose config` solo valida YAML y no
requiere daemon Docker activo.

## Decisión 3: Snapshots visuales en Linux

Los snapshots se regeneran con la imagen oficial Playwright `v1.61.1-jammy`
(misma versión que `apps/web/package.json`). Se commitean archivos
`*-chromium-linux.png` y se eliminan los `*-darwin.png` obsoletos.

Se documenta en `docs/testing/test-plan-mvp0.md` que los snapshots deben
generarse en Linux o contenedor Playwright oficial.

## Decisión 4: Cache de browsers Playwright

Tras `make setup`, se cachea `~/.cache/ms-playwright` con `actions/cache@v4`
usando hash de `apps/web/package-lock.json` como clave. Reduce tiempo de CI
en runs posteriores.

## Decisión 5: GitHub Actions y Node 24

Se actualiza a `actions/checkout@v4`, `actions/setup-python@v5`,
`actions/setup-node@v4` (versiones actuales estables). Los warnings de Node 20
son emitidos por el runner forzando Node 24; se documenta que la migración a
`@v5` de checkout/setup-node se hará cuando estén disponibles de forma estable.
No se usa `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION` salvo regresión.

## Decisión 6: Branch protection

`main` requiere el status check `test` (job de Quality) antes de merge.
Se configura con `gh api` tras el primer run verde para confirmar el nombre
exacto del contexto.

## Decisión 7: agent-packs.yml

Reutiliza `make setup` + `make agent-packs-verify` en lugar de `pip install
pyyaml` suelto en Python del sistema.
