# Dealix Missing Systems — Honest Inventory

This file lists what is **stubbed** vs **production-ready** in the
26-layer implementation. Read this before claiming "done" on any layer.

## Production-ready

| Layer | Why |
|---|---|
| Agent Registry | YAML + verifier enforces all required fields. |
| Machine Registry | YAML + verifier enforces all required fields. |
| Policy-as-Code | YAML + verifier enforces 11 NNs + top-level keys. |
| Eval Gate | YAML + verifier enforces per-agent eval + NN coverage. |
| Brand OS | Doc + verifier enforces positioning/voice/visual + disclaimer. |
| Private Ops Runtime | Bootstrap script + doc + verifier; idempotent. |
| Verifier framework | `verify_everything.py` + 24 layer verifiers + `_common.py`. |
| Makefile surface | All 25 targets present + verified by `verify_makefile.py`. |
| GitHub Actions wiring | 2 new workflows + verifier ensures targets referenced. |

## Stubbed (works, but uses placeholder data)

| Layer | What's stubbed | What's needed |
|---|---|---|
| CEO Daily Brief | Template emits `pending live wiring` for pipeline / approvals / revenue | Wire to friction_log aggregator + Moyasar + approval queue |
| CEO Weekly Review | Template only | Wire to VOCD calc + pipeline + capital allocation |
| Capital Allocation report | Template with target % only, no actuals | Wire to spend ledger |
| Strategy Scorecard | Input/output rows say `pending` | Wire to Moyasar + Proof Pack store |
| Revenue Forecast | Forecast table all `pending` | Wire to Moyasar + Pipeline source |
| Internal API | Router created but NOT mounted in api/main.py | Add include_router in api/main.py |
| Founder Console pages | Render with source-of-truth ref but no live metrics | Wire dealix-runtime to live API once mounted |

## Existing infrastructure (REUSED, not duplicated)

| Layer | Reused module |
|---|---|
| AI Governance | `dealix/governance/` |
| Worker Orchestrator | `dealix/revenue_ops_autopilot/` + `scripts/run_founder_commercial_day.sh` |
| Launch Layer | `scripts/verify_commercial_launch_ready.py` + `scripts/official_launch_verify.sh` |
| Customer Success | `dealix/commercial_ops/` |
| Legal/Trust/Security | `docs/SECURITY_RUNBOOK.md` + `dealix/trust/` |
| Company Memory | `dealix/registers/` (existing YAML governance registers) |

## What deliberately did NOT change

- `api/main.py` (so the Internal API router is unmounted by default — opt-in)
- The 40 existing GitHub workflows
- Any of the existing Makefile targets above the new 26-layer block
- Any of the existing `dealix/` packages or `apps/web/components/`
- `AGENTS.md` (kept as the deep operating manual)

## Risk assessment

| Risk | Mitigation |
|---|---|
| Stubs falsely claim status | Every stubbed doc carries `pending live wiring` and the readiness report flags it. |
| Internal API unmounted by accident | Documented as a manual follow-up; verifier catches structural issues, not mount status. |
| Private ops files committed | Verifier `verify_private_ops_runtime.py` scans for leaked path under repo. |
| Reports overwrite without provenance | Each report file is timestamped (UTC) and dated; replay is non-destructive. |

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
