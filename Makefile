.PHONY: setup start stop dev-api dev-mcp dev-web test test-unit test-e2e lint typecheck openspec-verify docker-up docker-down agent-packs-sync agent-packs-verify

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
	@echo "  MCP placeholder: http://localhost:8001/mcp/status"

stop:
	docker compose down --remove-orphans

dev-api:
	.venv/bin/uvicorn arasaac_platform.main:app --app-dir services/api/src --reload --port 8000

dev-mcp:
	.venv/bin/uvicorn safe_mcp.main:app --app-dir services/mcp/src --reload --port 8001

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
	.venv/bin/ruff check services tests
	npm --prefix apps/web run lint

typecheck:
	.venv/bin/mypy services/api/src services/mcp/src
	npm --prefix apps/web run typecheck

openspec-verify:
	test -s openspec/changes/0001-project-foundation/proposal.md
	test -s openspec/changes/0001-project-foundation/design.md
	test -s openspec/changes/0001-project-foundation/tasks.md
	test -s openspec/changes/0001-project-foundation/spec.md

agent-packs-sync:
	python3 scripts/sync_agent_packs.py

agent-packs-verify:
	python3 scripts/verify_agent_packs_sync.py

docker-up:
	$(MAKE) start

docker-down:
	$(MAKE) stop
