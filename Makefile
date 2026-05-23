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
        implementation-check security-check company-check \
        bootstrap-private mission-control ceo-action-queue control-tower \
        ceo-weekly weekly-close business-score assurance \
        revenue-ops delivery finance-full trust-full content \
        productization people partners

DEALIX_PRIVATE_ROOT ?= ../dealix-ops-private

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

# ── Dealix Implementation Sprint Pack ──────────────────────────
# Targets that operate the sprint pack. Most write to the private ops
# working tree at $(DEALIX_PRIVATE_ROOT). Public targets touch only the repo.

implementation-check: ## Run the full Implementation Sprint Pack verifier chain
	$(PYTHON) scripts/verify_implementation_sprint_pack.py
	$(PYTHON) scripts/verify_master_operating_blueprint.py
	$(PYTHON) scripts/verify_security_reliability_os.py
	$(PYTHON) scripts/verify_public_safety_v2.py
	$(PYTHON) scripts/verify_data_boundary.py
	$(PYTHON) scripts/verify_company_data_architecture.py
	$(PYTHON) scripts/verify_revenue_operations_playbook.py
	$(PYTHON) scripts/verify_delivery_client_success_os.py
	$(PYTHON) scripts/verify_finance_pricing_os.py
	$(PYTHON) scripts/verify_trust_ai_risk_os.py
	$(PYTHON) scripts/verify_brand_proof_content_os.py
	$(PYTHON) scripts/verify_productization_engineering_os.py
	$(PYTHON) scripts/verify_people_partner_os.py

security-check: ## Security + public safety + data boundary verifiers
	$(PYTHON) scripts/verify_security_reliability_os.py
	$(PYTHON) scripts/verify_public_safety_v2.py
	$(PYTHON) scripts/verify_data_boundary.py

company-check: ## Company data architecture + private data quality audit
	$(PYTHON) scripts/verify_company_data_architecture.py
	$(PYTHON) scripts/audit_private_data_quality.py --root $(DEALIX_PRIVATE_ROOT)

bootstrap-private: ## Bootstrap the dealix-ops-private/ working tree
	$(PYTHON) scripts/bootstrap_private_ops.py --root $(DEALIX_PRIVATE_ROOT)

mission-control: ## Refresh founder/mission_control.md
	$(PYTHON) scripts/generate_mission_control.py --root $(DEALIX_PRIVATE_ROOT)

ceo-action-queue: ## Refresh founder/ceo_action_queue.md
	$(PYTHON) scripts/generate_ceo_action_queue.py --root $(DEALIX_PRIVATE_ROOT)

control-tower: ## Refresh founder/control_tower_brief.md
	$(PYTHON) scripts/generate_control_tower_brief.py --root $(DEALIX_PRIVATE_ROOT)

business-score: ## Refresh business_audit/ceo_business_score.md
	$(PYTHON) scripts/generate_ceo_business_score.py --root $(DEALIX_PRIVATE_ROOT)

assurance: ## Refresh evidence/execution_assurance_report.md
	$(PYTHON) scripts/generate_execution_assurance_report.py --root $(DEALIX_PRIVATE_ROOT)

ceo-weekly: mission-control ceo-action-queue control-tower business-score assurance
	@echo "PASS: weekly CEO loop refreshed."

weekly-close: business-score assurance
	@echo "PASS: weekly close complete. Update metrics_history/weekly_metrics.csv next."

revenue-ops: ## Verify revenue ops doctrine
	$(PYTHON) scripts/verify_revenue_operations_playbook.py

delivery: ## Verify delivery + client success doctrine
	$(PYTHON) scripts/verify_delivery_client_success_os.py

finance-full: ## Generate finance command report + pricing review
	$(PYTHON) scripts/generate_finance_command_report.py --root $(DEALIX_PRIVATE_ROOT)
	$(PYTHON) scripts/generate_pricing_review.py --root $(DEALIX_PRIVATE_ROOT)

trust-full: ## Generate trust review and verify trust/AI risk OS
	$(PYTHON) scripts/verify_trust_ai_risk_os.py
	$(PYTHON) scripts/generate_trust_review.py --root $(DEALIX_PRIVATE_ROOT)

content: ## Verify content OS + scan content claims
	$(PYTHON) scripts/verify_brand_proof_content_os.py
	$(PYTHON) scripts/review_content_claims.py --root $(DEALIX_PRIVATE_ROOT)/content

productization: ## Generate productization review
	$(PYTHON) scripts/generate_productization_review.py --root $(DEALIX_PRIVATE_ROOT)

people: ## Verify people/partner OS
	$(PYTHON) scripts/verify_people_partner_os.py

partners: people
	@echo "PASS: partner system verified (covered by people target)."
