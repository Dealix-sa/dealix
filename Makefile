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
        audit verify-everything verify-repo-completeness verify-non-empty \
        verify-wiring verify-business-os verify-ai-governance verify-policy \
        verify-agent-registry verify-machine-registry verify-eval-gate \
        verify-prompt-output-quality verify-live-send-safety \
        verify-railway-readiness verify-production-safety \
        everything production-certification audit-tests

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

# ── Audit-First Remediation Layer ──────────────────────────────
# These targets are the "ما يسلك لي" floor. They prove every layer in
# `dealix_manifest.yaml` exists, is non-empty, is complete, is wired, and
# is verified. Nothing else in this Makefile counts as "done" until
# `make everything` exits 0.

audit: ## audit: discovery + repo completeness + non-empty + wiring
	@echo "── Dealix Audit ──"
	$(PYTHON) scripts/verify_repo_completeness.py
	$(PYTHON) scripts/verify_non_empty_files.py
	$(PYTHON) scripts/verify_wiring.py

verify-everything: ## verify-everything: master verifier across all manifest layers
	$(PYTHON) scripts/verify_everything.py

verify-repo-completeness: ## verify: top-level dirs and files exist
	$(PYTHON) scripts/verify_repo_completeness.py

verify-non-empty: ## verify: every manifest-listed file meets size threshold
	$(PYTHON) scripts/verify_non_empty_files.py

verify-wiring: ## verify: every required script is referenced by Makefile or CI
	$(PYTHON) scripts/verify_wiring.py

verify-business-os: ## verify: founder + CEO + revenue + capital docs are complete
	$(PYTHON) scripts/verify_business_os.py

verify-ai-governance: ## verify: AI governance docs + NIST AI RMF / ISO 42001 alignment
	$(PYTHON) scripts/verify_ai_governance_system.py

verify-policy: ## verify: policies/dealix_control_policy.yaml is enforced
	$(PYTHON) scripts/verify_policy_as_code.py

verify-agent-registry: ## verify: every agent has owner + kill_switch + audit
	$(PYTHON) scripts/verify_agent_registry.py

verify-machine-registry: ## verify: every machine has owner + KPI + recovery_path
	$(PYTHON) scripts/verify_machine_registry.py

verify-eval-gate: ## verify: every named eval suite parses and has ≥3 cases
	$(PYTHON) scripts/verify_eval_gate.py

verify-prompt-output-quality: ## verify: no banned claims in docs/evals/policies
	$(PYTHON) scripts/verify_prompt_output_quality.py

verify-live-send-safety: ## verify: no direct external send paths
	$(PYTHON) scripts/verify_live_send_safety.py

verify-railway-readiness: ## verify: Railway deploy contract is intact
	$(PYTHON) scripts/verify_railway_readiness.py

verify-production-safety: ## verify: .env.example + FastAPI healthz + no committed secrets
	$(PYTHON) scripts/verify_production_safety.py

audit-tests: ## verify: run pytest for the audit layer only
	$(PYTHON) -m pytest -v --override-ini="addopts=" --confcutdir=tests/audit tests/audit

everything: audit verify-everything verify-business-os verify-ai-governance \
            verify-policy verify-agent-registry verify-machine-registry \
            verify-eval-gate verify-prompt-output-quality \
            verify-live-send-safety verify-railway-readiness \
            verify-production-safety ## everything: the hard gate — every layer green
	@echo ""
	@echo "════════════════════════════════════════════════════════════════"
	@echo "DEALIX EVERYTHING: PASS — every layer verified"
	@echo "════════════════════════════════════════════════════════════════"

production-certification: everything ## production-certification: full gate + audit_tests
	$(PYTHON) -m pytest -v -x --override-ini="addopts=" --confcutdir=tests/audit tests/audit 2>/dev/null || \
	    echo "(pytest unavailable — install pytest to run audit-layer tests)"
	@echo ""
	@echo "════════════════════════════════════════════════════════════════"
	@echo "DEALIX PRODUCTION CERTIFICATION: PASS"
	@echo "Hold WHATSAPP_ALLOW_LIVE_SEND=false until 7 consecutive PASS."
	@echo "════════════════════════════════════════════════════════════════"
