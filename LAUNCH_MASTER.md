# Dealix — Launch Master

**Date:** 2026-05-22
**Branch:** `claude/strategic-launch-6FSvK`
**Status:** Technically launched · `DEALIX_READY_FOR_SALES=true` · Revenue verification blocked on founder-only Moyasar KYC.

> This file is the single entry point for the strategic launch. **It links; it does not copy.** Every claim here traces to a source file under this repo.

---

## 1. Launch Verdict

| Signal | Value | Source |
|---|---|---|
| `DEALIX_READY_FOR_SALES` | **true** | `scripts/verify_dealix_ready.py` (run 2026-05-22) |
| Decision | **`SELL_READY_STACK`** | same |
| Gates 0-8 | **all PASS** | [`DEALIX_READINESS.md`](DEALIX_READINESS.md) |
| Tests (verifier subset) | **16/16 passed** | same |
| Sellable services (readiness ≥ 85) | **6/6** | same |
| Missing gate files | **0** | same |
| Gates 9-10 (Scale, World-Class) | NOT EVALUATED | manual assessment after first 10 customers |

Honest framing: the **technical** stack is sell-ready. The **revenue** stack is blocked on the founder-only items in §4.

---

## 2. Done / Automatable — already in this repo

| Area | State | Canonical source |
|---|---|---|
| Backend production | ✅ live at `https://api.dealix.me` | [`DEALIX_COMPANY_OPERATIONAL_STATE.md`](DEALIX_COMPANY_OPERATIONAL_STATE.md) |
| Landing site | ✅ live at `https://dealix.me` | same |
| 161 FastAPI routers mounted | ✅ | `api/main.py` |
| Product packages (data_os, revenue_os, knowledge_os, governance_os, reporting_os, delivery_os) | ✅ code present | `auto_client_acquisition/` |
| 6 sellable services with readiness ≥ 85 | ✅ | [`DEALIX_READINESS.md`](DEALIX_READINESS.md) §Official Services |
| Gate docs (delivery, sales, demos) | ✅ all present | `docs/delivery/`, `docs/sales/`, `demos/` |
| Demo packs (3 sprints) | ✅ all 24 files | `demos/lead_intelligence_demo/`, `demos/ai_quick_win_demo/`, `demos/company_brain_demo/` |
| Test suite | ✅ 16/16 in verifier subset | `tests/` |
| Outreach content (LinkedIn DMs, agency DMs, follow-ups) | ✅ send-ready Arabic | [`docs/ops/launch_content_queue.md`](docs/ops/launch_content_queue.md) |
| Today's send queue (5/hour cap) | ✅ | [`docs/ops/today_send_queue.md`](docs/ops/today_send_queue.md) |
| Pipeline tracker (CSV, 50 leads seeded) | ✅ | `docs/ops/pipeline_tracker.csv` |
| Partner kit + agency targets | ✅ | `docs/ops/partner_send_queue.md`, `docs/ops/agency_partner_kit.md` |
| Scheduled healthcheck → auto-creates P0 issue on failure | ✅ | `.github/workflows/scheduled_healthcheck.yml` |
| CRM + content + scorecard | ✅ template | `docs/ops/COMPANY_CONTROL_CENTER.md`, `docs/ops/daily_scorecard.md` |
| Manual payment path (interim) | ✅ ready | `docs/ops/MANUAL_PAYMENT_SOP.md` |

**Doctrine guard kept:** the 11 non-negotiables are enforced by `tests/test_no_*.py` and `.claude/agents/dealix-pm.md` §Non-negotiables. No fake KPIs, no fabricated evidence, no automated cold outreach.

---

## 3. Founder-Only Manual Actions

These are the **only** blockers between current state and `REVENUE VERIFIED`. None can be automated by an in-repo agent (each requires Sami's identity, dashboard access, or a personal LinkedIn account).

→ **See [`FOUNDER_LAUNCH_ACTIONS.md`](FOUNDER_LAUNCH_ACTIONS.md)** for the precise step-by-step list.

Summary of the 5 critical-path items:

1. **Moyasar KYC** — unlocks live payments (1-3 business days). Instant unblock: sandbox `sk_test_` key.
2. **Sentry DSN** — 5 minutes, unlocks production error tracking.
3. **UptimeRobot monitor** — 10 minutes, external uptime check.
4. **First LinkedIn DMs** — 3 minutes each, manual send only (no automation — non-negotiable #3).
5. **PostHog real key** (if still using placeholder).

---

## 4. Offers & Pricing — Canonical for Launch

The launch uses the **SaaS plans** as canonical pricing (confirmed 2026-05-22):

| Plan | Price (SAR) | Use |
|---|---|---|
| **Pilot** | 1 (refundable, 7 days) | proof-of-flow trial |
| **Starter** | 999 / month | small B2B teams |
| **Growth** | 2,999 / month | mid-market B2B |
| **Scale** | 7,999 / month | enterprise |

**Source:** [`docs/ops/COMPANY_CONTROL_CENTER.md`](docs/ops/COMPANY_CONTROL_CENTER.md) §§5, 12 · landing pricing page · founder confirmation.

**Open decision (not blocking):** [`docs/company/OFFER_LADDER.md`](docs/company/OFFER_LADDER.md) lists consulting-service price ranges (Diagnostic 3.5-7.5k, Sprint 7.5-25k, etc.) — these are **services**, not SaaS plans. The two are not contradictory in nature but need to be reconciled into a single offer page after the first 10 customers.

The 5-rung agent-defined ladder (Free Diagnostic / 499 Sprint / 1,500 Pack / 2,999-4,999 Managed / 5K-25K Custom) in `.claude/agents/dealix-pm.md` is *aspirational* and **not** the launch's selling prices. To be reconciled in a follow-up.

---

## 5. Operating Loop (daily / weekly)

| When | What | File |
|---|---|---|
| Every morning (60 min) | TODAY command page | [`docs/ops/TODAY.md`](docs/ops/TODAY.md) |
| All day | Decision state dashboard | [`docs/ops/COMPANY_CONTROL_CENTER.md`](docs/ops/COMPANY_CONTROL_CENTER.md) |
| Hourly during work | Daily operating loop | [`docs/ops/DAILY_OPERATING_LOOP.md`](docs/ops/DAILY_OPERATING_LOOP.md) |
| Stage transitions | 3 customers/day math | [`docs/ops/THREE_CUSTOMERS_PER_DAY_OPERATING_MODEL.md`](docs/ops/THREE_CUSTOMERS_PER_DAY_OPERATING_MODEL.md) |
| When a prospect says yes | 15-min close-to-paid | [`docs/ops/FIRST_REVENUE_ATTEMPT.md`](docs/ops/FIRST_REVENUE_ATTEMPT.md) |
| First 10 customers | Manual delivery template | [`docs/ops/FIRST_CUSTOMER_DELIVERY_TEMPLATE.md`](docs/ops/FIRST_CUSTOMER_DELIVERY_TEMPLATE.md) |
| End of day | Daily scorecard | [`docs/ops/daily_scorecard.md`](docs/ops/daily_scorecard.md) |

Sending rule across all queues: **manual only, max 5/hour, reply within 30 minutes.** Automating LinkedIn or WhatsApp outreach violates non-negotiables #2 and #3.

---

## 6. Open Blockers & Risks

| # | Blocker | Owner | Unblock | ETA |
|---|---|---|---|---|
| 1 | Moyasar KYC | Sami | Complete dashboard KYC OR send sandbox `sk_test_` key | 1-3 days OR instant |
| 2 | `SENTRY_DSN` empty | Sami | Create Sentry project → send DSN | 5 min |
| 3 | First LinkedIn DM not sent | Sami | Open LinkedIn → paste from `today_send_queue.md` → send | 3 min |
| 4 | UptimeRobot not configured | Sami | Add HTTPS monitor on `/health` (10 min) | 10 min |
| 5 | PostHog placeholder key on landing (if still) | Sami | Send real PostHog key | 2 min |
| 6 | Offer doctrine drift (`OFFER_LADDER.md` vs SaaS plans) | Founder decision | Reconcile post first 10 customers | non-blocking |

None of these block **selling today** via the manual payment path. The first 5 only block "fully automated revenue."

---

## 7. Automatable / In-Repo ⇆ Founder-Only Manual

| Automatable in this repo | Founder-only (cannot be automated) |
|---|---|
| Code + tests + verification | Moyasar dashboard KYC submission |
| Doctrine + readiness scorecard | Sentry project creation + DSN copy |
| Outreach content drafts (Arabic, send-ready) | UptimeRobot monitor creation |
| Pipeline + scorecard CSVs | Sending the actual LinkedIn DM (manual per non-negotiable #3) |
| Manual payment SOP + Moyasar invoice generator | Receiving wire/STC Pay confirmation |
| 90-day plan, weekly review, scorecard templates | Customer kickoff calls, demo runs, founder voice |
| Healthcheck workflow + DLQ + reconciliation | Replying to inbound within 30 min |

---

## 8. Document Map (entry-point + canonicals)

| Area | Canonical file |
|---|---|
| **Launch entry point (you are here)** | `LAUNCH_MASTER.md` |
| Founder action list (manual blockers) | `FOUNDER_LAUNCH_ACTIONS.md` |
| Readiness scorecard | `DEALIX_READINESS.md` |
| Live operational state | `DEALIX_COMPANY_OPERATIONAL_STATE.md` |
| Daily command page | `docs/ops/TODAY.md` |
| Decision-state dashboard | `docs/ops/COMPANY_CONTROL_CENTER.md` |
| Outreach content | `docs/ops/launch_content_queue.md` |
| Today's send queue | `docs/ops/today_send_queue.md` |
| Pipeline tracker | `docs/ops/pipeline_tracker.csv` |
| Manual payment SOP | `docs/ops/MANUAL_PAYMENT_SOP.md` |
| Moyasar KYC checklist | `docs/ops/MOYASAR_KYC_CHECKLIST.md` |
| Sentry setup | `docs/ops/SENTRY_SETUP.md` |
| UptimeRobot setup | `docs/ops/UPTIMEROBOT_SETUP.md` |
| Sales playbook | `docs/sales/SALES_PLAYBOOK.md` |
| 11 non-negotiables (source of truth) | `.claude/agents/dealix-pm.md` §Non-negotiables |
| Stage gates (Arabic) | `docs/company/DEALIX_STAGE_GATES_AR.md` |
| Verification command | `python scripts/verify_dealix_ready.py` |

---

## Verification

To reproduce the launch verdict from a clean checkout:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
python scripts/verify_dealix_ready.py            # full
python scripts/verify_dealix_ready.py --skip-tests  # gates only
```

Expected on 2026-05-22: `DEALIX_READY_FOR_SALES=true`, all 9 gates PASS, 16/16 tests pass, decision `SELL_READY_STACK`.
