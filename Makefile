# ═══════════════════════════════════════════════════════════════
# Dealix — Makefile
# الأوامر الشائعة
# ═══════════════════════════════════════════════════════════════

.PHONY: help install install-dev install-observability install-security install-evals install-docs \
        setup first-setup test test-unit test-integration \
        lint format type-check security security-smoke clean run demo cockpit doctor \
        docker-build docker-up docker-down docker-logs \
        pre-commit-install pre-commit-run db-init alembic-heads requirements \
        env-check openapi-export api-contract-check dependency-inventory release-manifest production-smoke prod-verify \
        v5-status v5-smoke v5-snapshot v5-diagnostic v5-verify v5-digest \
        v5-proof-pack v10-verify v10-reference \
        brand-system growth-system marketing-system product-distribution \
        policy-check agent-registry machine-registry eval-gate \
        prompt-safety ai-governance launch-readiness execution-launch-layer \
        market-attack-system scale-moat-system founder-management-system \
        hypergrowth-ceo-layer founder-ceo-hypergrowth-layer company-os everything

# Python binary (override with PYTHON=python3.12 make ...)
PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
OPENAPI_OUTPUT ?= docs/architecture/openapi.json
PRODUCTION_BASE_URL ?= https://api.dealix.me

help: ## Show this help
	@echo "🏢 Dealix — Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ── Environment setup ──────────────────────────────────────────
install: ## Install production dependencies
	$(PIP) install -e .

install-dev: ## Install dev dependencies (tests, lint, etc.)
	$(PIP) install -e ".[dev]"

install-observability: ## Install optional observability stack
	$(PIP) install -e ".[observability]"

install-security: ## Install optional security and supply-chain tooling
	$(PIP) install -e ".[security]"

install-evals: ## Install optional evaluation and analysis tooling
	$(PIP) install -e ".[evals]"

install-docs: ## Install optional documentation site tooling
	$(PIP) install -e ".[docs]"

setup: install-dev pre-commit-install ## One-time dev setup
	@test -f .env || (cp .env.example .env && echo "✅ Created .env from template — edit it now")

first-setup: ## Interactive onboarding — generates .env, installs hooks, smoke-tests api.main
	bash scripts/first_setup.sh

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

security: security-smoke ## Run security scans
	bandit -c pyproject.toml -r core auto_client_acquisition autonomous_growth integrations api
	detect-secrets scan --baseline .secrets.baseline || true

security-smoke: ## Run dependency-free repository security smoke checks
	$(PYTHON) scripts/security_smoke.py

env-check: ## Validate .env.example contract and duplicate keys
	$(PYTHON) scripts/check_env_contract.py

openapi-export: ## Export FastAPI OpenAPI schema (OPENAPI_OUTPUT=...)
	$(PYTHON) scripts/export_openapi.py --output $(OPENAPI_OUTPUT)

api-contract-check: ## Check OpenAPI contract for removed paths/methods
	$(PYTHON) scripts/check_openapi_contract.py

dependency-inventory: ## Export lightweight dependency inventory
	$(PYTHON) scripts/export_dependency_inventory.py

release-manifest: ## Export production release manifest
	$(PYTHON) scripts/export_release_manifest.py

production-smoke: ## Run production API smoke test (PRODUCTION_BASE_URL=...)
	$(PYTHON) scripts/dealix_smoke_test.py --base-url $(PRODUCTION_BASE_URL)

prod-verify: env-check security-smoke api-contract-check dependency-inventory release-manifest v5-verify ## Canonical production-readiness verification bundle
	@echo "✅ Dealix production verification bundle completed"

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

cockpit: ## Founder Daily Brief — single-screen status (composes Bottleneck Radar + Hard Gates + Service Catalog)
	$(PYTHON) scripts/dealix_founder_daily_brief.py

doctor: env-check alembic-heads security-smoke ## Health check — env contract + single alembic head + security smoke
	@echo "✅ Repo doctor passed — see docs/playbooks/FOUNDER_NEXT_STEPS.md for what to do today"

alembic-heads: ## Fail if alembic reports >1 migration head
	$(PYTHON) scripts/check_alembic_single_head.py

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

# ── Company OS gates ───────────────────────────────────────────
# Each target verifies one layer of the Dealix Company OS. All are
# read-only — none of them write to production or send anything.
# `make everything` runs the master orchestrator and prints a single
# PASS/FAIL summary across all layers.

brand-system: ## company-os: brand css, logos, brand components
	$(PYTHON) scripts/verify_brand_system.py

growth-system: ## company-os: growth docs (ICP, lead scoring, GTM)
	$(PYTHON) scripts/verify_growth_system.py

marketing-system: ## company-os: marketing copy guards (banned claims, draft gate)
	$(PYTHON) scripts/verify_marketing_system.py

product-distribution: ## company-os: offer ladder + productized services
	$(PYTHON) scripts/verify_product_distribution.py

policy-check: ## company-os: policies/dealix_control_policy.yaml schema + refs
	$(PYTHON) scripts/verify_policy_as_code.py

agent-registry: ## company-os: registries/agent_registry.yaml cross-check
	$(PYTHON) scripts/verify_agent_registry.py

machine-registry: ## company-os: registries/machine_registry.yaml cross-check
	$(PYTHON) scripts/verify_machine_registry.py

eval-gate: ## company-os: evals/gates/dealix_agent_eval_gate.yaml
	$(PYTHON) scripts/verify_eval_gate.py

prompt-safety: ## company-os: banned-claim scan + draft_gate exercise
	$(PYTHON) scripts/verify_prompt_output_quality.py

ai-governance: ## company-os: aggregate policy + registries + eval + prompt safety
	$(PYTHON) scripts/verify_ai_governance_system.py

launch-readiness: ## company-os: launch bundle + paid launch + workflow gates
	$(PYTHON) scripts/verify_launch_readiness.py

execution-launch-layer: ## company-os: launch + daily-revenue workflows
	$(PYTHON) scripts/verify_execution_launch_layer.py

market-attack-system: ## company-os: market / ICP / category docs
	$(PYTHON) scripts/verify_market_attack_system.py

scale-moat-system: ## company-os: moat + scale docs
	$(PYTHON) scripts/verify_scale_moat_system.py

founder-management-system: ## company-os: founder command center + KPIs
	$(PYTHON) scripts/verify_founder_management_system.py

hypergrowth-ceo-layer: ## company-os: CEO operating system + capital model
	$(PYTHON) scripts/verify_hypergrowth_ceo_layer.py

founder-ceo-hypergrowth-layer: ## company-os: aggregate founder + CEO + hypergrowth
	$(PYTHON) scripts/verify_founder_ceo_hypergrowth_layer.py

company-os: ## company-os: layer-level existence check
	$(PYTHON) scripts/verify_company_os.py

everything: ## company-os: MASTER GATE — runs all layer verifiers, prints unified PASS/FAIL
	$(PYTHON) scripts/verify_everything.py
