# CANONICAL COMMAND PATH — Dealix Launch Readiness

## Local Readiness (Developer)
```bash
# 1. Environment
make setup                    # Install deps + create .env
make env-check               # Validate env contract

# 2. Database
docker compose up -d postgres redis
make db-init                 # Dev only

# 3. Backend
make run                     # uvicorn api.main:app --reload
make doctor                  # Full health check

# 4. Frontend (canonical: frontend/)
cd frontend && npm install && npm run typecheck && npm run build
```

## Commercial Go-Live (Founder)
```bash
# 1. Verification bundle
make prod-verify             # env-check + security-smoke + api-contract-check + dependency-inventory + release-manifest + v5-verify

# 2. Commercial launch gate
bash scripts/verify_dealix_commercial_go_live.sh
# OR
python3 scripts/verify_commercial_launch_ready.py

# 3. Full local stack
bash scripts/dealix_local_stack_verify.sh
```

## Production Smoke
```bash
# Against live deployment
make production-smoke PRODUCTION_BASE_URL=https://api.dealix.me
# OR
bash scripts/post_redeploy_verify.sh  # v5-verify
```

## Quick Regression Test Bundle
```bash
APP_ENV=test pytest tests/test_pg_event_store.py tests/test_model_router.py tests/test_integrations.py tests/test_v5_layers.py tests/unit/test_compliance_os.py tests/test_isolated_pg_event_store.py tests/test_saudi_targeting_profile.py tests/test_leads_batch_router.py tests/test_strategy_os_scoring.py tests/test_strategy_os_ai_readiness.py tests/test_data_os_quality.py tests/test_governance_os_draft_gate.py tests/test_delivery_os_framework.py tests/test_commercial_engagements_lead_intelligence.py tests/test_commercial_engagements_support_desk.py tests/test_commercial_engagements_quick_win_ops.py tests/test_commercial_roadmap_mvp.py tests/test_service_readiness_score.py tests/test_readiness_gates.py tests/test_db_sync_url.py tests/test_sync_weekly_ops_from_checklist_log.py tests/test_workflow_control_registry.py tests/test_populate_kpi_baselines_platform_signals.py tests/test_ceo_master_plan_status.py tests/test_founder_comprehensive_plan.py -q --no-cov
```

## Command Map (Makefile → Script)

| Makefile Target | Script | Purpose | Status |
|----------------|--------|---------|--------|
| `make env-check` | `scripts/check_env_contract.py` | Validate env contract | ✅ OK |
| `make security-smoke` | `scripts/security_smoke.py` | Repo security smoke | ⚠️ Slow on large repo |
| `make api-contract-check` | `scripts/check_openapi_contract.py` | OpenAPI drift check | ✅ OK |
| `make dependency-inventory` | `scripts/export_dependency_inventory.py` | Export deps | ✅ OK |
| `make release-manifest` | `scripts/export_release_manifest.py` | Export manifest | ✅ OK |
| `make production-smoke` | `scripts/dealix_smoke_test.py` | Production smoke | ✅ OK |
| `make alembic-heads` | `scripts/check_alembic_single_head.py` | Single head check | ✅ OK |
| `make openapi-export` | `scripts/export_openapi.py` | Export OpenAPI JSON | ✅ OK |
| `make v5-verify` | `scripts/post_redeploy_verify.sh` | 22-point production verify | ✅ OK |
| `make v10-verify` | `scripts/v10_master_verify.sh` | v10 reference library verify | ✅ OK |
| `make doctor` | env-check + alembic-heads + security-smoke | Full health check | ✅ OK |
| `make prod-verify` | doctor + api-contract-check + dependency-inventory + release-manifest + v5-verify | Canonical production bundle | ✅ OK |

## Verified Status
- All 14 critical scripts exist and compile
- All Makefile targets point to existing files
- README.md, AGENTS.md, and Makefile reference consistent command names
- No stale/broken commands found
