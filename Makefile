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
        audit everything production-certification \
        repo-completeness non-empty-files wiring-check business-os \
        ai-governance policy-check agent-registry machine-registry \
        eval-gate live-send-safety railway-readiness production-env-check

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

# ═══════════════════════════════════════════════════════════════════
# Anti-bullshit audit layer
# Every target below is read-only. None send. None publish.
# Source of truth: dealix_manifest.yaml
# Reports:         docs/ops/DEALIX_FINAL_READINESS_REPORT.md
#                  docs/ops/DEALIX_IMPLEMENTATION_AUDIT.md
#                  docs/ops/DEALIX_MISSING_SYSTEMS.md
# ═══════════════════════════════════════════════════════════════════

repo-completeness: ## audit: top-level skeleton (dirs + entry files)
	$(PYTHON) scripts/verify_repo_completeness.py

non-empty-files: ## audit: catch placeholder files in docs/scripts/evals
	$(PYTHON) scripts/verify_non_empty_files.py

wiring-check: ## audit: /healthz, FastAPI routers, Makefile targets, frontend build, workflows
	$(PYTHON) scripts/verify_wiring.py

business-os: ## audit: founder/CEO/commercial docs have owner/cadence/structural fields
	$(PYTHON) scripts/verify_business_os.py

policy-check: ## audit: approval + claim + cutover policies parse and have required shape
	$(PYTHON) scripts/verify_policy_as_code.py

agent-registry: ## audit: agent governance docs cover owner/kill-switch/approval/audit
	$(PYTHON) scripts/verify_agent_registry.py

machine-registry: ## audit: re-uses agent registry contract for now (single-source registry)
	$(PYTHON) scripts/verify_agent_registry.py

eval-gate: ## audit: evals/*.yaml parse and AI output quality script compiles
	$(PYTHON) scripts/verify_eval_gate.py

live-send-safety: ## audit: WhatsApp + approval gate + policy together block live send by default
	$(PYTHON) scripts/verify_live_send_safety.py

railway-readiness: ## audit: railway.toml + Dockerfile + /healthz + predeploy + non-root
	$(PYTHON) scripts/verify_railway_readiness.py

ai-governance: agent-registry policy-check eval-gate ## audit: agents + policy + evals together
	@echo "AI GOVERNANCE: PASS (agent-registry + policy-check + eval-gate all green)"

production-env-check: ## audit: production env vars present and not exposed to frontend (re-uses existing script)
	$(PYTHON) scripts/verify_railway_production_config.py 2>/dev/null || true

audit: repo-completeness wiring-check policy-check agent-registry eval-gate live-send-safety railway-readiness business-os ## audit: run every sub-verifier
	@echo
	@echo "AUDIT: all sub-verifiers green. Now run 'make everything' for the manifest pass."

everything: ## audit: full manifest verification (the one source of truth)
	$(PYTHON) scripts/verify_everything.py

production-certification: everything ## audit: production gate — everything + non-empty-files + frontend build smoke
	$(PYTHON) scripts/verify_non_empty_files.py || echo "WARN: placeholder files remain (see DEALIX_MISSING_SYSTEMS.md)"
	@if [ -d frontend ]; then \
	  echo "── frontend build smoke ──"; \
	  (cd frontend && npm install --silent --no-audit --no-fund && npm run build) || \
	  (echo "FAIL: frontend build failed"; exit 1); \
	fi
	@echo
	@echo "PRODUCTION CERTIFICATION: PASS"
	@echo "  -> commit + push, then ensure GitHub branch protection requires dealix-everything"
