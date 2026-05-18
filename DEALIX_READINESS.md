# Dealix Readiness Control Center

**لا تثق بالإحساس. ثق بنظام التحقق.**  
**نظام التشغيل اليومي:** [`docs/company/DEALIX_OPERATING_KERNEL.md`](docs/company/DEALIX_OPERATING_KERNEL.md) — [`docs/company/DECISION_RULES.md`](docs/company/DECISION_RULES.md) — مراجعة أسبوعية [`docs/company/WEEKLY_OPERATING_REVIEW.md`](docs/company/WEEKLY_OPERATING_REVIEW.md) — [`docs/company/SERVICE_REGISTRY.md`](docs/company/SERVICE_REGISTRY.md).  
سياق السوق: [McKinsey — The State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/) — [Gartner — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

المرجع: [`docs/company/DEALIX_STAGE_GATES_AR.md`](docs/company/DEALIX_STAGE_GATES_AR.md).

التحقق الآلي:

```bash
python scripts/verify_dealix_ready.py
python scripts/verify_dealix_ready.py --skip-tests
```

---

> **Last scored:** 2026-05-18 — workstream W4, Commercial Launch Plan (first-paid-pilot track).
> Scoring is from REAL script output, not feeling. Verification artifacts below.

### Verification run — 2026-05-18

| Script | Verdict | Key numbers |
|--------|---------|-------------|
| `python3 scripts/verify_dealix_ready.py --skip-tests` | **PASS** — `DEALIX_READY_FOR_SALES=true` | Gates 0–8 all `PASS`; `STARTER_SERVICES_OFFER_PASS=3/3` (all score 100); `MISSING_FILES=0`; decision `SELL_READY_STACK` |
| `bash scripts/dealix_capability_verify.sh` | **PASS** — `DEALIX_READY=true` | `READY_SERVICES=6/6`; 27 capability tests passed; service/governance/proof-pack/quality/sales-asset checks all `true` |
| `bash scripts/revenue_os_master_verify.sh` | **PASS** — `DEALIX_REVENUE_OS_VERDICT=PASS` | 73 revenue_os + decision-passport tests passed; all 14 signals `pass` (incl. all 5 doctrine non-negotiables); ruff `All checks passed` |

**Env note:** the three scripts share an isolated/uv-tool `pytest` on `PATH` that lacks the
project's test deps; the runs above were obtained after installing missing runtime/test
dependencies (`httpx`, `sqlalchemy`, `pydantic`, `redis`, `fastapi`, `python-jose`,
`pytest`, `pytest-asyncio`, `pytest-cov`, `email-validator`) and reinstalling `cffi`. A
pre-existing batch of 21 cosmetic `ruff` lint findings (import-sort + `encode("utf-8")`)
was auto-fixed under the freeze's CI-hygiene allowance — this is what flipped the revenue_os
verdict from `PARTIAL` to `PASS`. No product logic changed.

---

## Company Status

| Field | Value |
|-------|--------|
| **Current Stage** | **Gate 8 Pass** — sell-ready stack verified; under ACTIVE Commercial Freeze, North Star = first PAID pilot + customer-approved Proof Pack (L3+) |
| **Officially Sellable Services** | Lead Intelligence Sprint (100), AI Quick Win Sprint (100), Company Brain Sprint (100), AI Support Desk Sprint (90), AI Governance Program (100), Client AI Policy Pack (100) — all readiness ≥ 85 |
| **Services in Beta** | (none — no service scored 70–84) |
| **Services Not Ready** | (none below 70). Note: rungs 2–5 are *commercially frozen* (delivered founder-assisted, not fully managed) — not a readiness fail, a deliberate freeze. |

---

## Gate Scores (يدوي: نقاط / آلي: راجع مخرجات السكربت)

| Gate | الاسم | قرار (PASS / FIX / BLOCKED) | Score يدوي / ملاحظة |
|------|--------|-----------------------------|---------------------|
| 0 | Founder Clarity | **PASS** | `GATE0_PASS=true` — all positioning/mission/ICP/north-star docs present |
| 1 | Offer Readiness | **PASS** | `GATE1_PASS=true` — 3/3 starter services score 100 (≥ 85 bar) |
| 2 | Delivery Readiness | **PASS** | `GATE2_PASS=true` — all 6 delivery-standard docs present |
| 3 | Product Readiness | **PASS (MVP)** | `GATE3_PASS=true` — all 6 product `*_os` packages carry code; 73 revenue_os tests green |
| 4 | Governance Readiness | **PASS** | `GATE4_PASS=true` — governance rules + AI output quality both `true`; 5/5 doctrine non-negotiables `pass` |
| 5 | Demo Readiness | **PASS** | `GATE5_PASS=true` — all 24 demo-pack files + DEMO_SCRIPT present |
| 6 | Sales Readiness | **PASS** | `GATE6_PASS=true` — all 6 sales-kit docs present |
| 7 | Client Delivery Readiness | **PASS** | `GATE7_PASS=true` — client-onboarding pack complete |
| 8 | Retainer Readiness | **PASS** | `GATE8_PASS=true` — RETAINER_READINESS.md present |
| 9 | Scale Readiness | `insufficient_data` | No script-scored signal; explicitly out of scope under Commercial Freeze (do not scale before first paid pilot) |
| 10 | World-Class Readiness | `insufficient_data` | Aspirational bar — no automated score exists; not assessed |

**قرار ثلاثي:** `PASS` → انتقل | `FIX` → أصلح ثم أعد التقييم | `BLOCKED` → لا بيع ولا توسع حتى تُزال المعرقلات.

**Sell gate result:** gates 0,1,2,4,5,6 PASS **and** gate 3 PASS as MVP → the official
service stack is **sellable now**. `verify_dealix_ready.py` confirms `DEALIX_READY_FOR_SALES=true`,
decision `SELL_READY_STACK`.

---

## Official Services

1. Lead Intelligence Sprint — `docs/services/lead_intelligence_sprint/` — score 100 — **sellable**
2. AI Quick Win Sprint — `docs/services/ai_quick_win_sprint/` — score 100 — **sellable**
3. Company Brain Sprint — `docs/services/company_brain_sprint/` — score 100 — **sellable**

Also verified ≥ 85: AI Support Desk Sprint (90), AI Governance Program (100), Client AI
Policy Pack (100).

## Do Not Sell Yet

1. **Rungs 2–5** (Data-to-Revenue Pack, Managed Revenue Ops, Command Center, Partner OS) — not for readiness reasons, but because they are under the **ACTIVE Commercial Freeze** (`docs/ops/COMMERCIAL_FREEZE.md`); delivered today as founder-assisted tooling, not fully managed services.
2. Anything dependent on **live payments** — Moyasar account is not KYC-activated (`account_inactive_error`); no real charge can clear until founder completes `docs/ops/MOYASAR_KYC_CHECKLIST.md`.
3. Gate 9/10 scale claims — `insufficient_data`; do not market scale capability before the first paid pilot proves the motion.

## Critical Gaps

1. **Moyasar account not activated** — payment→delivery cannot be exercised with real money; the `sk_test_` key path lets the founder verify the full flow now without revenue (see Founder Action Checklist).
2. **First paid pilot not yet delivered** — the freeze's own exit condition is unmet; readiness is verified but commercially unproven (zero paid invoices, zero customer-approved Proof Packs).
3. **Founder-only blockers open** — first warm-intro messages not sent, SENTRY_DSN empty, UptimeRobot monitor not created. These gate revenue and only Sami can clear them — consolidated in `docs/ops/FOUNDER_ACTION_CHECKLIST.md`.

## Next Build Decisions

1. **No new build.** Commercial Freeze is ACTIVE — only founder-led selling, rung 0–1 delivery finish, and readiness/ledger recording are permitted.
2. Hold rung 2–5 automation until a real market signal triggers it (`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`).
3. Re-score this file after the first paid pilot closes; that event ends the freeze and unlocks the next 90-day plan.

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـMVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/) · [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/) · [`demos/company_brain_demo/`](demos/company_brain_demo/)
