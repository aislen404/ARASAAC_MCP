MVP_OPENSPECS_ARCHIVED = 0001-project-foundation 0002-arasaac-license-governance \
	0003-arasaac-connector 0004-mcp-server-core 0005-pictogram-search-tools \
	0006-material-domain-model 0007-visual-agenda-generator \
	0008-communication-board-generator 0012-export-engine 0013-web-app-shell-aa \
	0014-guided-creation-flow 0015-preview-editor 0016-review-workflow \
	0017-audit-observability 0019-testing-quality-gates \
	0020-docker-compose-deployment 0021-governed-ai-assistant \
	0022-obsidian-knowledge-sync 0023-frontend-convergencia-serena

OBSIDIAN_VAULT_PATH ?= $(HOME)/Library/Mobile Documents/iCloud~md~obsidian/Documents/ARASAAC_Project

.PHONY: setup start stop reset-data dev-api dev-mcp mcp-stdio dev-web dev dev-db dev-db-migrate test test-unit test-e2e lint typecheck openspec-verify docker-up docker-down agent-packs-sync agent-packs-verify obsidian-sync obsidian-sync-check obsidian-hooks-install db-migrate db-upgrade

setup:
	python3 -m venv .venv
	.venv/bin/pip install -e "services/api[dev]" -e "services/mcp[dev]"
	npm --prefix apps/web install
	cd apps/web && npx playwright install chromium

start:
	@docker info >/dev/null 2>&1 || { echo "Error: Docker no está iniciado. Abre Docker Desktop y vuelve a ejecutar 'make start'."; exit 1; }
	docker compose up --build --detach
	@echo ""
	@echo "Demo MVP-0 iniciada:"
	@echo "  Web:             http://localhost:3000"
	@echo "  API healthcheck: http://localhost:8000/health"
	@echo "  Estado IA:       http://localhost:8000/api/ai/status"
	@echo "  MCP status HTTP: http://localhost:8001/mcp/status"
	@echo "  MCP stdio real:  make mcp-stdio"

stop:
	docker compose down --remove-orphans

reset-data:
	@echo "Eliminando contenedores y volumen PostgreSQL local..."
	docker compose down --volumes --remove-orphans

dev-api:
	@set -a; [ ! -f .env ] || . ./.env; set +a; \
		exec .venv/bin/uvicorn arasaac_platform.main:app --app-dir services/api/src --reload --port 8000

dev-mcp:
	.venv/bin/uvicorn safe_mcp.main:app --app-dir services/mcp/src --reload --port 8001

mcp-stdio:
	.venv/bin/arasaac-mcp

dev-web:
	npm --prefix apps/web run dev

test:
	$(MAKE) test-unit
	$(MAKE) test-e2e

test-unit:
	.venv/bin/pytest services/api/tests services/mcp/tests tests/smoke \
		--cov=arasaac_platform --cov=safe_mcp --cov-report=term-missing \
		--cov-report=xml:coverage/python.xml --cov-fail-under=75
	npm --prefix apps/web run test:coverage

test-e2e:
	npm --prefix apps/web run test:e2e

lint:
	.venv/bin/ruff check services tests scripts/sync_obsidian_vault.py
	npm --prefix apps/web run lint

typecheck:
	.venv/bin/mypy services/api/src services/mcp/src
	npm --prefix apps/web run typecheck

openspec-verify:
	@for change in $(MVP_OPENSPECS_ARCHIVED); do \
		test -s "openspec/changes/archive/$$change/proposal.md"; \
		test -s "openspec/changes/archive/$$change/design.md"; \
		test -s "openspec/changes/archive/$$change/tasks.md"; \
		test -s "openspec/changes/archive/$$change/spec.md"; \
	done
	@for dir in openspec/changes/*/; do \
		case "$$dir" in */archive/) continue;; esac; \
		test -s "$$dir/proposal.md"; \
		test -s "$$dir/design.md"; \
		test -s "$$dir/tasks.md"; \
		test -s "$$dir/spec.md"; \
	done
	@echo "OpenSpecs verificadas (archivo MVP + changes activas)."

agent-packs-sync:
	python3 scripts/sync_agent_packs.py

agent-packs-verify:
	python3 scripts/verify_agent_packs_sync.py

obsidian-sync:
	python3 scripts/sync_obsidian_vault.py --vault "$(OBSIDIAN_VAULT_PATH)"

obsidian-sync-check:
	python3 scripts/sync_obsidian_vault.py --vault "$(OBSIDIAN_VAULT_PATH)" --check

obsidian-hooks-install:
	git config core.hooksPath .githooks
	chmod +x .githooks/post-commit .githooks/post-merge
	@echo "Hooks Obsidian activados para este repositorio."

docker-up:
	$(MAKE) start

docker-down:
	$(MAKE) stop

dev-db:
	docker compose up db -d
	@echo "Esperando PostgreSQL..."
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		docker compose exec -T db pg_isready -U arasaac -d arasaac_mvp >/dev/null 2>&1 && break; \
		sleep 2; \
	done
	@echo "PostgreSQL listo en localhost:5433 (Docker; puerto 5433 evita conflicto con Postgres local)"
	@echo "Ejecuta: make db-migrate"

dev-db-migrate: dev-db db-migrate

dev:
	@echo "Flujo local: make dev-db-migrate && make dev-api && make dev-mcp && make dev-web"

db-migrate:
	@set -a; \
		if [ -f .env ]; then . ./.env; fi; \
		if [ -z "$$DATABASE_URL" ]; then \
			export DATABASE_URL="postgresql+psycopg://arasaac:local-development-only@localhost:5433/arasaac_mvp"; \
		fi; \
		set +a; \
		cd services/api && ../../.venv/bin/alembic -c alembic.ini upgrade head || { \
			echo ""; \
			echo "No se pudo migrar. Comprueba:"; \
			echo "  1) make dev-db (PostgreSQL Docker en :5433)"; \
			echo "  2) DATABASE_URL en .env apunta a localhost:5433 (ver .env.example)"; \
			echo "  3) Si las tablas ya existen sin Alembic: make reset-data && make dev-db-migrate"; \
			exit 1; \
		}

db-upgrade: db-migrate
