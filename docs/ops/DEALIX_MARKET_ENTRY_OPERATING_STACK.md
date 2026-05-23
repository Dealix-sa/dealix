# Dealix Market Entry Operating Stack

This document describes the full operating stack that the Dealix Master Prompt v7 ships, and where each component lives in the repository. It is the index that verifier scripts use, and the map that humans use to navigate the system.

---

## 1. Layers

| Layer | What it does | Where it lives | Verified by |
|-------|--------------|----------------|-------------|
| Brand System | Visual identity, tokens, components, pillars | `docs/brand/`, `apps/web/lib/brand-tokens.ts`, `apps/web/components/brand/` | `scripts/verify_brand_system.py` |
| Growth System | Sector targeting, account scoring, distribution machines, intelligence layer | `docs/growth/`, `docs/intelligence/` | `scripts/verify_growth_system.py` |
| Marketing System | Content calendar, campaigns, ideas, GEO playbooks | `docs/marketing/` | `scripts/verify_marketing_system.py` |
| Product Distribution | Productization candidates, offer ladder, distribution OS | `docs/product/PRODUCT_DISTRIBUTION_OS.md`, `docs/product/DEALIX_PRODUCT_LADDER.md` | `scripts/verify_product_distribution.py` |
| Policy as Code | Control policy YAML enforced everywhere | `policies/dealix_control_policy.yaml` | `scripts/verify_policy_as_code.py` |
| Agent Registry | All AI agents (id, purpose, tools, approval class, owner) | `registries/agent_registry.yaml` | `scripts/verify_agent_registry.py` |
| Eval Gate | Required eval suites and pass thresholds | `evals/gates/dealix_agent_eval_gate.yaml` | `scripts/verify_eval_gate.py` |
| Prompt Output Quality | Static matrix of expected prompt outputs | `docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md` | `scripts/verify_prompt_output_quality.py` |
| Security Gate | Production-grade security posture | `docs/security/PRODUCTION_SECURITY_GATE.md` | rolled into `verify_sovereign_operating_stack.py` |
| Internal API | Founder/ops-only observability routes | `api/routers/internal/` (when added) | `scripts/smoke_internal_api.py` |
| Private Runtime Ledgers | CSV operating state | `$PRIVATE_OPS` (default `/opt/dealix-ops-private`) | `scripts/bootstrap_private_ops_runtime.py` |

---

## 2. Composite verifiers

| Composite | Components | Purpose |
|-----------|------------|---------|
| `verify_brand_growth_operating_layer.py` | brand + growth + marketing | Daily commercial surface check |
| `verify_ultimate_operating_layer.py` | brand + growth + marketing + policy + agent registry + eval gate | Full ops-layer check |
| `verify_sovereign_operating_stack.py` | all of the above + security gate | Pre-release readiness |
| `verify_market_entry_stack.py` | runs every verifier and prints a scorecard | One-button market readiness |

---

## 3. Worker scripts

Workers read CSVs from `$PRIVATE_OPS` and print summaries to stdout. They never send external messages or write production data.

| Worker | Reads | Writes |
|--------|-------|--------|
| `run_ceo_summary_worker.py` | `runtime/`, `finance/`, `sales/`, `trust/` | `founder/operating_scorecard.md` (optional) |
| `run_sales_funnel_worker.py` | `sales/`, `outreach/` | stdout |
| `run_trust_flags_worker.py` | `trust/` | stdout |
| `run_finance_summary_worker.py` | `finance/` | stdout |
| `run_operating_scorecard_worker.py` | aggregates above | `founder/operating_scorecard.md` |

---

## 4. Workflows

| Workflow | Trigger | Runs |
|----------|---------|------|
| `.github/workflows/dealix-brand-growth-operating-layer.yml` | push to main, PR | `make brand-growth-operating-layer` |
| `.github/workflows/dealix-sovereign-operating-stack.yml` | weekly, PR | `make sovereign-operating-stack` |
| `.github/workflows/dealix-market-entry-stack.yml` | weekly, PR | `make market-entry-stack` + `make smoke-internal-api` |

---

## 5. Operating rhythm

| Cadence | Action |
|---------|--------|
| Per-PR | brand-growth, sovereign, market-entry workflows |
| Weekly | sovereign + market-entry on schedule |
| Daily | founder runs `make brand-growth-operating-layer` locally |
| Quarterly | review and bump policy version, agent registry, eval gate thresholds |

---

## 6. Where to add next

When extending the stack:

- New agent → add row in `registries/agent_registry.yaml` and one suite in `evals/gates/dealix_agent_eval_gate.yaml`.
- New policy → add rule in `policies/dealix_control_policy.yaml` and add to required list in `scripts/verify_policy_as_code.py`.
- New surface (e.g., partnerships) → add `docs/<surface>/` plus `scripts/verify_<surface>.py` and wire into `verify_market_entry_stack.py`.

This document is the index. If you cannot find a component on this map, it has not yet been wired into the operating stack.
