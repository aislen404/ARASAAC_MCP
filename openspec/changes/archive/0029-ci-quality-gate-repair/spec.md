# Spec — 0029 CI Quality Gate Repair

## MUST

- MUST install PyYAML during `make setup` so `agent-packs-verify` works offline.
- MUST run agent-pack scripts with `.venv/bin/python3` (same interpreter as pytest/ruff).
- MUST pass `make agent-packs-verify` in GitHub Actions Quality without `ModuleNotFoundError`.
- MUST run the same gates in CI as `make test-uat` (lint, types, unit, e2e, openspec, packs, build, audit low, compose config).
- MUST provide Linux Playwright snapshots for Convergencia Serena visual tests.
- MUST pass visual regression tests on `ubuntu-latest`.
- MUST protect `main` requiring the Quality status check before merge.

## SHOULD

- SHOULD cache Playwright browsers in CI to reduce pipeline duration.
- SHOULD use a 30-minute timeout for the Quality job while E2E suite grows.
- SHOULD document Linux snapshot generation in the MVP-0 test plan.

## MUST NOT

- MUST NOT commit macOS-only snapshots as the sole reference for CI visual tests.
- MUST NOT install PyYAML only on system Python while other gates use the venv.
- MUST NOT merge to `main` while Quality is failing.
