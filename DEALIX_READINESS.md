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

## Company Status

| Field | Value |
|-------|--------|
| **Current Stage** | Gate 6 Pass + Gates 7, 8 Pass — `SELL_READY_STACK` |
| **Officially Sellable Services** | 6 خدمات (كلها بدرجة ≥ 90) |
| **Services in Beta** | (none) |
| **Services Not Ready** | (none) |
| **Last Verification** | 2026-05-22 · `python scripts/verify_dealix_ready.py` · exit 0 |

---

## Gate Scores (آلي من `scripts/verify_dealix_ready.py` — 2026-05-22)

| Gate | الاسم | قرار | ملاحظة |
|------|--------|------|--------|
| 0 | Founder Clarity | **PASS** | الملفات الخمسة موجودة + `DEALIX_READINESS.md` |
| 1 | Offer Readiness | **PASS** | 3/3 خدمات بداية ≥ 85 (كلها = 100) + service_files |
| 2 | Delivery Readiness | **PASS** | الملفات الستة في `docs/delivery/` |
| 3 | Product Readiness | **PASS** | جميع الحزم الستة في `auto_client_acquisition/` تحوي كود |
| 4 | Governance Readiness | **PASS** | `verify_governance_rules` + `verify_ai_output_quality` |
| 5 | Demo Readiness | **PASS** | حزم `demos/` الثلاث كاملة + `DEMO_SCRIPT.md` |
| 6 | Sales Readiness | **PASS** | 6 ملفات في `docs/sales/` |
| 7 | Client Delivery Readiness | **PASS** | 6 ملفات `docs/delivery/client_onboarding/` |
| 8 | Retainer Readiness | **PASS** | `docs/delivery/RETAINER_READINESS.md` |
| 9 | Scale Readiness | NOT EVALUATED | السكربت لا يقيّمها — تقييم يدوي مطلوب لاحقاً |
| 10 | World-Class Readiness | NOT EVALUATED | معيار طموح — انظر [`docs/company/WORLD_CLASS_READINESS_AR.md`](docs/company/WORLD_CLASS_READINESS_AR.md) |

**Tests:** PASS (16/16 من الـpytest subset المقيّد).
**MISSING_FILES:** 0.
**DEALIX_READY_FOR_SALES:** `true`.
**Decision:** `SELL_READY_STACK`.

**قرار ثلاثي:** `PASS` → انتقل | `FIX` → أصلح ثم أعد التقييم | `BLOCKED` → لا بيع ولا توسع حتى تُزال المعرقلات.

---

## Official Services (Sellable — readiness ≥ 85)

| # | Service | Folder | Score |
|---|---------|--------|------:|
| 1 | Lead Intelligence Sprint | `docs/services/lead_intelligence_sprint/` | 100 |
| 2 | AI Quick Win Sprint | `docs/services/ai_quick_win_sprint/` | 100 |
| 3 | Company Brain Sprint | `docs/services/company_brain_sprint/` | 100 |
| 4 | AI Support Desk Sprint | `docs/services/ai_support_desk_sprint/` | 90 |
| 5 | AI Governance Program | `docs/services/ai_governance_program/` | 100 |
| 6 | Client AI Policy Pack | `docs/services/client_ai_policy_pack/` | 100 |

## Do Not Sell Yet

(none — كل الخدمات الست عبرت العتبة)

## Critical Gaps

(لم يكشف المتحقق أي فجوة في 2026-05-22)

## Next Build Decisions

1. تنظيف doctrine drift في التسعير: `OFFER_LADDER.md` يحوي أرقاماً مختلفة عن `COMPANY_CONTROL_CENTER.md` (راجع `LAUNCH_MASTER.md` §5). قرار مفتوح، لا يحظر الإطلاق.
2. تقييم يدوي لـGate 9 (Scale Readiness) و10 (World-Class) بعد أول 10 عملاء.
3. متابعة المسار الحرج للمؤسس في `FOUNDER_LAUNCH_ACTIONS.md` (Moyasar KYC، Sentry، UptimeRobot).

---

## Verification Run — 2026-05-22

```
$ python scripts/verify_dealix_ready.py
... 16 passed in 0.73s
GATE0_PASS=true … GATE8_PASS=true
TESTS_PASS=true
DEALIX_READY_FOR_SALES=true
Decision: SELL_READY_STACK
```

(المخرج الكامل محفوظ في `/tmp/launch/verify_full.log` أثناء التشغيل؛ لإعادة الإنتاج: شغّل الأمر أعلاه.)

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـMVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/) · [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/) · [`demos/company_brain_demo/`](demos/company_brain_demo/)
