.PHONY: setup start stop dev-api dev-mcp dev-web test lint typecheck openspec-verify docker-up docker-down

setup:
	python3 -m venv .venv
	.venv/bin/pip install -e "services/api[dev]" -e "services/mcp[dev]"
	npm --prefix apps/web install

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
	.venv/bin/pytest services/api/tests services/mcp/tests tests/smoke
	npm --prefix apps/web run test

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

docker-up:
	$(MAKE) start

docker-down:
	$(MAKE) stop
