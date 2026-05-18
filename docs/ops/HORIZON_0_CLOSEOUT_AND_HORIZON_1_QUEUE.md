# Dealix — Horizon 0 Closeout & Horizon 1 Action Queue — إغلاق Horizon 0 وقائمة Horizon 1
<!-- PHASE 12 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** Horizon 0 يُغلق عند اكتمال ثلاثة شروط: توحيد الرواية ✅،
> بوابة الجاهزية خضراء ✅، وتفعيل Moyasar ⛔. الشرطان الأولان مكتملان؛ البيع
> الفعلي في Horizon 1 لا يبدأ بجمع الدفع حتى يُفعّل المؤسس حساب Moyasar.

المرجع: [`MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md`](../MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md)

---

## 1) حالة Horizon 0 — Closeout

| البند | الحالة | الدليل |
|-------|--------|--------|
| بوابة الجاهزية | ✅ PASS (39/0/0) | `scripts/business_readiness_verify.sh` — `SELLABLE_NOW=YES` |
| تسليم الدرجة 0 (Free Diagnostic) | ✅ GREEN | `docs/03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md` |
| تسليم الدرجة 1 (499 Sprint) | ✅ GREEN | `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md` |
| توحيد الرواية | ✅ COMPLETE | 74 ملفاً، 3 commits (`d43b5fe`, `6bea317`, `88df8d2`) |
| 4 وثائق التدشين الأم | ✅ DONE | MASTER_LAUNCH · REVENUE_OPS_AND_MONEY · AFFILIATE_GOVERNANCE · DISTRIBUTION_DASHBOARD |
| تفعيل Moyasar | ⛔ BLOCKED | فعل يدوي على المؤسس — لا يقدر عليه كود أو وكيل |

**بوابة الخروج H0→H1:** الرواية ✅ + الجاهزية ✅ + Moyasar ⛔ →
البيع التحضيري يبدأ الآن؛ **جمع أول دفعة** ينتظر Moyasar فقط.

---

## 2) قائمة Horizon 1 — Action Queue (الأيام 4–30)

### أ. أفعال المؤسس — المسار الحرج (لا يقدر عليها وكيل)

1. **تفعيل Moyasar** — KYC وربط الحساب البنكي. المُعطِّل #1 للإيراد.
2. اعتماد وإرسال رسائل التواصل الدافئة لقائمة الـ20–50 المؤهلة.
3. إجراء الـDiagnostics، وإغلاق أول 499 Sprint.

### ب. عمل مدعوم بالوكلاء — آمن مع التجميد (مسودات بانتظار موافقتك)

| الوكيل | المهمة |
|--------|--------|
| dealix-sales | تأهيل القائمة الدافئة، رندرة عروض Sprint، صياغة مسودات تواصل في طابور الموافقة |
| dealix-delivery | تشغيل Sprint الـ7 أيام عند إغلاق أول عميل؛ تجميع Proof Pack؛ تسجيل أصل Capital Ledger |
| dealix-content | إنشاء قالب Sprint Completion Certificate؛ أول محتوى case مجهول؛ بدء إيقاع LinkedIn |

### ج. Backlog — قرارات للمؤسس

- **إعادة بناء أصلين** وُسما بتعارض بنيوي عميق (لا مجرد تأطير):
  `docs/sales-kit/dealix_self_dogfooding.md` و `docs/sales-kit/dealix_roi_calculator.html`
  — منطقهما مبني على عقيدة الأتمتة الكاملة؛ يُعاد بناؤهما تحت عقيدة الرادار المحكوم.
- **مراجعة كاملة لـ pitch deck و pilot agreement** — وُحّدت ادعاءاتهما الظاهرة،
  لكن العمود الإجمالي (deck) ونموذج التسعير القديم يحتاجان إعادة بناء قبل أي
  استخدام استثماري — راجع `REVENUE_OPS_AND_MONEY_PLAN.md` (وضعية التمويل).
- **توحيد هندسي** (محرّكا diagnostic، ومسارا proof-pack) — عمل كود = Horizon 4،
  مبوّب خلف رفع التجميد. لا يُنفّذ الآن.

---

## 3) ما لا يُنفّذ الآن — حدود التجميد

البناء البرمجي للأتمتة الكاملة (Full Ops / autopilot) هو **Horizon 4**،
مبوّب خلف بوابة: تكرار workflow 3+ مرات بإثبات + رفع تجميد صريح. الإرسال
الخارجي التلقائي بلا موافقة **ممنوع بنيوياً دائماً** بالـ11 غير-قابلة-للتفاوض —
ليس قيد تجميد، بل تصميم. انظر `MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md`
قسم Horizon 4.

---

## فهرس مرجعي

| الموضوع | الملف |
|---------|--------|
| الخطة الأم | [MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md](../MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md) |
| خطة المال | [REVENUE_OPS_AND_MONEY_PLAN.md](../REVENUE_OPS_AND_MONEY_PLAN.md) |
| لوحة التوزيع اليومية | [DISTRIBUTION_DASHBOARD.md](DISTRIBUTION_DASHBOARD.md) |
| خطة 90 يوم | [../90_DAY_BUSINESS_EXECUTION_PLAN.md](../90_DAY_BUSINESS_EXECUTION_PLAN.md) |
| SOP تسليم Sprint | [../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) |

---

*Version 1.0 | Horizon 0 closeout | Goals not guarantees | Missing data = insufficient_data*
