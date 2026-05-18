# Dealix Proposal System — نظام العروض
<!-- Canonical pricing: docs/OFFER_LADDER_AND_PRICING.md (single source of truth) -->

لا تُرسل عروضاً عشوائية. استخدم بنية واحدة في كل مرة، وسعراً واحداً من السلم الرسمي فقط.
كل عرض **bilingual** (عربي أولاً)، **draft-only** حتى موافقة المؤسس، ولا يحتوي ادعاءات مضمونة.

> مصدر الحقيقة للأسعار: [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).

---

## كل عرض يجب أن يحتوي — Every proposal must include

1. النطاق المحدود — bounded Scope
2. الاستثناءات — Exclusions (الممنوعات الـ11)
3. السعر + شروط الدفع 50/50 (50% عند القبول، 50% عند تسليم Proof Pack)
4. وعد مقياس الإثبات — proof score target ≥ 80، أصل رأسمالي ≥ 1
5. مسار الـ Retainer بعد Sprint
6. إخلاء المسؤولية: "النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes"

### الاستثناءات الـ11 (تظهر في كل عرض) — The 11 non-negotiables

1. لا cold outreach على أي قناة. 2. لا أتمتة LinkedIn. 3. لا scraping.
4. لا إرسال جماعي (bulk). 5. لا ادعاءات مبيعات مضمونة ("نضمن"/"guaranteed"/"10x").
6. لا proof/metrics مزيّفة. 7. لا إرسال خارجي بدون موافقة المؤسس الصريحة.
8. لا قوائم مشتراة. 9. لا تجاوز PDPL / قابلية التواصل. 10. لا استشارات قانونية.
11. لا إرسال تلقائي — كل تواصل draft-only.

---

## القالب الموحّد — Unified proposal template

```markdown
# Proposal: [Rung N — Offer Name]

## Client Goal — هدف العميل
## Problem — المشكلة
## Proposed Engagement — ما سيُسلَّم
## Scope — النطاق
  **Included — المتضمَّن:** ...
  **Excluded — المستثنى:** (الاستثناءات الـ11) ...
## Timeline — الجدول
## Client Responsibilities — مسؤوليات العميل
## Price & Payment — السعر والدفع (50% قبول / 50% تسليم)
## Success Metric — مقياس النجاح (proof score >= 80, capital asset >= 1)
## Retainer Path — مسار الترقية
## Governance — الحوكمة
## Disclaimer — النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed
## Next Step — الخطوة التالية
```

نسخة إعادة الاستخدام في الكود: `docs/templates/PROPOSAL_BODY.md` (تُبقى متزامنة مع هذا القسم).

---

## قوالب الدرجات الست — Per-rung proposal templates

### Rung 0 — Free AI Ops Diagnostic (مجاني)

- **العميل المستهدف:** أي مؤسس B2B سعودي مهتم.
- **المخرجات:** تقرير تشخيصي صفحة واحدة + 3 أولويات + توصية الخطوة التالية.
- **المدخلات:** 6 أسئلة عبر `/diagnostic.html` (15 دقيقة).
- **الاستثناءات:** لا وعود ROI، لا تقارير متقدمة، لا وصول للمنصة.
- **السعر:** مجاني — لا دفع.
- **مسار الترقية:** → Rung 1 — 7-Day Revenue Proof Sprint (499 SAR).
- نمط التسليم: منتج مُتحقَّق منه.

### Rung 1 — 7-Day Revenue Proof Sprint (499 SAR)

عرض كامل جاهز: [`PROPOSAL_REVENUE_PROOF_SPRINT.md`](PROPOSAL_REVENUE_PROOF_SPRINT.md).

- **المخرجات:** تشخيص مفصل، 5 مسودات رسائل (draft-only)، Proof Pack يوم 7، تقرير تنفيذي، خطة 30 يوماً.
- **السعر:** 499 SAR (دفع واحد) — 50% قبول / 50% تسليم Proof Pack.
- **مقياس النجاح:** فرصة ≥ 1 موثقة، proof score ≥ 80، رضا ≥ 4/5.
- **الترقية:** → Rung 2 (1,500) أو Rung 3 (2,999–4,999/شهر).
- نمط التسليم: منتج مُتحقَّق منه.

### Rung 2 — Data-to-Revenue Pack (1,500 SAR)

- **العميل المستهدف:** شركة B2B لديها بيانات عملاء/مبيعات غير مستثمرة، تحتاج معالجة PII.
- **المخرجات:** تحليل pipeline كامل، خريطة فرص مرتبة، 10 مسودات استهداف، تقرير ROI basis، playbook مبيعات مخصص.
- **المدخلات:** CRM export أو Excel، 3 شهور بيانات مبيعات، وصف ICP الحالي.
- **الاستثناءات:** لا scraping، لا تكامل CRM مباشر.
- **السعر:** 1,500 SAR (مشروع واحد) — 50% قبول / 50% تسليم.
- **مقياس النجاح:** فرصة ≥ 1 موثقة، playbook معتمد من العميل.
- **الترقية:** → Rung 3 — Managed Revenue Ops.
- نمط التسليم: بقيادة المؤسس.

### Rung 3 — Managed Revenue Ops (2,999–4,999 SAR/شهر)

- **شرط الدخول:** proof score ≥ 80 + adoption ≥ 70 + workflow owner واضح.
- **المخرجات:** تقرير أسبوعي تنفيذي، ≤20 مسودة تواصل/شهر (معتمدة)، Proof Pack شهري، تقرير KPIs، جلسة استراتيجية شهرية 60 دقيقة.
- **الاستثناءات:** ≤20 مسودة/شهر، لا إرسال تلقائي، لا استشارات قانونية.
- **السعر:** 2,999–4,999 SAR/شهر (اشتراك) — أول شهر 50% قبول / 50% بعد أول Proof Pack شهري.
- **الترقية:** → Rung 4 — Executive Command Center.
- نمط التسليم: **بقيادة المؤسس / شبه-مؤتمت — founder-assisted / semi-automated** (يُفصح عنه للعميل).

### Rung 4 — Executive Command Center (7,500–15,000 SAR/شهر)

- **شرط الدخول:** ≥ 3 pilots مكتملة + ≥ 1 case study موثق.
- **المخرجات:** تقرير يومي تنفيذي، رادار سوق أسبوعي، مسودات شهرية كاملة، Proof Pack كامل، استراتيجية نمو ربعية، وصول أولوية للمؤسس.
- **الاستثناءات:** لا CFO افتراضي، لا مشورة قانونية، لا تمثيل خارجي.
- **السعر:** 7,500–15,000 SAR/شهر — شروط دفع 50/50 للشهر الأول.
- **الترقية:** → Rung 5 — Agency Partner OS أو Custom Enterprise.
- نمط التسليم: **بقيادة المؤسس / شبه-مؤتمت** (يُفصح عنه).

### Rung 5 — Agency Partner OS (مخصص + 15–30% rev-share)

- **العميل المستهدف:** وكالة تسويق/استشارات تريد تقديم Dealix لعملائها.
- **شرط الدخول:** ≥ 3 proof packs مكتملة + اتفاقية شراكة موقعة.
- **المخرجات:** white-label محدود، تدريب الشريك، co-branded proof packs، dashboard شريك، دعم أولوية.
- **الاستثناءات:** لا white-label كامل قبل 3 proof packs، لا مشاركة بيانات عملاء عبر الشركاء.
- **السعر:** مخصص + rev-share 15–30% (راجع [`../AGENCY_PARTNER_PROGRAM.md`](../AGENCY_PARTNER_PROGRAM.md) لتفاصيل الأنواع الثلاثة).
- نمط التسليم: **بقيادة المؤسس / شبه-مؤتمت** (يُفصح عنه).

---

See also: `docs/company/SERVICE_REGISTRY.md`, `docs/company/SERVICE_READINESS_MATRIX.md`,
[`SALES_SYSTEM_COMPLETE.md`](SALES_SYSTEM_COMPLETE.md), [`OBJECTION_HANDLING.md`](OBJECTION_HANDLING.md).
