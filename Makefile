# ──────────────────────────────────────────────────────────────────────────────
# FoyerGate — developer Makefile
#
# Common commands. Run `make help` to see what's available.
# ──────────────────────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help
.PHONY: help install lint format test test-cov up down logs clean docs docs-serve

# ── Variables ──────────────────────────────────────────────────────
COMPOSE_FILE := deploy/docker/compose.yaml
COMPOSE      := docker compose -f $(COMPOSE_FILE)

# ── Help ───────────────────────────────────────────────────────────
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ──────────────────────────────────────────────────────────
install: ## Install dependencies (uv)
	uv sync --all-extras

# ── Code quality ───────────────────────────────────────────────────
lint: ## Run linters (ruff + mypy)
	uv run ruff check .
	uv run mypy src

format: ## Format code (ruff)
	uv run ruff format .
	uv run ruff check --fix .

# ── Tests ──────────────────────────────────────────────────────────
test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage HTML report
	uv run pytest --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

# ── Local stack (Docker Compose) ───────────────────────────────────
up: ## Start the full stack (API, Postgres, Redis, MinIO, OPA)
	$(COMPOSE) up -d
	@echo ""
	@echo "  FoyerGate is starting up. Once healthy:"
	@echo "    API docs:      http://localhost:9876/docs"
	@echo "    MinIO console: http://localhost:9001  (foyergate / changeme-in-production)"
	@echo "    OPA:           http://localhost:8181"
	@echo ""

down: ## Stop and remove the local stack
	$(COMPOSE) down

logs: ## Tail logs from the local stack
	$(COMPOSE) logs -f

ps: ## Show running services
	$(COMPOSE) ps

# ── Documentation ──────────────────────────────────────────────────
docs: ## Build documentation (requires `uv sync --extra docs`)
	uv run mkdocs build

docs-serve: ## Serve docs locally with hot reload
	uv run mkdocs serve

# ── Housekeeping ───────────────────────────────────────────────────
clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
