# Dealix 26-Layer Implementation Audit

**Branch:** `claude/eloquent-wright-LsBD0`
**Date:** 2026-05-24
**Source order:** Founder master implementation order for Dealix Company OS.

This audit is the input contract for every cluster engineer. Each row records
what already exists, what's missing, the canonical home, and the verifier that
guards the layer.

| # | Layer | Exists | Missing | Home | Verifier | Make target |
|---|---|---|---|---|---|---|
| 1 | Brand OS | `dealix/business_now/`, `docs/business/` | brand_system source-of-truth doc + verifier | `dealix/brand_system/` (new), `docs/brand/DEALIX_BRAND_OS.md` | `scripts/verifiers/verify_brand_system.py` | `brand-system` |
| 2 | Founder Console | 8 pages under `apps/web/app/{agents,approvals,control-plane,safety,sandbox,self-evolving,value-engine}` | `/ceo`, `/ceo-os`, `/founder-leverage`, `/capital-allocation`, `/strategy`, `/market-attack`, `/moat`, `/ai-governance`, `/company-memory` page.tsx + shared `founder-shell.tsx` + `dealix-runtime.ts` | `apps/web/app/<page>/page.tsx`, `apps/web/components/founder-console/`, `apps/web/lib/dealix-runtime.ts` | `scripts/verifiers/verify_founder_console.py` | `founder-console` |
| 3 | CEO Operating System | `scripts/run_ceo_one_session_readiness.sh`, `docs/transformation/CEO_ONE_SESSION_MASTER_PLAN_AR.md` | unified `verify_company_os.py` + daily/weekly brief generators | `scripts/generate_ceo_daily_brief.py`, `scripts/generate_ceo_weekly_review.py`, `docs/company/DEALIX_CEO_OS.md` | `scripts/verifiers/verify_company_os.py` | `company-os` |
| 4 | Capital Allocation | (none) | doc + report generator + verifier | `docs/company/DEALIX_CAPITAL_ALLOCATION.md`, `scripts/generate_capital_allocation_report.py` | `scripts/verifiers/verify_capital_allocation.py` | `capital-allocation` |
| 5 | Strategy Metrics | `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md` | scorecard generator + verifier | `docs/company/DEALIX_STRATEGY_METRICS.md`, `scripts/generate_strategy_scorecard.py` | `scripts/verifiers/verify_strategy_metrics.py` | `strategy-scorecard` |
| 6 | Revenue Factory | `dealix/revenue_ops_autopilot/`, many scripts | forecast generator + verifier doc | `docs/company/DEALIX_REVENUE_FACTORY.md`, `scripts/generate_revenue_forecast.py` | `scripts/verifiers/verify_revenue_factory.py` | `revenue-forecast` |
| 7 | Launch Layer | `scripts/official_launch_verify.sh`, `scripts/verify_commercial_launch_ready.py` | unified launch verifier orchestrator | `docs/company/DEALIX_LAUNCH_LAYER.md` | `scripts/verifiers/verify_launch_layer.py` | `launch-layer` |
| 8 | Market Attack System | (none formalized) | doc + verifier | `docs/company/DEALIX_MARKET_ATTACK.md` | `scripts/verifiers/verify_market_attack_system.py` | `market-attack-system` |
| 9 | Scale / Moat System | (none formalized) | doc + verifier | `docs/company/DEALIX_SCALE_MOAT.md` | `scripts/verifiers/verify_scale_moat_system.py` | `scale-moat-system` |
| 10 | Founder Management System | `docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md` | folded into `verify_company_os.py` | (existing doc) | `scripts/verifiers/verify_company_os.py` (shared) | `company-os` |
| 11 | Hypergrowth CEO Layer | (none formalized) | doc + verifier | `docs/company/DEALIX_HYPERGROWTH_CEO.md` | `scripts/verifiers/verify_founder_ceo_hypergrowth_layer.py` | `founder-ceo-hypergrowth-layer` |
| 12 | AI Governance | `dealix/governance/`, `scripts/verify_governance.py`, `evals/governance_eval.yaml` | unified verifier surfacing all governance modules | `docs/company/DEALIX_AI_GOVERNANCE.md` | `scripts/verifiers/verify_ai_governance.py` | `ai-governance` |
| 13 | Policy-as-Code | `policies/dealix_control_policy.yaml` (NEW) | parser + verifier | (existing yaml) | `scripts/verifiers/verify_policy_as_code.py` | `policy-check` |
| 14 | Agent Registry | `registries/agent_registry.yaml` (NEW) | schema + verifier | (existing yaml) | `scripts/verifiers/verify_agent_registry.py` | `agent-registry` |
| 15 | Machine Registry | (none) | yaml + schema + verifier | `registries/machine_registry.yaml` | `scripts/verifiers/verify_machine_registry.py` | `machine-registry` |
| 16 | Eval Gate | `evals/*.yaml`, `evals/personal_operator_cases.jsonl` | gate yaml + verifier | `evals/gates/dealix_agent_eval_gate.yaml` | `scripts/verifiers/verify_eval_gate.py` | `eval-gate` |
| 17 | Private Ops Runtime | (none committed) | bootstrap script + layout doc | `scripts/bootstrap_private_ops_runtime.py`, `docs/runtime/PRIVATE_OPS_LAYOUT.md` | `scripts/verifiers/verify_private_ops_runtime.py` | `bootstrap-runtime` |
| 18 | Internal API | many existing routers | `api/routers/internal/founder_console.py` (read-only console aggregator) | (new router) | `scripts/verifiers/smoke_internal_api.py` | `smoke-internal-api` |
| 19 | Worker Orchestrator | `dealix/revenue_ops_autopilot/`, `scripts/run_dealix_daily_ops.py` | doc + verifier | `docs/company/DEALIX_WORKER_ORCHESTRATOR.md` | `scripts/verifiers/verify_worker_orchestrator.py` | `worker-orchestrator` |
| 20 | Customer Success | `dealix/commercial_ops/`, many existing CS docs | doc + verifier | `docs/company/DEALIX_CUSTOMER_SUCCESS.md` | `scripts/verifiers/verify_customer_success.py` | `customer-success` |
| 21 | Enterprise Sales | `docs/commercial/*` | doc + verifier | `docs/company/DEALIX_ENTERPRISE_SALES.md` | `scripts/verifiers/verify_enterprise_sales.py` | `enterprise-sales` |
| 22 | Legal / Trust / Security | `docs/SECURITY_RUNBOOK.md`, `dealix/trust/` | doc + verifier | `docs/company/DEALIX_LEGAL_TRUST_SECURITY.md` | `scripts/verifiers/verify_legal_trust_security.py` | `legal-trust-security` |
| 23 | Company Memory | `dealix/registers/`, various memory files | doc + verifier | `docs/company/DEALIX_COMPANY_MEMORY.md` | `scripts/verifiers/verify_company_memory.py` | `company-memory` |
| 24 | Verifiers | many `scripts/verify_*.py` | supreme verifier `verify_everything.py` | `scripts/verify_everything.py` | (self) | `everything` |
| 25 | Makefile | existing Makefile | append 26-layer targets | `Makefile` | (self) | `help` |
| 26 | GitHub Actions | 40 existing workflows | `.github/workflows/dealix-everything.yml` + `dealix-company-os.yml` | (new workflow files) | n/a | n/a |

## Verifier contract

Every layer verifier prints exactly one final line:

```
<LAYER_NAME>: PASS|FAIL
```

It exits 0 on PASS, 1 on FAIL. Optional `--verbose` for diagnostic lines.

## Supreme verifier

`scripts/verify_everything.py` registers every layer verifier, can run a single
layer with `--layer NAME`, and on a full run prints the aggregate block:

```
DEALIX EVERYTHING VERIFICATION
Brand OS: PASS|FAIL
...
RESULT: PASS|FAIL
```

Exit 0 only when all 26 layers pass.

## Non-negotiables coverage

Every layer's verifier MUST refuse to PASS if any of the 11 non-negotiables
would be violated by its artifacts (e.g., a doc that promises guaranteed revenue
fails Brand OS; an agent missing from registry fails Agent Registry).
