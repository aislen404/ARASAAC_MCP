# Tasks — 0029 CI Quality Gate Repair

- [x] Redactar proposal, design, spec y tasks de OpenSpec 0029.
- [x] Instalar `pyyaml` en `make setup` y usar `.venv/bin/python3` en targets de packs.
- [x] Simplificar `agent-packs.yml` para reutilizar setup/verify del Makefile.
- [x] Alinear `quality.yml` con `make test-uat` (timeout 30, cache Playwright).
- [x] Regenerar snapshots visuales Linux y eliminar snapshots darwin obsoletos.
- [x] Documentar generación de snapshots en `docs/testing/test-plan-mvp0.md`.
- [x] Documentar gate canónico de packs en `docs/agents/multi-ide-agent-packs.md`.
- [x] Actualizar `docs/testing/test-report-mvp0.md` tras UAT/CI verde.
- [x] Configurar branch protection en `main`.
- [x] Archivar OpenSpec 0029 tras merge.
