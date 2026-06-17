# Revenue Factory OS — Documentation Suite Index

> النسخة العربية: [`INDEX_REVENUE_FACTORY_OS_AR.md`](./INDEX_REVENUE_FACTORY_OS_AR.md)

This is the spine of the Revenue Factory OS documentation suite: 25 EN
canonical documents + 25 AR companions + this index. Each row links the
operating spec to the underlying runtime (modules, routers, migrations,
scripts, GitHub Actions, Makefile targets) so the documentation is
**runnable**, not abstract.

## Doctrine

Every document in this suite anchors to the 5 non-negotiables in
[`docs/transformation/01_doctrine_lock.md`](./transformation/01_doctrine_lock.md):

1. No external high-risk action without approval.
2. No measured value claim without source evidence.
3. No cross-tenant operational access.
4. No production autonomy without rollback path.
5. No proof-level overclaiming beyond available evidence level.

## How to Use This Suite

- **Executive starting point**: [`founder/REVENUE_WAR_ROOM_OS.md`](./founder/REVENUE_WAR_ROOM_OS.md) and [`control_plane/SALES_COCKPIT_SYSTEM.md`](./control_plane/SALES_COCKPIT_SYSTEM.md).
- **Engineering starting point**: [`runtime/REVENUE_FACTORY_RUNTIME.md`](./runtime/REVENUE_FACTORY_RUNTIME.md), [`runtime/WORKER_QUEUE_ARCHITECTURE.md`](./runtime/WORKER_QUEUE_ARCHITECTURE.md), [`data/GROWTH_DATABASE_MODEL.md`](./data/GROWTH_DATABASE_MODEL.md).
- **Trust / compliance starting point**: [`control_plane/APPROVAL_CENTER_V2.md`](./control_plane/APPROVAL_CENTER_V2.md), [`trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`](./trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md), [`evals/AI_EVAL_RED_TEAM_SYSTEM.md`](./evals/AI_EVAL_RED_TEAM_SYSTEM.md).
- **Commercial starting point**: [`distribution/DEALIX_DISTRIBUTION_OS.md`](./distribution/DEALIX_DISTRIBUTION_OS.md), [`distribution/EXPERIMENT_ENGINE.md`](./distribution/EXPERIMENT_ENGINE.md), [`finance/PRICING_YIELD_MANAGEMENT.md`](./finance/PRICING_YIELD_MANAGEMENT.md).

## Document Index

### Tier A — Foundation

| # | EN canonical | AR companion | Primary runtime anchor |
|---|--------------|--------------|------------------------|
| 1 | [runtime/REVENUE_FACTORY_RUNTIME.md](./runtime/REVENUE_FACTORY_RUNTIME.md) | [runtime/REVENUE_FACTORY_RUNTIME_AR.md](./runtime/REVENUE_FACTORY_RUNTIME_AR.md) | `.github/workflows/daily-revenue-machine.yml`, `scripts/founder_revenue_day_runner.py` |
| 2 | [data/GROWTH_DATABASE_MODEL.md](./data/GROWTH_DATABASE_MODEL.md) | [data/GROWTH_DATABASE_MODEL_AR.md](./data/GROWTH_DATABASE_MODEL_AR.md) | `db/models.py`, `db/migrations/versions/` |
| 3 | [runtime/WORKER_QUEUE_ARCHITECTURE.md](./runtime/WORKER_QUEUE_ARCHITECTURE.md) | [runtime/WORKER_QUEUE_ARCHITECTURE_AR.md](./runtime/WORKER_QUEUE_ARCHITECTURE_AR.md) | `core/queue/worker.py`, `core/queue/tasks.py` |
| 4 | [control_plane/APPROVAL_CENTER_V2.md](./control_plane/APPROVAL_CENTER_V2.md) | [control_plane/APPROVAL_CENTER_V2_AR.md](./control_plane/APPROVAL_CENTER_V2_AR.md) | `auto_client_acquisition/approval_center/`, `api/routers/approval_center.py` |
| 5 | [trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md](./trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md) | [trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md](./trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md) | `db/models.py::SuppressionRecord`, `auto_client_acquisition/outreach_window.py` |

### Tier B — Commercial

| # | EN canonical | AR companion | Primary runtime anchor |
|---|--------------|--------------|------------------------|
| 6 | [distribution/DEALIX_DISTRIBUTION_OS.md](./distribution/DEALIX_DISTRIBUTION_OS.md) | [distribution/DEALIX_DISTRIBUTION_OS_AR.md](./distribution/DEALIX_DISTRIBUTION_OS_AR.md) | `auto_client_acquisition/whatsapp_safe_send.py`, `.github/workflows/founder_commercial_daily.yml` |
| 7 | [distribution/EMAIL_DELIVERABILITY_SYSTEM.md](./distribution/EMAIL_DELIVERABILITY_SYSTEM.md) | [distribution/EMAIL_DELIVERABILITY_SYSTEM_AR.md](./distribution/EMAIL_DELIVERABILITY_SYSTEM_AR.md) | `db/models.py::GmailDraftRecord`, `auto_client_acquisition/outreach_window.py` |
| 8 | [control_plane/SALES_COCKPIT_SYSTEM.md](./control_plane/SALES_COCKPIT_SYSTEM.md) | [control_plane/SALES_COCKPIT_SYSTEM_AR.md](./control_plane/SALES_COCKPIT_SYSTEM_AR.md) | `dashboard/app.py`, `api/routers/command_center.py` |
| 9 | [distribution/EXPERIMENT_ENGINE.md](./distribution/EXPERIMENT_ENGINE.md) | [distribution/EXPERIMENT_ENGINE_AR.md](./distribution/EXPERIMENT_ENGINE_AR.md) | `evals/`, `auto_client_acquisition/crm_v10/lead_scoring.py` |
| 10 | [founder/REVENUE_WAR_ROOM_OS.md](./founder/REVENUE_WAR_ROOM_OS.md) | [founder/REVENUE_WAR_ROOM_OS_AR.md](./founder/REVENUE_WAR_ROOM_OS_AR.md) | `.github/workflows/daily_digest.yml`, `make v5-digest` |
| 11 | [founder/BOARD_LEVEL_KPI_STACK.md](./founder/BOARD_LEVEL_KPI_STACK.md) | [founder/BOARD_LEVEL_KPI_STACK_AR.md](./founder/BOARD_LEVEL_KPI_STACK_AR.md) | `make v5-status`, `make v5-snapshot`, `make v5-verify` |

### Tier C — Downstream + Governance

| # | EN canonical | AR companion | Primary runtime anchor |
|---|--------------|--------------|------------------------|
| 12 | [client_success/CUSTOMER_LIFECYCLE_OS.md](./client_success/CUSTOMER_LIFECYCLE_OS.md) | [client_success/CUSTOMER_LIFECYCLE_OS_AR.md](./client_success/CUSTOMER_LIFECYCLE_OS_AR.md) | `auto_client_acquisition/revenue_memory/event_store.py`, `docs/delivery/DELIVERY_LIFECYCLE.md` |
| 13 | [finance/BILLING_RECEIVABLES_OS.md](./finance/BILLING_RECEIVABLES_OS.md) | [finance/BILLING_RECEIVABLES_OS_AR.md](./finance/BILLING_RECEIVABLES_OS_AR.md) | `db/migrations/versions/20260512_005_payments_table.py`, `docs/BILLING_MOYASAR_RUNBOOK.md` |
| 14 | [client_success/SUPPORT_SUCCESS_OS.md](./client_success/SUPPORT_SUCCESS_OS.md) | [client_success/SUPPORT_SUCCESS_OS_AR.md](./client_success/SUPPORT_SUCCESS_OS_AR.md) | `core/queue/cs_handoff_task.py` |
| 15 | [finance/PRICING_YIELD_MANAGEMENT.md](./finance/PRICING_YIELD_MANAGEMENT.md) | [finance/PRICING_YIELD_MANAGEMENT_AR.md](./finance/PRICING_YIELD_MANAGEMENT_AR.md) | `docs/PRICING_STRATEGY.md`, `docs/OFFER_LADDER_AND_PRICING.md` |
| 16 | [finance/AI_UNIT_ECONOMICS.md](./finance/AI_UNIT_ECONOMICS.md) | [finance/AI_UNIT_ECONOMICS_AR.md](./finance/AI_UNIT_ECONOMICS_AR.md) | `docs/OBSERVABILITY_ENV.md`, `dashboard/pages/` |
| 17 | [engineering/OBSERVABILITY_SLO_SYSTEM.md](./engineering/OBSERVABILITY_SLO_SYSTEM.md) | [engineering/OBSERVABILITY_SLO_SYSTEM_AR.md](./engineering/OBSERVABILITY_SLO_SYSTEM_AR.md) | `docs/SLO.md`, `make v5-verify` |
| 18 | [evals/AI_EVAL_RED_TEAM_SYSTEM.md](./evals/AI_EVAL_RED_TEAM_SYSTEM.md) | [evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md](./evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md) | `evals/`, `docs/EVALS_RUNBOOK.md` |
| 19 | [security/SUPPLY_CHAIN_HARDENING_ROADMAP.md](./security/SUPPLY_CHAIN_HARDENING_ROADMAP.md) | [security/SUPPLY_CHAIN_HARDENING_ROADMAP_AR.md](./security/SUPPLY_CHAIN_HARDENING_ROADMAP_AR.md) | `make security`, `make pre-commit-run` |
| 20 | [product/COMMAND_CENTER_PRODUCT_SPEC.md](./product/COMMAND_CENTER_PRODUCT_SPEC.md) | [product/COMMAND_CENTER_PRODUCT_SPEC_AR.md](./product/COMMAND_CENTER_PRODUCT_SPEC_AR.md) | `frontend/src/`, `dashboard/app.py` |
| 21 | [distribution/ABM_STRATEGIC_ACCOUNT_MACHINE.md](./distribution/ABM_STRATEGIC_ACCOUNT_MACHINE.md) | [distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md](./distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md) | `docs/commercial/operations/targeting/ABM_WAVE1_ICP_AR.md` |
| 22 | [partners/PARTNER_REVENUE_MACHINE.md](./partners/PARTNER_REVENUE_MACHINE.md) | [partners/PARTNER_REVENUE_MACHINE_AR.md](./partners/PARTNER_REVENUE_MACHINE_AR.md) | `docs/partners/` (existing cluster) |
| 23 | [intelligence/COMPETITIVE_INTELLIGENCE_MACHINE.md](./intelligence/COMPETITIVE_INTELLIGENCE_MACHINE.md) | [intelligence/COMPETITIVE_INTELLIGENCE_MACHINE_AR.md](./intelligence/COMPETITIVE_INTELLIGENCE_MACHINE_AR.md) | `docs/COMPETITIVE_POSITIONING.md`, `autonomous_growth/agents/` |
| 24 | [legal/COMMERCIAL_CONTRACT_PACK.md](./legal/COMMERCIAL_CONTRACT_PACK.md) | [legal/COMMERCIAL_CONTRACT_PACK_AR.md](./legal/COMMERCIAL_CONTRACT_PACK_AR.md) | `docs/legal/`, `templates/` |
| 25 | [localization/ARABIC_SALES_ENGINE.md](./localization/ARABIC_SALES_ENGINE.md) | [localization/ARABIC_SALES_ENGINE_AR.md](./localization/ARABIC_SALES_ENGINE_AR.md) | `docs/localization/`, `README.ar.md` |

## Runtime → Document Reverse Index

For engineers wanting to know "which doc explains how this code works":

| Runtime surface | Documented in |
|----------------|---------------|
| `db/models.py` (LeadRecord, SuppressionRecord, OutreachQueueRecord, etc.) | [data/GROWTH_DATABASE_MODEL.md](./data/GROWTH_DATABASE_MODEL.md) |
| `db/models.py::SuppressionRecord` | [trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md](./trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md) |
| `db/models.py::AuditLogRecord` | [control_plane/APPROVAL_CENTER_V2.md](./control_plane/APPROVAL_CENTER_V2.md) |
| `db/migrations/versions/20260512_005_payments_table.py` | [finance/BILLING_RECEIVABLES_OS.md](./finance/BILLING_RECEIVABLES_OS.md) |
| `core/queue/worker.py`, `tasks.py` | [runtime/WORKER_QUEUE_ARCHITECTURE.md](./runtime/WORKER_QUEUE_ARCHITECTURE.md) |
| `core/queue/cs_handoff_task.py` | [client_success/SUPPORT_SUCCESS_OS.md](./client_success/SUPPORT_SUCCESS_OS.md) |
| `auto_client_acquisition/approval_center/` | [control_plane/APPROVAL_CENTER_V2.md](./control_plane/APPROVAL_CENTER_V2.md) |
| `auto_client_acquisition/whatsapp_safe_send.py` | [distribution/EMAIL_DELIVERABILITY_SYSTEM.md](./distribution/EMAIL_DELIVERABILITY_SYSTEM.md), [distribution/DEALIX_DISTRIBUTION_OS.md](./distribution/DEALIX_DISTRIBUTION_OS.md) |
| `auto_client_acquisition/outreach_window.py` | [trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md](./trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md), [distribution/EMAIL_DELIVERABILITY_SYSTEM.md](./distribution/EMAIL_DELIVERABILITY_SYSTEM.md) |
| `auto_client_acquisition/crm_v10/lead_scoring.py` | [runtime/REVENUE_FACTORY_RUNTIME.md](./runtime/REVENUE_FACTORY_RUNTIME.md), [distribution/EXPERIMENT_ENGINE.md](./distribution/EXPERIMENT_ENGINE.md) |
| `auto_client_acquisition/revenue_memory/event_store.py` | [data/GROWTH_DATABASE_MODEL.md](./data/GROWTH_DATABASE_MODEL.md), [client_success/CUSTOMER_LIFECYCLE_OS.md](./client_success/CUSTOMER_LIFECYCLE_OS.md) |
| `api/routers/approval_center.py` | [control_plane/APPROVAL_CENTER_V2.md](./control_plane/APPROVAL_CENTER_V2.md) |
| `api/routers/command_center.py`, `business_now.py` | [control_plane/SALES_COCKPIT_SYSTEM.md](./control_plane/SALES_COCKPIT_SYSTEM.md), [product/COMMAND_CENTER_PRODUCT_SPEC.md](./product/COMMAND_CENTER_PRODUCT_SPEC.md) |
| `api/routers/automation.py` | [distribution/DEALIX_DISTRIBUTION_OS.md](./distribution/DEALIX_DISTRIBUTION_OS.md) |
| `dashboard/app.py`, `dashboard/pages/` | [control_plane/SALES_COCKPIT_SYSTEM.md](./control_plane/SALES_COCKPIT_SYSTEM.md), [product/COMMAND_CENTER_PRODUCT_SPEC.md](./product/COMMAND_CENTER_PRODUCT_SPEC.md), [finance/AI_UNIT_ECONOMICS.md](./finance/AI_UNIT_ECONOMICS.md) |
| `autonomous_growth/agents/` | [distribution/DEALIX_DISTRIBUTION_OS.md](./distribution/DEALIX_DISTRIBUTION_OS.md), [intelligence/COMPETITIVE_INTELLIGENCE_MACHINE.md](./intelligence/COMPETITIVE_INTELLIGENCE_MACHINE.md) |
| `.github/workflows/daily-revenue-machine.yml` | [runtime/REVENUE_FACTORY_RUNTIME.md](./runtime/REVENUE_FACTORY_RUNTIME.md) |
| `.github/workflows/founder_commercial_daily.yml` | [distribution/DEALIX_DISTRIBUTION_OS.md](./distribution/DEALIX_DISTRIBUTION_OS.md) |
| `.github/workflows/daily_digest.yml`, `make v5-digest` | [founder/REVENUE_WAR_ROOM_OS.md](./founder/REVENUE_WAR_ROOM_OS.md), [control_plane/APPROVAL_CENTER_V2.md](./control_plane/APPROVAL_CENTER_V2.md) |
| `.github/workflows/daily_snapshot.yml`, `make v5-snapshot` | [founder/BOARD_LEVEL_KPI_STACK.md](./founder/BOARD_LEVEL_KPI_STACK.md) |
| `make v5-verify` | [engineering/OBSERVABILITY_SLO_SYSTEM.md](./engineering/OBSERVABILITY_SLO_SYSTEM.md), [founder/BOARD_LEVEL_KPI_STACK.md](./founder/BOARD_LEVEL_KPI_STACK.md) |
| `make security`, `make pre-commit-run` | [security/SUPPLY_CHAIN_HARDENING_ROADMAP.md](./security/SUPPLY_CHAIN_HARDENING_ROADMAP.md) |
| `evals/` | [evals/AI_EVAL_RED_TEAM_SYSTEM.md](./evals/AI_EVAL_RED_TEAM_SYSTEM.md), [distribution/EXPERIMENT_ENGINE.md](./distribution/EXPERIMENT_ENGINE.md) |
| `scripts/founder_revenue_day_runner.py`, `run_dealix_complete_autonomous_day.py` | [runtime/REVENUE_FACTORY_RUNTIME.md](./runtime/REVENUE_FACTORY_RUNTIME.md) |
| `scripts/dealix_founder_daily_brief.py` | [distribution/DEALIX_DISTRIBUTION_OS.md](./distribution/DEALIX_DISTRIBUTION_OS.md), [founder/REVENUE_WAR_ROOM_OS.md](./founder/REVENUE_WAR_ROOM_OS.md) |

## Verification

To verify this suite is internally consistent:

```bash
# Every new doc has a Doctrine Anchor section
rg -l "^## (Doctrine Anchor|مرجع الدوكترين)" docs/runtime docs/distribution docs/control_plane docs/founder docs/finance docs/client_success docs/evals docs/intelligence/COMPETITIVE_INTELLIGENCE_MACHINE*.md docs/security/SUPPLY_CHAIN_HARDENING_ROADMAP*.md docs/product/COMMAND_CENTER_PRODUCT_SPEC*.md docs/partners/PARTNER_REVENUE_MACHINE*.md docs/legal/COMMERCIAL_CONTRACT_PACK*.md docs/localization/ARABIC_SALES_ENGINE*.md docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM*.md docs/data/GROWTH_DATABASE_MODEL*.md docs/engineering/OBSERVABILITY_SLO_SYSTEM*.md | wc -l
# expected: 50

# Bilingual completeness: every EN has its AR companion
ls docs/runtime/*.md docs/data/GROWTH_DATABASE_MODEL*.md docs/distribution/*.md docs/control_plane/*.md docs/founder/*.md docs/finance/*.md docs/client_success/*.md docs/engineering/OBSERVABILITY_SLO_SYSTEM*.md docs/evals/AI_EVAL_RED_TEAM_SYSTEM*.md docs/security/SUPPLY_CHAIN_HARDENING_ROADMAP*.md docs/product/COMMAND_CENTER_PRODUCT_SPEC*.md docs/partners/PARTNER_REVENUE_MACHINE*.md docs/intelligence/COMPETITIVE_INTELLIGENCE_MACHINE*.md docs/legal/COMMERCIAL_CONTRACT_PACK*.md docs/localization/ARABIC_SALES_ENGINE*.md docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM*.md | wc -l
# expected: 50

# No fake Makefile targets are referenced
rg "make growth-daily|make distribution|make day-start" docs/runtime docs/data docs/distribution docs/control_plane docs/founder docs/finance docs/client_success docs/evals docs/intelligence/COMPETITIVE_INTELLIGENCE_MACHINE*.md docs/security/SUPPLY_CHAIN_HARDENING_ROADMAP*.md docs/product/COMMAND_CENTER_PRODUCT_SPEC*.md docs/partners/PARTNER_REVENUE_MACHINE*.md docs/legal/COMMERCIAL_CONTRACT_PACK*.md docs/localization/ARABIC_SALES_ENGINE*.md docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM*.md docs/engineering/OBSERVABILITY_SLO_SYSTEM*.md
# expected: no matches
```

## Open Items (honest)

- This suite is **documentation**, not new runtime. Wiring up new
  Makefile targets, building the unified approval inbox UI, formalizing
  the experiment registry, and end-to-end reply routing are follow-up
  work — each of those is named as an Open Item in the relevant doc.
- ~12 of the 25 documents extend existing material (Pricing, Lifecycle,
  Observability, Evals, Red Team, Competitive, ABM, Partner, Contract,
  Command Center, War Room, Billing). Their value is consolidation +
  bilingual + doctrine-anchored format, not net-new strategy.
- This INDEX is the spine of this 51-document suite; it is not a
  replacement for a repo-wide `docs/INDEX.md` that catalogs all 2,222
  markdown files in the project.
