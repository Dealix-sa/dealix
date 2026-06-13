# Dealix Official Private-Launch Decision — قرار الإطلاق الخاص الرسمي

<!-- Owner: Founder | Date: 2026-06-07 | Arabic primary — العربية أولاً -->
<!-- Status record. Cross-references canon; does not duplicate the 30-gate matrix. -->

> **قاعدة:** لا ادعاء "أُطلِق" (launched) قبل إغلاق ≥ 24/30 بوابة من
> [`docs/LAUNCH_GATES.md`](../LAUNCH_GATES.md) بما فيها بوابة **G5 — أول صفقة مدفوعة**.
> هذا الملف يسجّل قرار **الإطلاق الخاص** (Private Launch) فقط.
>
> **Rule:** no "launched" claim before ≥ 24/30 gates in `docs/LAUNCH_GATES.md`
> are closed, including **G5 — first paid deal**. This document records the
> **Private Launch** decision only.

---

## 1. القرار — Verdict

| المسار / Track | القرار / Verdict | الشرط / Condition |
|---|---|---|
| **الإطلاق الخاص / Private Launch** | **GO مشروط / Conditional GO** | بعد خضرة بوابات الكود + إكمال المؤسس للخطوات اليدوية (§4) |
| **الإطلاق العام / Public Launch** | **NO-GO** | حتى أول إثبات مدفوع (G5) و ≥ 24/30 بوابة |

**الإطلاق الخاص** = عروض خاصة، تشخيص مجاني، Sprint مدفوع بـ 499 ريال لقائمة دافئة
بموافقة المؤسس. لا حملة عامة، ولا إرسال آلي.

**Private Launch** = private demos, free diagnostic, paid 499 SAR sprint to an
approved warm list with founder approval. No public campaign, no automated sends.

---

## 2. حالة الـ PRs المرشّحة — Candidate PR state

*(قُرئت من GitHub مباشرة بتاريخ 2026-06-07 / read live from GitHub)*

| PR | العنوان | الحالة | الأساس | ملاحظة |
|---|---|---|---|---|
| **#638** | Claude Code workflow + `CLAUDE.md` | open · **draft** · unstable | `main@7bd43c3` | يحتاج `ANTHROPIC_API_KEY` (سر يدوي) قبل أن يعمل `@claude` |
| **#650** | green doctrine/governance gates + canonical `/health` | open · **draft** · unstable | `main@7bd43c3` | 137 doctrine-guard مرّت؛ يؤكد `/health` و`/health/deep` كنقاط رسمية؛ ~9 drift تحتاج قرار منتج |

كلاهما **مسودة غير مدموجة**. الدمج إلى `main` قرار مؤسس — لا ينفّذه وكيل.
Both are **unmerged drafts**. Merging to `main` is a founder-only decision.

---

## 3. بوابات الكود المطلوبة — Required code gates

شغّلها دفعة واحدة عبر / run them in one shot via:

```bash
bash scripts/dealix_close_now.sh
```

| البوابة / Gate | كيف تتحقق / How |
|---|---|
| `make doctor` | env contract + single alembic head + security smoke |
| `make env-check` | عقد `.env.example` |
| `make security-smoke` | فحص أمني بدون تبعيات |
| `make api-contract-check` | عقد OpenAPI (لا مسارات محذوفة) |
| `make test` | حزمة الاختبارات |
| `make prod-verify` | حزمة جاهزية الإنتاج الرسمية |
| `/health` → 200 | `api/routers/health.py` (نقطة liveness الرسمية) |
| `/health/deep` → 200 | فحص DB/Redis/LLM/DLQ |
| `/api/v1/pricing/plans` → 200 | `api/routers/pricing.py` |
| production smoke | `make production-smoke PRODUCTION_BASE_URL=…` |

البوابة الأعمق للإطلاق: [`scripts/official_launch_verify.sh`](../../scripts/official_launch_verify.sh)
(انظر [`PHASE_C_PRODUCTION_LAUNCH_AR.md`](PHASE_C_PRODUCTION_LAUNCH_AR.md) و
[`RELEASE_READINESS_CHECKLIST.md`](RELEASE_READINESS_CHECKLIST.md)).

---

## 4. خطوات المؤسس فقط — Founder-only blockers

لا ينفّذها أي وكيل (المبدأ #8: لا إجراء خارجي بدون موافقة). تُنفَّذ يدوياً:

- [ ] دمج PR #638 ثم إضافة `ANTHROPIC_API_KEY` في GitHub Secrets.
- [ ] مراجعة + دمج PR #650 بعد خضرة البوابات.
- [ ] حماية `main` (ruleset: PR + مراجعة + status checks + linear history + block force-push).
- [ ] إنشاء بيئات GitHub: `staging` و `production` (مراجِعون مطلوبون للإنتاج، فرع `main` فقط).
- [ ] أسرار الإنتاج (`DATABASE_URL`, `APP_SECRET_KEY`, `JWT_SECRET_KEY`, `MOYASAR_*`, `SMTP_*`, `RAILWAY_TOKEN` …) — كل قيمة سر مستقل، لا JSON واحد كبير.
- [ ] DNS/TLS موثّق يدوياً.
- [ ] Moyasar live (KYC + التبديل من test) موثّق يدوياً + اختبار webhook.
- [ ] اعتماد قائمة العملاء الدافئة وأول سكربت ديمو.
- [ ] لا رسالة عميل خارجية ولا دفعة حية بدون موافقة صريحة.

تتبّع الخطوات الخارجية مرتبط بـ #467–#471 (انظر وصف PR #650 §4).

---

## 5. نطاق الإطلاق الخاص — Allowed now / Not allowed yet

**مسموح الآن / Allowed:** عروض خاصة · تشخيص مجاني · Sprint 499 ريال · تشغيل تجريبي
(dry-run) · workflows بموافقة أولاً · تسجيل نقاط داخلي · ادعاءات مدعومة بأدلة · Proof Packs.

**غير مسموح بعد / Not yet:** إطلاق عام · أتمتة واتساب باردة · scraping بدون أساس نظامي ·
ادعاء إيراد مضمون · دفعات حية ذاتية · التزامات خارجية ذاتية · ادعاء امتثال كامل بدون دليل.

---

## 6. خطة التراجع — Rollback

1) تعطيل workflow الإنتاج. 2) إرجاع آخر commit إصدار. 3) تعطيل مداخل
`checkout`/`payment`. 4) تدوير الأسرار المتأثرة. 5) تجميد الـ workflows الخارجية.
6) نشر مذكرة حادثة داخلية. 7) استعادة آخر نشر سليم معروف (`.last_good_sha`).

---

## 7. خطة أول إيراد — First-revenue plan (reconciled with canon)

متوافقة مع [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) — المصدر الرسمي للأسعار:

| الدرجة / Rung | العرض | السعر |
|---|---|---|
| 0 | تشخيص مجاني / Free AI Ops Diagnostic | 0 |
| **1** | **7-Day Revenue Proof Sprint** (الدخول) | **499 SAR** |
| 2 | Data-to-Revenue Pack | 1,500 SAR |
| 3 | Managed Revenue Ops | 2,999–4,999 SAR/شهر |
| 4 | Executive Command Center (بعد 3 pilots) | 7,500–15,000 SAR/شهر |

- **القطاع المستهدف:** شركات خدمات B2B في السعودية.
- **عرض الدخول:** 7-Day Revenue Proof Sprint بـ 499 ريال (دفع 50/50 — انظر
  [`.claude/agents/dealix-sales.md`](../../.claude/agents/dealix-sales.md)).
- **الهدف:** أول Sprint مدفوع + أول Proof Pack + اقتراح ترقية.
- **حزمة "Command Sprint" الخاصة:** [`sales/COMMAND_SPRINT_OFFER.md`](../../sales/COMMAND_SPRINT_OFFER.md).
- **قائمة الاستهداف:** [`sales/FIRST_50_TARGET_ACCOUNTS.csv`](../../sales/FIRST_50_TARGET_ACCOUNTS.csv)
  + القائمة الدافئة القائمة [`pipeline_tracker.csv`](pipeline_tracker.csv).

> ملاحظة تسعير: "7,500–15,000 ريال" هو سعر **شهري** للدرجة 4 (Executive Command
> Center) ويُفتح بعد 3 pilots — وليس Sprint لمرة واحدة. لا يُقدَّم كعرض دخول.

---

## مراجع — Cross-links

- [`docs/LAUNCH_GATES.md`](../LAUNCH_GATES.md) — مصفوفة الـ 30 بوابة (canon)
- [`docs/ops/RELEASE_READINESS_CHECKLIST.md`](RELEASE_READINESS_CHECKLIST.md)
- [`docs/ops/PHASE_C_PRODUCTION_LAUNCH_AR.md`](PHASE_C_PRODUCTION_LAUNCH_AR.md)
- [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)
- [`scripts/dealix_close_now.sh`](../../scripts/dealix_close_now.sh) ·
  [`scripts/official_launch_verify.sh`](../../scripts/official_launch_verify.sh)

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
