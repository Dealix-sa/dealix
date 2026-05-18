# Dealix Readiness Control Center

**لا تثق بالإحساس. ثق بنظام التحقق.**  
**نظام التشغيل اليومي:** [`docs/company/DEALIX_OPERATING_KERNEL.md`](docs/company/DEALIX_OPERATING_KERNEL.md) — [`docs/company/DECISION_RULES.md`](docs/company/DECISION_RULES.md) — مراجعة أسبوعية [`docs/company/WEEKLY_OPERATING_REVIEW.md`](docs/company/WEEKLY_OPERATING_REVIEW.md) — [`docs/company/SERVICE_REGISTRY.md`](docs/company/SERVICE_REGISTRY.md).  
سياق السوق: [McKinsey — The State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/) — [Gartner — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

المرجع: [`docs/company/DEALIX_STAGE_GATES_AR.md`](docs/company/DEALIX_STAGE_GATES_AR.md).

**الإطلاق الرسمي:** قرار go/no-go ومتتالية التدشين في [`docs/LAUNCH_GO_LIVE_RUNBOOK.md`](docs/LAUNCH_GO_LIVE_RUNBOOK.md) — إجراءات المؤسس في [`docs/FOUNDER_LAUNCH_ACTIONS.md`](docs/FOUNDER_LAUNCH_ACTIONS.md).
**Official launch:** go/no-go decision and launch sequence live in the runbook; founder-only actions in the action checklist.

التحقق الآلي:

```bash
python scripts/verify_dealix_ready.py
python scripts/verify_dealix_ready.py --skip-tests
```

---

## Company Status

| Field | Value |
|-------|--------|
| **Current Stage** | (مثال: Gate 6 Pass — جاهز للبيع للخدمات الثلاث الأولى) |
| **Officially Sellable Services** | |
| **Services in Beta** | (Score 70–84 أو ناقص demo فقط) |
| **Services Not Ready** | (أقل من 70 أو hard fail) |

---

## Gate Scores (يدوي: نقاط / آلي: راجع مخرجات السكربت)

| Gate | الاسم | قرار (PASS / FIX / BLOCKED) | Score يدوي / ملاحظة |
|------|--------|-----------------------------|---------------------|
| 0 | Founder Clarity | | /100 (Pass ≥ 85) |
| 1 | Offer Readiness | | /100 (Pass ≥ 85 لكل عرض) |
| 2 | Delivery Readiness | | /100 (Pass ≥ 85) |
| 3 | Product Readiness | | /100 (Pass ≥ 80 MVP) |
| 4 | Governance Readiness | | /100 (Pass ≥ 90) |
| 5 | Demo Readiness | | /100 (Pass ≥ 85) |
| 6 | Sales Readiness | | /100 (Pass ≥ 85) |
| 7 | Client Delivery Readiness | | |
| 8 | Retainer Readiness | | /100 (Pass ≥ 85) |
| 9 | Scale Readiness | | /100 (Pass ≥ 85) |
| 10 | World-Class Readiness | | (معيار طموح — انظر [`docs/company/WORLD_CLASS_READINESS_AR.md`](docs/company/WORLD_CLASS_READINESS_AR.md)) |

**قرار ثلاثي:** `PASS` → انتقل | `FIX` → أصلح ثم أعد التقييم | `BLOCKED` → لا بيع ولا توسع حتى تُزال المعرقلات.

---

## Official Services

1. Lead Intelligence Sprint — `docs/services/lead_intelligence_sprint/`
2. AI Quick Win Sprint — `docs/services/ai_quick_win_sprint/`
3. Company Brain Sprint — `docs/services/company_brain_sprint/`

## Do Not Sell Yet

1.
2.
3.

## Critical Gaps

تم التحقق منها بتاريخ 2026-05-18 / Verified 2026-05-18:

1. **P0 — Moyasar KYC غير مُفعّل:** لا يمكن تحصيل مدفوعات حية حتى يكمل المؤسس توثيق حساب ميسر. (Moyasar account KYC inactive — no live payment until founder completes verification.)
2. **P1 — واجهة الـconsole غير منشورة:** تطبيق Next.js في `frontend/` يبني ويجتاز فحص الأنواع بنجاح لكنه غير منشور على مضيف. (Next.js console builds + typechecks clean but is not deployed.)
3. **P1 — مراقبة الإنتاج ناقصة:** `SENTRY_DSN` و UptimeRobot و `RESEND_API_KEY` غير مضبوطة (الكود يتدهور بأمان حتى تُضبط). (Production monitoring not yet configured — code degrades gracefully.)
4. **P2 — دين فني في الاختبارات:** ~59 اختبار خلفي فاشل مسبقًا على `main` (اختبارات تعتمد على البيئة + اختبارات قديمة غير متزامنة مع الكود) — بوابة CI السريعة خضراء (94 نجح). (~59 pre-existing backend test failures on main; the required CI quick-regression gate is green.)

## Next Build Decisions

1. أكمل بنود **P0** في [`docs/FOUNDER_LAUNCH_ACTIONS.md`](docs/FOUNDER_LAUNCH_ACTIONS.md) قبل قبول أول عميل يدفع.
2. انشر الـconsole واربط نطاقًا فرعيًا (مثل app.dealix.me).
3. خصّص جلسة تنظيف للاختبارات الخلفية الفاشلة مسبقًا (خارج نطاق الإطلاق لكنه دين يجب سداده).

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـMVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/) · [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/) · [`demos/company_brain_demo/`](demos/company_brain_demo/)
