# Repo Skeleton — ARASAAC Social MCP Platform

```text
arasaac-social-mcp/
  README.md
  LICENSE.md
  NOTICE-ARASAAC.md
  AGENTS.md
  docker-compose.yml
  .env.example
  .gitignore
  Makefile

  openspec/
    project.md
    adr/
      ADR-0001-python-backend.md
      ADR-0002-nextjs-frontend.md
      ADR-0003-postgres-pgvector.md
      ADR-0004-license-by-design.md
      ADR-0005-human-review-by-design.md
    changes/
      0001-project-foundation/
      0002-arasaac-license-governance/
      0003-arasaac-connector/
      0004-mcp-server-core/
      0005-pictogram-search-tools/
      0006-material-domain-model/
      0007-visual-agenda-generator/
      0008-communication-board-generator/
      0009-accessible-document-generator/
      0010-social-story-generator/
      0011-signage-generator/
      0012-export-engine/
      0013-web-app-shell-aa/
      0014-guided-creation-flow/
      0015-preview-editor/
      0016-review-workflow/
      0017-audit-observability/
      0018-preferences-without-pii/
      0019-testing-quality-gates/
      0020-docker-compose-deployment/
      0021-keycloak-future-auth/
      0022-semantic-search-future/
      0023-multientity-future/
      0024-arasaac-validation-dossier/

  apps/
    web/
      package.json
      next.config.js
      src/
        app/
        components/
        features/
        lib/
        styles/
        tests/

  services/
    api/
      pyproject.toml
      src/arasaac_platform/
        main.py
        api/
        domain/
        services/
        repositories/
        schemas/
        mcp/
        arasaac/
        export/
        governance/
        audit/
      tests/
      alembic/

  packages/
    shared-contracts/
      schemas/
      openapi/
      mcp-tools/

  docs/
    architecture/
    deployment/
    user-manual/
    entity-manual/
    accessibility/
    compliance/
    arasaac-dossier/

  scripts/
    sync_arasaac_catalog.py
    export_material.py
    validate_license.py

  tests/
    e2e/
    accessibility/
    fixtures/
```

## Comandos esperados

```bash
make setup
make dev
make test
make lint
make typecheck
make accessibility-test
make openspec-verify
make docker-up
```

## Política de ramas

- `main`: estable.
- `develop`: integración.
- `feature/openspec-XXXX-name`: implementación por OpenSpec.
- `release/x.y.z`: preparación de piloto/release.

## Convención de commits

```text
feat(mcp): add search_pictograms tool
fix(license): enforce visible attribution before export
test(export): add pdf license notice checks
docs(openspec): add visual agenda spec
```
