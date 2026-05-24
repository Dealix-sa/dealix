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
        bootstrap-runtime brand-system growth-system marketing-system \
        product-distribution policy-check agent-registry machine-registry \
        eval-gate company-os everything ceo-daily-brief ceo-weekly-review \
        capital-allocation strategy-scorecard revenue-forecast \
        market-attack-system scale-moat-system founder-ceo-hypergrowth-layer \
        smoke-internal-api

# Python binary (override with PYTHON=python3.12 make ...)
PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

# Dealix Company OS — private-ops root.
# Honors the existing convention: /opt/dealix (override with PRIVATE_OPS=...).
PRIVATE_OPS ?= /opt/dealix

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

# ── Dealix Company OS ──────────────────────────────────────────
# Read-only verifiers + private-ops runtime + CEO report generators.
# Every target honors the 11 non-negotiables and Article 13 Build Order.

bootstrap-runtime: ## CompanyOS: scaffold private-ops dirs under $(PRIVATE_OPS)
	$(PYTHON) scripts/bootstrap_private_ops_runtime.py --private-ops $(PRIVATE_OPS)

policy-check: ## CompanyOS: verify the 11 policy invariants resolve
	$(PYTHON) scripts/verify_policy_as_code.py

agent-registry: ## CompanyOS: verify agent registry YAML mirrors canonical Python
	$(PYTHON) scripts/verify_agent_registry.py

machine-registry: ## CompanyOS: verify machine registry YAML mirrors canonical
	$(PYTHON) scripts/verify_machine_registry.py

eval-gate: ## CompanyOS: verify the agent eval gate references real eval files
	$(PYTHON) scripts/verify_eval_gate.py

brand-system: ## CompanyOS: verify brand tokens + founder shell are wired
	$(PYTHON) scripts/verify_brand_system.py

growth-system: ## CompanyOS: verify growth surface index exists
	$(PYTHON) scripts/verify_growth_system.py

marketing-system: ## CompanyOS: verify launch/marketing surface index exists
	$(PYTHON) scripts/verify_marketing_system.py

product-distribution: ## CompanyOS: verify customer_success surface index exists
	$(PYTHON) scripts/verify_product_distribution.py

market-attack-system: ## CompanyOS: verify market-attack templates exist + claim-clean
	$(PYTHON) scripts/verify_market_attack_system.py

scale-moat-system: ## CompanyOS: verify scale/moat surface index exists
	$(PYTHON) scripts/verify_scale_moat_system.py

founder-ceo-hypergrowth-layer: ## CompanyOS: verify founder console wiring end-to-end
	$(PYTHON) scripts/verify_founder_ceo_hypergrowth_layer.py

company-os: ## CompanyOS: run the meta verifier (all sub-verifiers)
	$(PYTHON) scripts/verify_company_os.py

everything: ## CompanyOS: master verifier — final judge for the whole surface
	$(PYTHON) scripts/verify_everything.py

ceo-daily-brief: ## CompanyOS: assemble CEO daily brief into $(PRIVATE_OPS)/founder/
	$(PYTHON) scripts/generate_ceo_daily_brief.py --private-ops $(PRIVATE_OPS)

ceo-weekly-review: ## CompanyOS: assemble CEO weekly review into $(PRIVATE_OPS)/founder/
	$(PYTHON) scripts/generate_ceo_weekly_review.py --private-ops $(PRIVATE_OPS)

capital-allocation: ## CompanyOS: assemble capital allocation report into $(PRIVATE_OPS)/founder/
	$(PYTHON) scripts/generate_capital_allocation_report.py --private-ops $(PRIVATE_OPS)

strategy-scorecard: ## CompanyOS: assemble strategy scorecard into $(PRIVATE_OPS)/founder/
	$(PYTHON) scripts/generate_strategy_scorecard.py --private-ops $(PRIVATE_OPS)

revenue-forecast: ## CompanyOS: assemble revenue forecast into $(PRIVATE_OPS)/founder/
	$(PYTHON) scripts/generate_revenue_forecast.py --private-ops $(PRIVATE_OPS)

smoke-internal-api: ## CompanyOS: smoke /api/v1/internal/founder-console/* endpoints
	$(PYTHON) scripts/smoke_internal_api.py
