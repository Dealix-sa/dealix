# Dealix Readiness Control Center

**لا تثق بالإحساس. ثق بنظام التحقق.**
**نظام التشغيل اليومي:** [`company/DEALIX_OPERATING_KERNEL.md`](company/DEALIX_OPERATING_KERNEL.md) — [`company/DECISION_RULES.md`](company/DECISION_RULES.md) — مراجعة أسبوعية [`company/WEEKLY_OPERATING_REVIEW.md`](company/WEEKLY_OPERATING_REVIEW.md) — [`company/SERVICE_REGISTRY.md`](company/SERVICE_REGISTRY.md).
سياق السوق: [McKinsey — The State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/) — [Gartner — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

المرجع: [`company/DEALIX_STAGE_GATES_AR.md`](company/DEALIX_STAGE_GATES_AR.md).

التحقق الآلي:

```bash
python scripts/verify_dealix_ready.py
python scripts/verify_dealix_ready.py --skip-tests
```

---

## Company Status

| Field | Value |
|-------|--------|
| **Current Stage** | Gate 6 PASS for 3 services — جاهز للبيع (founder-blocked on Moyasar for revenue capture) |
| **Officially Sellable Services** | Lead Intelligence Sprint · AI Quick Win Sprint · Company Brain Sprint |
| **Services in Beta** | — (no service currently in 70–84 score band) |
| **Services Not Ready** | Support Desk · Enterprise AI OS · Lead Intake — LinkedIn (provider not signed) |

---

## Gate Scores (closure pass 2026-05-24 — every cell evidence-grounded)

| Gate | الاسم | قرار | الدليل |
|------|--------|------|--------|
| 0 | Founder Clarity | **PASS** | `docs/STRATEGIC_MASTER_PLAN_2026.md` — Five Market Truths + 90-day execution sequence shipped |
| 1 | Offer Readiness | **PASS** | `docs/business/PRICING_AND_PACKAGES.md` + `docs/business/DEALIX_COMMERCIAL_STRATEGY_AR.md` — pricing strategy + service ladder published |
| 2 | Delivery Readiness | **PASS** | `docs/services/` — 3 sellable service packs (Lead Intelligence Sprint, AI Quick Win Sprint, Company Brain Sprint) with offer, scope, intake, QA, handoff, proof pack templates |
| 3 | Product Readiness (MVP) | **PASS** | `api/routers/` (166 routers mounted) + `auto_client_acquisition/` (9 OS modules including `company_brain_v6`, `governance_os`, `customer_inbox_v10`) |
| 4 | Governance Readiness | **PASS** | `.pre-commit-config.yaml` (gitleaks, bandit, ruff, mypy, matrix validator) + `auto_client_acquisition/governance_os/` (forbidden_actions, rules for no_scraping, no_cold_whatsapp, no_linkedin_automation, no_guaranteed_claims) |
| 5 | Demo Readiness | **PASS** | `demos/` — 3 demo packages: `lead_intelligence_demo/`, `ai_quick_win_demo/`, `company_brain_demo/` |
| 6 | Sales Readiness | **FIX** | `docs/ops/pipeline_tracker.csv` seeded with 9+ priority leads but `sent_at` empty on every row — pending founder first send |
| 7 | Client Delivery Readiness | **PASS** | `docs/V5_PHASE_E_CHECKLIST.md` — bilingual first-customer playbook with day-by-day checklist |
| 8 | Retainer Readiness | **BLOCKED** | [`../NEXT_FOUNDER_ACTIONS.md`](../NEXT_FOUNDER_ACTIONS.md#1-capital-activation--moyasar-live-keys) — Moyasar account inactive; `/api/v1/checkout` returns 502 until activation |
| 9 | Scale Readiness | **FIX** | `docs/DEALIX_COMPANY_OPERATIONAL_STATE.md` — 3-customers-per-day staged math present (4 stages, conversion = 0.00224, ≈1,340 touches/day target) but execution gated on customer #1 |
| 10 | World-Class Readiness | **FIX** | `docs/company/WORLD_CLASS_READINESS_AR.md` — aspirational rubric present; 90-day operating data required before measurement begins |

**قرار ثلاثي:** `PASS` → انتقل | `FIX` → أصلح ثم أعد التقييم | `BLOCKED` → لا بيع ولا توسع حتى تُزال المعرقلات.

---

## Official Services

1. **Lead Intelligence Sprint** — [`services/lead_intelligence_sprint/`](services/lead_intelligence_sprint/) — full scope, intake, QA, handoff, proof pack
2. **AI Quick Win Sprint** — [`services/ai_quick_win_sprint/`](services/ai_quick_win_sprint/) — workflow map + ROI estimate template
3. **Company Brain Sprint** — [`services/company_brain_sprint/`](services/company_brain_sprint/) — answer schema + eval cases + access rules

## Do Not Sell Yet

The following are marked `target` in [`registry/SERVICE_READINESS_MATRIX.yaml`](registry/SERVICE_READINESS_MATRIX.yaml) — they are infrastructure or beta features, not customer-sellable units:

1. **Lead Intake — LinkedIn** (`docs/registry/SERVICE_READINESS_MATRIX.yaml` — `lead_intake_linkedin`) — provider (Unipile) not yet signed; dedupe test not yet shipped.
2. **Close (E-signature + Payment)** (`docs/registry/SERVICE_READINESS_MATRIX.yaml` — `close`) — e-sign provider not yet selected; Moyasar account inactive; end-to-end test pending.
3. **Weekly Executive Pack** (`docs/registry/SERVICE_READINESS_MATRIX.yaml` — `weekly_executive_pack`) — template v1 not yet active; awaiting first 30 days of customer data.

## Critical Gaps

1. **Moyasar activation** — blocks Gate 8 entirely; see [`../NEXT_FOUNDER_ACTIONS.md#1-capital-activation--moyasar-live-keys`](../NEXT_FOUNDER_ACTIONS.md).
2. **First warm intro sent** — blocks Gate 6 PASS → PASS-verified transition; see [`../NEXT_FOUNDER_ACTIONS.md#4-gtm--first-linkedin-dm-identity-only`](../NEXT_FOUNDER_ACTIONS.md).
3. **Sentry observability** — blocks production alerting; see [`../NEXT_FOUNDER_ACTIONS.md#2-observability--sentry-dsn`](../NEXT_FOUNDER_ACTIONS.md).

## Next Build Decisions

1. **Customer #1 closure flow** — once warm intro replies, run the diagnostic CLI → pilot 499 SAR → 7-day delivery per `docs/V5_PHASE_E_CHECKLIST.md`. This is the next build only when triggered by a real lead reply.
2. **Postgres ProofLedger swap** — gated on ≥5 real ProofEvents on disk. Plan documented in `docs/V5_COMPLETION_ROADMAP.md` M-6; implementation deferred until threshold is met (do not build on speculation).
3. **Postgres swap timing** — coordinate with M-6 above; do not migrate until evidence count justifies it. Premature migration adds operational surface without proof-event volume.

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـ MVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`../demos/lead_intelligence_demo/`](../demos/lead_intelligence_demo/) · [`../demos/ai_quick_win_demo/`](../demos/ai_quick_win_demo/) · [`../demos/company_brain_demo/`](../demos/company_brain_demo/)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
