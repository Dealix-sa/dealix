# ═══════════════════════════════════════════════════════════════
# AI Company Saudi — Makefile
# الأوامر الشائعة
# ═══════════════════════════════════════════════════════════════

.PHONY: help install install-dev setup test test-unit test-integration \
        lint format type-check security clean run demo \
        docker-build docker-up docker-down docker-logs \
        pre-commit-install pre-commit-run db-init requirements \
        v5-status v5-smoke v5-snapshot v5-diagnostic v5-verify v5-digest \
        v5-proof-pack v10-verify v10-reference \
        bootstrap-public bootstrap-private bootstrap-all \
        implementation-status market-evidence stoplight \
        day-start day-close week-close

# Python binary (override with PYTHON=python3.12 make ...)
PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

# Private ops directory (override with PRIVATE_OPS=/path make ...)
PRIVATE_OPS ?= ../dealix-ops-private

help: ## Show this help
	@echo "🏢 AI Company Saudi — Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ── Environment setup ──────────────────────────────────────────
install: ## Install production dependencies
	$(PIP) install -e .

install-dev: ## Install dev dependencies (tests, lint, etc.)
	$(PIP) install -e ".[dev]"

setup: install-dev pre-commit-install ## One-time dev setup
	@test -f .env || (cp .env.example .env && echo "✅ Created .env from template — edit it now")

requirements: ## Export requirements.txt from pyproject
	$(PIP) install pip-tools
	$(PIP) compile pyproject.toml -o requirements.txt
	$(PIP) compile --extra dev pyproject.toml -o requirements-dev.txt

# ── Quality ────────────────────────────────────────────────────
lint: ## Run ruff + black checks
	ruff check .
	black --check .

format: ## Auto-format with ruff + black
	ruff check --fix .
	black .

type-check: ## Run mypy
	mypy core auto_client_acquisition autonomous_growth integrations api

security: ## Run security scans
	bandit -c pyproject.toml -r core auto_client_acquisition autonomous_growth integrations api
	detect-secrets scan --baseline .secrets.baseline || true

# ── Tests ──────────────────────────────────────────────────────
test: ## Run full test suite with coverage
	pytest -v

test-unit: ## Unit tests only
	pytest -v -m "not integration" tests/unit

test-integration: ## Integration tests only
	pytest -v tests/integration

# ── Pre-commit ─────────────────────────────────────────────────
pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit on all files
	pre-commit run --all-files

# ── Run locally ────────────────────────────────────────────────
run: ## Run API server (dev mode, reload on changes)
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

demo: ## Run interactive CLI demo
	$(PYTHON) cli.py

# ── Database ───────────────────────────────────────────────────
db-init: ## Initialize database tables (dev only)
	$(PYTHON) -c "import asyncio; from db.session import init_db; asyncio.run(init_db())"

# ── Docker ─────────────────────────────────────────────────────
docker-build: ## Build Docker image
	docker build -t dealix:latest .

docker-up: ## Start full stack (app + postgres + redis + mongo)
	docker compose up -d --build

docker-down: ## Stop and remove containers
	docker compose down

docker-logs: ## Tail application logs
	docker compose logs -f app

# ── Cleanup ────────────────────────────────────────────────────
clean: ## Remove build artifacts, caches
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# ── v5 founder CLIs ────────────────────────────────────────────
# These wrap the read-only Dealix v5 founder tooling. Each is safe
# to run any time — none of them write to production or send anything.

v5-status: ## v5: bilingual local snapshot (services + reliability + live gates)
	$(PYTHON) scripts/dealix_status.py

v5-smoke: ## v5: cross-platform smoke test against a deploy (BASE_URL=...)
	$(PYTHON) scripts/dealix_smoke_test.py $(if $(BASE_URL),--base-url $(BASE_URL))

v5-snapshot: ## v5: write JSON audit snapshot to docs/snapshots/<today>.json
	$(PYTHON) scripts/dealix_snapshot.py

v5-diagnostic: ## v5: list available bundles for the Diagnostic generator
	$(PYTHON) scripts/dealix_diagnostic.py --list-bundles

v5-verify: ## v5: 22-point production verifier (set BASE_URL=...)
	bash scripts/post_redeploy_verify.sh

v5-digest: ## v5: print the daily founder digest markdown (no email)
	$(PYTHON) scripts/dealix_morning_digest.py --print

v5-proof-pack: ## v5: assemble bilingual Proof Pack from JSONL events (HANDLE=...)
	$(PYTHON) scripts/dealix_proof_pack.py --customer-handle $(HANDLE)

# ── v10 founder + reference library ────────────────────────────
# v10 = AI Business Operating System reference architecture.
# Each target is read-only diagnostics — never live actions.

v10-verify: ## v10: full master verification (reference + modules + safety + tests)
	bash scripts/v10_master_verify.sh

v10-reference: ## v10: show 70-tool reference library summary
	$(PYTHON) scripts/verify_reference_library_70.py

# ── Implementation Automation Pack ─────────────────────────────
# Bootstrap + sprint + stoplight + day/week loops. Honors the
# No More Systems Gate: nothing here sends external messages.

bootstrap-public: ## Bootstrap public Dealix OS scaffold (idempotent)
	$(PYTHON) scripts/bootstrap_dealix_os.py

bootstrap-private: ## Bootstrap private ops directory (PRIVATE_OPS=...)
	$(PYTHON) scripts/bootstrap_private_ops.py --private-ops $(PRIVATE_OPS)

bootstrap-all: ## Bootstrap both public scaffold and private ops
	$(PYTHON) scripts/bootstrap_dealix_os.py
	$(PYTHON) scripts/bootstrap_private_ops.py --private-ops $(PRIVATE_OPS)

implementation-status: ## Report implementation sprint completion
	$(PYTHON) scripts/implementation_sprint_status.py

market-evidence: ## Gate: market execution evidence must exist
	$(PYTHON) scripts/verify_market_execution_evidence.py --private-ops $(PRIVATE_OPS)

stoplight: ## Generate strategic stoplight report (red/yellow/green)
	$(PYTHON) scripts/generate_stoplight_report.py --private-ops $(PRIVATE_OPS)

day-start: ## CEO day-start loop: mission control + stoplight + revenue ops
	$(PYTHON) -m dealix_cli mission-control --private-ops $(PRIVATE_OPS)
	$(PYTHON) scripts/generate_stoplight_report.py --private-ops $(PRIVATE_OPS)
	$(PYTHON) -m dealix_cli revenue-ops --private-ops $(PRIVATE_OPS)

day-close: ## CEO day-close loop: advance + close-day + stoplight
	$(PYTHON) -m dealix_cli advance --private-ops $(PRIVATE_OPS)
	$(PYTHON) -m dealix_cli close-day --private-ops $(PRIVATE_OPS)
	$(PYTHON) scripts/generate_stoplight_report.py --private-ops $(PRIVATE_OPS)

week-close: ## CEO week-close loop: weekly + trust + finance + assurance + stoplight
	$(PYTHON) -m dealix_cli ceo-weekly --private-ops $(PRIVATE_OPS)
	$(PYTHON) -m dealix_cli weekly --private-ops $(PRIVATE_OPS)
	$(PYTHON) -m dealix_cli trust --private-ops $(PRIVATE_OPS)
	$(PYTHON) -m dealix_cli finance-v2 --private-ops $(PRIVATE_OPS)
	$(PYTHON) -m dealix_cli assurance --private-ops $(PRIVATE_OPS)
	$(PYTHON) scripts/generate_stoplight_report.py --private-ops $(PRIVATE_OPS)
