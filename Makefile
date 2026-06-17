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
        launch-validate launch-vertical-score launch-icp-score launch-trust-preflight \
        launch-outreach-drafts launch-proposal launch-founder-command launch-weekly-review \
        launch-content launch-pipeline launch-all-dry-runs test-launch

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

# ── Distribution / Revenue Execution OS ────────────────────────
# Approval-first revenue execution. All read-only or draft-only — none of
# these send anything externally or charge a customer.

distribution-day: ## Founder morning command report (pending drafts, due follow-ups, queues)
	$(PYTHON) scripts/distribution_day.py

draft-quality: ## Draft Quality Gate — fail on guaranteed-outcome / forbidden-channel drafts
	$(PYTHON) scripts/check_draft_quality.py

distribution-metrics: ## Write the daily + weekly distribution KPI snapshot
	$(PYTHON) scripts/distribution_metrics.py

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

# ── Launch OS (GTM Revenue Intelligence) ───────────────────────
# All targets are read-only dry-runs — no external sends, no production mutations.

launch-validate: ## Launch OS: validate schemas + file inventory
	$(PYTHON) scripts/launch/launch_bundle_validate.py

launch-vertical-score: ## Launch OS: print ranked Saudi verticals + top wedge
	$(PYTHON) scripts/launch/vertical_score_dry_run.py

launch-icp-score: ## Launch OS: score sample accounts, print tier table
	$(PYTHON) scripts/launch/icp_score_dry_run.py

launch-trust-preflight: ## Launch OS: run trust preflight on sample drafts
	$(PYTHON) scripts/launch/trust_preflight_dry_run.py

launch-outreach-drafts: ## Launch OS: generate sample outreach drafts (email/linkedin/phone)
	$(PYTHON) scripts/launch/outreach_draft_factory_dry_run.py

launch-proposal: ## Launch OS: render sample proposal pack to markdown
	$(PYTHON) scripts/launch/proposal_pack_dry_run.py

launch-founder-command: ## Launch OS: generate today's founder daily brief
	$(PYTHON) scripts/launch/founder_daily_command_dry_run.py

launch-weekly-review: ## Launch OS: print weekly GTM review from sample pipeline
	$(PYTHON) scripts/launch/weekly_gtm_review_dry_run.py

launch-content: ## Launch OS: generate sample content assets (LinkedIn / video / email)
	$(PYTHON) scripts/launch/content_factory_dry_run.py

launch-pipeline: ## Launch OS: print pipeline summary from sample data
	$(PYTHON) -c "from dealix.launch_os.pipeline_tracker import PipelineTracker; t = PipelineTracker(); t.seed_sample(); print(t.pipeline_summary())"

launch-all-dry-runs: launch-validate launch-vertical-score launch-icp-score launch-trust-preflight launch-outreach-drafts launch-proposal launch-founder-command launch-weekly-review launch-content ## Launch OS: run all dry-run scripts in sequence
	@echo "✅ All Launch OS dry-runs completed"

test-launch: ## Launch OS: run launch-specific test suite
	pytest tests/launch/ -v --tb=short

# ═══════════════════════════════════════════════════════════════
# Company Operating System — launch controls
# ═══════════════════════════════════════════════════════════════

# ── Safety gates ───────────────────────────────────────────────
company-check: no-auto-send-check large-file-check secret-check outreach-compliance-check ## Run all company launch safety checks
	$(PYTHON) scripts/verify_company_launch_ready.py

launch-check: company-check ## Alias for company-check

no-auto-send-check: ## Verify no ungated auto external send patterns
	$(PYTHON) scripts/verify_no_auto_external_send.py

large-file-check: ## Verify no new forbidden large files / archives
	$(PYTHON) scripts/verify_repo_large_files.py

secret-check: ## Scan for suspicious secret patterns
	$(PYTHON) scripts/verify_secret_patterns.py

outreach-compliance-check: ## Verify outreach data has source_url, verification_status, opt-out
	$(PYTHON) scripts/verify_outreach_compliance.py

# ── Daily revenue machine ──────────────────────────────────────
revenue-daily: ## Run the full daily revenue machine (dry-run, drafts only)
	$(PYTHON) scripts/revenue/run_daily_revenue_machine.py

outreach: ## Generate outreach drafts for today
	$(PYTHON) scripts/revenue/generate_outreach.py

followups: ## Generate follow-up drafts (day 3 / day 7)
	$(PYTHON) scripts/revenue/generate_followups.py

proposals: ## Generate one-page proposal briefs for hot leads
	$(PYTHON) scripts/revenue/generate_proposal_brief.py

revenue-report: ## Generate daily CEO revenue report
	$(PYTHON) scripts/revenue/generate_daily_revenue_report.py

# ── 100-company workflow ───────────────────────────────────────
prepare-100: ## Prepare a 100-company research queue (default batch=10)
	$(PYTHON) scripts/revenue/prepare_100_target_day.py --batch-size $(or $(BATCH_SIZE),10)

validate-100: ## Validate the 100-company day before contact
	$(PYTHON) scripts/revenue/validate_100_target_day.py

batch-queue: ## Build batch outreach queue with cooldown + max follow-up gates
	$(PYTHON) scripts/revenue/batch_outreach_queue.py --batch-size $(or $(BATCH_SIZE),10)

# ── Gmail drafts (manual review required) ──────────────────────
gmail-drafts-dry-run: ## Preview Gmail drafts without creating them
	$(PYTHON) scripts/email/create_gmail_drafts_safe.py --dry-run

gmail-drafts: ## Create Gmail drafts from generated outbox (requires env vars)
	$(PYTHON) scripts/email/create_gmail_drafts_safe.py

# ── Server readiness ───────────────────────────────────────────
server-preflight: ## Run server preflight checks
	$(PYTHON) scripts/server/server_preflight.py

server-health: ## Run server healthcheck
	bash scripts/server/server_healthcheck.sh

company-production-smoke: ## Run company-focused production smoke tests
	bash scripts/server/run_production_smoke.sh

# ── Command center ─────────────────────────────────────────────
command-room: ## Build the offline founder command room dashboard
	$(PYTHON) scripts/command_room/build_command_room.py

# ── One-command company day ────────────────────────────────────
company-day: ## Run full company launch day pipeline
	bash scripts/run_company_launch_day.sh


.PHONY: company-check launch-check no-auto-send-check large-file-check secret-check outreach-compliance-check revenue-daily outreach followups proposals revenue-report prepare-100 validate-100 batch-queue gmail-drafts-dry-run gmail-drafts server-preflight server-health company-production-smoke command-room company-day
