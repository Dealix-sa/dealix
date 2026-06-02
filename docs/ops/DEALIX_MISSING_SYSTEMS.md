# Dealix Missing Systems

**Generated:** 2026-05-24
**Companion to:** `DEALIX_IMPLEMENTATION_AUDIT.md`

This document lists what is **not yet built** at the time of this PR. The verifier layer (`make everything`) currently passes because every anchor file exists — but the deeper company-runtime layer is not yet in place. This is the explicit roadmap for the next PRs.

---

## What this PR did NOT build

These layers are intentionally deferred. They will land in Phase 2-5.

### Phase 2 — Generators (`scripts/generate_*.py`)

Missing report generators (30+):

| Generator | Purpose | Output path (under `${PRIVATE_OPS}`) |
|---|---|---|
| `generate_ceo_daily_brief.py` | CEO Daily Brief (top action, revenue, bottleneck, trust flags) | `founder/ceo_daily_brief.md` |
| `generate_ceo_weekly_review.py` | CEO Weekly Review | `founder/ceo_weekly_review.md` |
| `generate_founder_leverage_report.py` | Founder leverage / time audit | `founder/founder_leverage.md` |
| `generate_capital_allocation_report.py` | Capital allocation board | `finance/capital_allocation.csv` + `.md` |
| `generate_strategy_scorecard.py` | Strategy scorecard | `founder/strategy_scorecard.md` |
| `generate_revenue_forecast.py` | Revenue forecast | `finance/revenue_forecast.md` |
| `generate_weekly_growth_review.py` | Weekly growth review | `growth/weekly_growth_review.md` |
| `generate_beachhead_sector_scorecard.py` | Beachhead sector scorecard | `market_attack/beachhead_sector_scorecard.{csv,md}` |
| `generate_strategic_account_list.py` | Strategic accounts | `market_attack/strategic_accounts.csv` |
| `generate_offer_market_fit_report.py` | Offer-market-fit report | `market_attack/offer_market_fit_report.md` |
| `generate_campaign_command_report.py` | Campaign command report | `campaigns/campaign_command_report.md` |
| `generate_authority_content_queue.py` | Authority content queue | `growth/authority_content_queue.csv` |
| `generate_partner_pipeline_report.py` | Partner pipeline | `partners/partner_pipeline.csv` |
| `generate_objection_intelligence_report.py` | Objection intelligence | `market_attack/objection_library.csv` |
| `generate_revenue_intelligence_graph_report.py` | Revenue intelligence graph | `graph/revenue_intelligence_graph_report.md` |
| `generate_sector_playbook_report.py` | Sector playbook | `growth/sector_playbook.md` |
| `generate_message_performance_report.py` | Message performance | `growth/message_performance.csv` |
| `generate_buyer_objection_graph.py` | Buyer objection graph | `graph/objections.csv` |
| `generate_proof_library_report.py` | Proof library | `proof/proof_library.csv` |
| `generate_partner_ecosystem_report.py` | Partner ecosystem | `partners/partner_ecosystem.csv` |
| `generate_productization_pipeline_report.py` | Productization pipeline | `product/productization_pipeline.csv` |
| `generate_expansion_report.py` | Customer expansion | `customer_success/expansion_map.csv` |
| `generate_moat_scorecard.py` | Moat scorecard | `moat/moat_scorecard.md` |
| `generate_ai_governance_board_pack.py` | AI Governance board pack | `trust/board_pack.md` |
| `generate_data_moat_report.py` | Data moat report | `data/data_moat.md` |
| `generate_talent_gap_report.py` | Talent gap | `people/talent_gap.csv` |
| `generate_company_memory_report.py` | Company memory | `learning/company_memory.csv` |
| `generate_monthly_advisor_update.py` | Monthly advisor update | `founder/advisor_update.md` |

Plus the bootstrap:
- `scripts/bootstrap_private_ops_runtime.py` — creates the `/opt/dealix-ops-private/` skeleton (33 directories, ~70 CSV/MD files).
- `scripts/update_worker_state.py` — heartbeat for each worker.
- `scripts/smoke_internal_api.py` — Founder Console API smoke test.

### Phase 3 — Founder Console (`apps/web/`)

The repo currently has `frontend/` (Next.js 15). The canonical `apps/web/` layout described in long-form planning docs is a future migration. Missing pages:

```
apps/web/app/
├── ceo/page.tsx                    ← /ceo command center
├── ceo-os/page.tsx
├── founder-leverage/page.tsx
├── strategy/page.tsx
├── capital-allocation/page.tsx
├── sales-cockpit/page.tsx
├── deal-desk/page.tsx
├── approvals/page.tsx
├── workers/page.tsx
├── trust/page.tsx
├── ai-governance/page.tsx
├── finance/page.tsx
├── finance-ops/page.tsx
├── distribution/page.tsx
├── launch/page.tsx
├── market-attack/page.tsx
├── campaigns/page.tsx
├── sales-assets/page.tsx
├── authority/page.tsx
├── revenue-intelligence/page.tsx
├── moat/page.tsx
├── playbooks/page.tsx
├── proof-library/page.tsx
├── partner-ecosystem/page.tsx
├── productization/page.tsx
├── customer-success/page.tsx
├── delivery/page.tsx
├── retention/page.tsx
├── proof/page.tsx
├── data/page.tsx
├── experiments/page.tsx
├── security/page.tsx
├── audit/page.tsx
├── metrics/page.tsx
├── legal/page.tsx
├── advisor/page.tsx
└── settings/page.tsx                ← 37 pages total
```

Missing brand components (`apps/web/components/brand/`):
- `dealix-logo.tsx` (minimal, replaces `frontend/src/components/brand/BrandLogo.tsx`)
- `brand-card.tsx`
- `metric-card.tsx`
- `status-badge.tsx`
- `section-heading.tsx`
- `cta-button.tsx`
- `trust-badge.tsx`
- `growth-arrow.tsx`
- `proof-card.tsx`
- `offer-card.tsx`

Missing libraries:
- `apps/web/lib/brand-tokens.ts` (Deep Green + Gold token system)
- `apps/web/lib/dealix-runtime.ts` (reads `${PRIVATE_OPS}` CSVs)
- `apps/web/lib/dealix-actions.ts` (queues approvals, never sends)

### Phase 4 — Founder Console Internal API (`api/internal/`)

```
api/internal/
├── auth.py
├── runtime_reader.py
├── policy_adapter.py
└── routers/internal/
    └── founder_console.py
```

These are NEW under a separate `internal` namespace — the existing 170+ public routers are untouched.

### Phase 5 — GitHub Workflows + Makefile per-layer commands

This PR adds `dealix-everything.yml` only. The 7 deferred workflows:

- `dealix-brand-growth-operating-layer.yml`
- `dealix-company-os.yml` (broader than the master gate; per-PR)
- `dealix-execution-launch-layer.yml`
- `dealix-market-attack-system.yml`
- `dealix-scale-moat-system.yml`
- `dealix-founder-management-system.yml`
- `dealix-hypergrowth-ceo-layer.yml`

Per-layer Makefile commands for **generators** (e.g. `make ceo-daily-brief PRIVATE_OPS=…`) — currently the Makefile has *verifier* targets but no *generator* targets. The generator targets land in Phase 2.

### Phase 6 — Private Ops bootstrap (off-repo)

`/opt/dealix-ops-private/` skeleton — see the planning doc on the user's machine for the full 33-directory list. This is NEVER committed to the repo (contains sensitive customer data).

---

## Cross-cutting gaps (within the verifier layer itself)

Even though every verifier currently passes, here are the limitations to be aware of:

| Limitation | Impact | Future PR |
|---|---|---|
| Verifiers only check anchor files exist, not contents | A doc can be empty and still PASS | Add deep schema check per layer |
| Banned-claim scanner is substring + 300-char negation window | A claim hidden across paragraphs may pass; a long negation may fail | Add LLM-assisted semantic check, but only as warn, not block |
| Agent Registry cross-check skipped when `pydantic` is missing | Local dev without deps reports SKIP | Already handled; CI installs pydantic and runs the cross-check |
| Machine Registry doesn't check schedule strings | A typo in `cron: "0 6 * * 0"` is invisible | Future PR can parse + validate cron expressions |
| Eval Gate doesn't enforce live pass rates | Thresholds defined; not yet measured | Wire `scripts/run_evals.py` to write a status JSON the gate reads |
| Company OS layer check is structural only | Doesn't measure functional completeness | Each layer needs its own deep verifier (Phase 2-5) |

---

## Priority order for the next PR

1. **Phase 2 — Generators**: `bootstrap_private_ops_runtime.py` + `generate_ceo_daily_brief.py` + `generate_capital_allocation_report.py` + `generate_beachhead_sector_scorecard.py` first. These produce immediate founder value.
2. **Phase 4 — Internal API**: a single `/api/internal/founder/state` endpoint that returns the data backing the CEO Daily Brief. Read-only.
3. **Phase 3 — Founder Console UI**: the `/ceo` page first, consuming the internal API.
4. **Phase 5 — Per-layer workflows**: each generator gets a daily / weekly schedule.

Each subsequent PR should flip a layer's verifier from "anchor PASS" to "deep PASS" by adding sub-checks for the new artifacts that PR introduces.
