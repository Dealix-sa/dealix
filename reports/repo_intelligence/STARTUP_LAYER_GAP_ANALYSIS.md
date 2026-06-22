# Dealix STARTUP_LAYER_GAP_ANALYSIS.md

**Date:** 2026-06-23

## Gap matrix

| Startup layer | Status | Existing assets | Gaps |
|---|---|---|---|
| Revenue Command Room OS | partial | `business/products/REVENUE_COMMAND_ROOM_OS.md`, `scripts/revenue/`, `scripts/command_room/`, `ledgers/` | Need deterministic `full-revenue-day`; better target scoring; `outbound-dry` target |
| Company Brain OS | missing | `founder_os/`, `executive/`, `intelligence/`, `autonomous_growth/` have fragments | Need `scripts/brain/`, `reports/brain/`, `ledgers/decisions_log.csv`, daily decision format |
| WhatsApp / Inbox Follow-up OS | partial | `auto_client_acquisition/whatsapp_client_os/`, `auto_client_acquisition/whatsapp_safe_send.py` | Need product doc, unified inbox model, follow-up queue |
| AI Trust & Compliance OS | partial | `dealix/registers/compliance_saudi.yaml`, `dealix/registers/no_overclaim.yaml`, `business/products/CONTROLLED_LIVE_OUTBOUND_OS.md` | Need `trust/` policy pack, tests, PDPL/SDAIA checklists |
| Client Delivery OS | partial | `clients/_TEMPLATE/`, `clients/_PROJECT_WORKBENCH/`, `company/delivery/CLIENT_DELIVERY_OS.md` | Need `clients/_template/` canonical structure, `scripts/delivery/`, Makefile targets |
| Controlled Live Outbound OS | partial | `app/outbound/policy_gate.py`, `auto_client_acquisition/email/`, `auto_client_acquisition/whatsapp_safe_send.py` | Need `scripts/outbound/`, dry-run target, suppression/rate-limit tests |
| Company Diagnosis Sprint | missing | `auto_client_acquisition/diagnostic_engine/`, `docs/services/ai_ops_diagnostic/offer.md` | Need sprint doc, intake form, diagnosis report template |
| Daily CEO Decision Desk | missing | `docs/CEO_OPERATING_CONTEXT.md`, `business/reports/DAILY_CEO_BRIEF_TEMPLATE.md` | Need `scripts/brain/generate_daily_decision.py`, decision format |
| Offer Intelligence OS | missing | `business/proposals/`, `docs/COMPANY_SERVICE_LADDER.md` | Need offer doc, pricing, packaging, upsell path |
| Market & Competitor Watch OS | missing | `auto_client_acquisition/market_intelligence/`, `autonomous_growth/` | Need radar script, competitor register, signals ledger |

## Shortest path to close gaps

### Phase 1 (now)
- Stabilize build, tests, company-day, command-room.
- Add `outbound-dry` target.
- Gitignore generated artifacts.

### Phase 2
- Consolidate brand/company/product docs into `docs/company/`, `docs/brand/`, `business/products/`.
- Reuse `docs/COMPANY_SERVICE_LADDER.md` and `business/proposals/` for Offer Intelligence.

### Phase 3
- Use existing `frontend/src/app/[locale]/` pages to build public homepage, product pages, diagnostic CTA.
- Reuse `frontend/src/components/command-room/`, `dashboard/`, `services/` components.

### Phase 4
- Wrap existing `scripts/revenue/` into `run_revenue_day.py` with deterministic output.
- Reuse `auto_client_acquisition/email/daily_targeting.py` for research.
- Reuse `auto_client_acquisition/email/compliance.py` for compliance gate.

### Phase 5
- Build `scripts/brain/` using existing `founder_os/`, `executive/`, `intelligence/` content as seed.
- Link brain outputs into command room.

### Phase 6
- Standardize `clients/_template/` from existing `_TEMPLATE/` + `_PROJECT_WORKBENCH/`.
- Add `scripts/delivery/client_intake.py` etc.

### Phase 7
- Create `trust/` from existing compliance registers and `auto_client_acquisition/compliance_os/`.

### Phase 8
- Add `scripts/outbound/check_live_outbound_env.py` and `run_controlled_live_outbound.py`.
- Connect to `app/outbound/policy_gate.py`.

### Phase 9
- Add alembic migrations; finalize env examples; document Railway deploy.

### Phase 10
- Reuse `autonomous_growth/` and existing `sales/` playbooks for GTM machine.

### Phase 11
- Add founder dashboard views using existing `frontend/src/components/`.

### Phase 12
- Produce final go/no-go pack.

## Biggest reuse opportunities

1. `frontend/` already has ~70 pages and many components. Do not rebuild.
2. `auto_client_acquisition/` has research, compliance, email, WhatsApp code. Wrap it, don't rewrite.
3. `clients/_TEMPLATE/` and `_PROJECT_WORKBENCH/` are 90% of Client Delivery OS.
4. `docs/DEALIX_OPERATING_CONSTITUTION.md` and `docs/COMPANY_SERVICE_LADDER.md` are the core of the source-of-truth layer.
5. `tests/test_no_auto_send.py` and `scripts/verify_no_auto_external_send.py` already enforce the safety contract.
