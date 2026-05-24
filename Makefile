# ═══════════════════════════════════════════════════════════════
# AI Company Saudi — Makefile
# الأوامر الشائعة
# ═══════════════════════════════════════════════════════════════

.PHONY: help install install-dev setup test test-unit test-integration \
        lint format type-check security clean run demo \
        docker-build docker-up docker-down docker-logs \
        pre-commit-install pre-commit-run db-init requirements \
        v5-status v5-smoke v5-snapshot v5-diagnostic v5-verify v5-digest \
        v5-proof-pack v10-verify v10-reference

# Python binary (override with PYTHON=python3.12 make ...)
PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

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

# ── Dealix Company OS — 26 layers ──────────────────────────────
# Supreme + per-layer verifiers. Each verifier prints `<Name>: PASS|FAIL`
# and exits 0 on PASS. `make everything` aggregates all 26.

.PHONY: everything brand-system founder-console company-os capital-allocation \
        strategy-scorecard revenue-forecast launch-layer market-attack-system \
        scale-moat-system founder-ceo-hypergrowth-layer ai-governance \
        policy-check agent-registry machine-registry eval-gate \
        bootstrap-runtime worker-orchestrator customer-success \
        enterprise-sales legal-trust-security company-memory \
        smoke-internal-api ceo-daily-brief ceo-weekly-review \
        growth-system marketing-system product-distribution

everything: ## Dealix supreme verifier — runs all 26 layers
	$(PYTHON) scripts/verify_everything.py

brand-system: ## Dealix: Brand OS verifier
	$(PYTHON) scripts/verifiers/verify_brand_system.py

founder-console: ## Dealix: Founder Console verifier
	$(PYTHON) scripts/verifiers/verify_founder_console.py

company-os: ## Dealix: CEO OS + Founder Mgmt + Hypergrowth verifier
	$(PYTHON) scripts/verifiers/verify_company_os.py

capital-allocation: ## Dealix: Capital Allocation report + verifier
	$(PYTHON) scripts/generate_capital_allocation_report.py
	$(PYTHON) scripts/verifiers/verify_capital_allocation.py

strategy-scorecard: ## Dealix: Strategy Metrics scorecard + verifier
	$(PYTHON) scripts/generate_strategy_scorecard.py
	$(PYTHON) scripts/verifiers/verify_strategy_metrics.py

revenue-forecast: ## Dealix: Revenue Factory forecast + verifier
	$(PYTHON) scripts/generate_revenue_forecast.py
	$(PYTHON) scripts/verifiers/verify_revenue_factory.py

launch-layer: ## Dealix: Launch Layer verifier
	$(PYTHON) scripts/verifiers/verify_launch_layer.py

market-attack-system: ## Dealix: Market Attack System verifier
	$(PYTHON) scripts/verifiers/verify_market_attack_system.py

scale-moat-system: ## Dealix: Scale / Moat System verifier
	$(PYTHON) scripts/verifiers/verify_scale_moat_system.py

founder-ceo-hypergrowth-layer: ## Dealix: Hypergrowth CEO Layer verifier
	$(PYTHON) scripts/verifiers/verify_founder_ceo_hypergrowth_layer.py

ai-governance: ## Dealix: AI Governance verifier
	$(PYTHON) scripts/verifiers/verify_ai_governance.py

policy-check: ## Dealix: Policy-as-Code verifier
	$(PYTHON) scripts/verifiers/verify_policy_as_code.py

agent-registry: ## Dealix: Agent Registry verifier
	$(PYTHON) scripts/verifiers/verify_agent_registry.py

machine-registry: ## Dealix: Machine Registry verifier
	$(PYTHON) scripts/verifiers/verify_machine_registry.py

eval-gate: ## Dealix: Eval Gate verifier
	$(PYTHON) scripts/verifiers/verify_eval_gate.py

bootstrap-runtime: ## Dealix: Private Ops Runtime dry-run (use --apply on host)
	$(PYTHON) scripts/bootstrap_private_ops_runtime.py
	$(PYTHON) scripts/verifiers/verify_private_ops_runtime.py

worker-orchestrator: ## Dealix: Worker Orchestrator verifier
	$(PYTHON) scripts/verifiers/verify_worker_orchestrator.py

customer-success: ## Dealix: Customer Success verifier
	$(PYTHON) scripts/verifiers/verify_customer_success.py

enterprise-sales: ## Dealix: Enterprise Sales verifier
	$(PYTHON) scripts/verifiers/verify_enterprise_sales.py

legal-trust-security: ## Dealix: Legal / Trust / Security verifier
	$(PYTHON) scripts/verifiers/verify_legal_trust_security.py

company-memory: ## Dealix: Company Memory verifier
	$(PYTHON) scripts/verifiers/verify_company_memory.py

smoke-internal-api: ## Dealix: Internal API smoke test
	$(PYTHON) scripts/verifiers/smoke_internal_api.py

ceo-daily-brief: ## Dealix: generate today's CEO daily brief
	$(PYTHON) scripts/generate_ceo_daily_brief.py

ceo-weekly-review: ## Dealix: generate this week's CEO weekly review
	$(PYTHON) scripts/generate_ceo_weekly_review.py

# Aliases (legacy / convenience names from the founder master order)
growth-system: revenue-forecast ## Dealix: alias for revenue-forecast
marketing-system: market-attack-system ## Dealix: alias for market-attack-system
product-distribution: scale-moat-system ## Dealix: alias for scale-moat-system
