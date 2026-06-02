# Proposal Factory — مصنع العروض (Distribution OS v1)

**الغرض:** توليد **هيكل عرض محكوم** (proposal skeleton) بحدود حوكمة مدمجة، يملؤه المؤسس بعد جلسة الاكتشاف. العرض يخرج مسودةً بالحالة `pending_approval` ولا يُرسَل إلا يدوياً بعد موافقة. **لا ضمان نتائج، لا نطاق مفتوح، لا التزام قانوني بلا مراجعة.**

**المنفّذ:** [`scripts/generate_proposal_draft.py`](../../scripts/generate_proposal_draft.py) — يعيد استخدام [`auto_client_acquisition.sales_os.build_proposal_skeleton`](../../auto_client_acquisition/sales_os/proposal_generator.py).

**التشغيل:** `make proposal-drafts`.

**مراجع:** سياسة الجودة: [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) · حزمة الإثبات: [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md) · الحزم والأسعار: [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · محرك الإغلاق: [FULL_OPS_CLOSE_ENGINE_AR.md](../commercial/FULL_OPS_CLOSE_ENGINE_AR.md).

---

## 1) مكوّنات العرض (13 قسماً)

هذه هي مفاتيح الأقسام الثابتة (`PROPOSAL_SECTION_KEYS`) — لا يُحذف منها قسم:

| # | القسم | ماذا يحتوي |
|---|-------|------------|
| 1 | `problem` (المشكلة) | الألم المحدّد من الاكتشاف — «ما بعد الـ lead» لا وصف المنتج |
| 2 | `current_maturity` (النضج الحالي) | أين العميل اليوم في المتابعة/الحوكمة |
| 3 | `recommended_sprint` (الـ Sprint المقترح) | Diagnostic أو Lead Intelligence Sprint إلخ |
| 4 | `scope` (النطاق) | ما يُنفَّذ ضمن السعر — **محدود ومكتوب** |
| 5 | `inputs_needed` (المدخلات المطلوبة) | صادرات CSV، نقطة اتصال، وصول قراءة، SLA رد |
| 6 | `deliverables` (المخرجات) | تقرير، قائمة مراحل، مسودات، حزمة إثبات |
| 7 | `governance_boundaries` (حدود الحوكمة) | لا كشط، لا واتساب بارد آلي، لا أتمتة لينكدإن، لا ضمان، إجراءات خارجية بموافقة أولاً |
| 8 | `proof_metrics` (مقاييس الإثبات) | طريقة القياس المتوقعة (before/after) — لا أرقام مخترعة |
| 9 | `timeline` (الجدول الزمني) | أيام عمل، جلسات kickoff/review، تاريخ التسليم |
| 10 | `price` (السعر / نطاق سعري) | من جدول الحزم — رقم أو مدى، لا «حسب النتيجة» |
| 11 | `retainer_path` (مسار الريتينر) | التوسعة **بعد** Proof فقط، لا قبله |
| 12 | `exclusions` (الاستثناءات) | تكاملات ثقيلة، إرسال جماعي، أي ضمان إيراد رقمي |
| 13 | `no_sales_guarantee_statement` (بيان عدم ضمان المبيعات) | إلزامي — انظر §3 |

القسمان 7 و13 يأتيان **مملوءين مسبقاً** من `build_proposal_skeleton`؛ البقية يملؤها المؤسس بعد الاكتشاف.

---

## 2) القواعد (غير قابلة للتفاوض)

| القاعدة | لماذا |
|---------|-------|
| **لا ضمان ROI** | لا نَعِد بنتيجة مالية؛ نَعِد بقدرة محكومة وأدلة جاهزية |
| **لا نطاق مفتوح** | النطاق مكتوب ومحدود — يلغي توقع «السحر» |
| **لا التزام قانوني بلا مراجعة** | أي بند تعاقدي/قانوني يمرّ بمراجعة قبل الإرسال |
| **كل عرض يحتاج موافقة** | يخرج `pending_approval`؛ يُرسَل يدوياً بعد قرار المؤسس |

---

## 3) بيان عدم ضمان المبيعات (مملوء مسبقاً)

النص الافتراضي من `build_proposal_skeleton` (EN، يُترجَم/يُكيَّف عند الحاجة):

> "This sprint does not promise sales outcomes. It builds a governed revenue capability and produces proof of readiness, prioritization, and next actions."

والمقابل العربي المعتمد:

> «هذا الـ Sprint لا يَعِد بنتائج مبيعات. يبني **قدرة إيراد محكومة** ويُخرِج دليلاً على الجاهزية، والأولويات، والخطوات التالية.»

وحدود الحوكمة المملوءة مسبقاً (`governance_boundaries`):

> "No scraping. No cold WhatsApp automation. No LinkedIn automation. No guaranteed sales claims. External actions are draft/approval-first."

---

## 4) من الاكتشاف إلى العرض

```text
discovery (اكتشاف) → build_proposal_skeleton → ملء المؤسس للأقسام 1–6, 8–12
→ بوابة الجودة (DRAFT_QUALITY_POLICY) → pending_approval → موافقة → إرسال يدوي
```

العرض يخضع لنفس بوابة الجودة كأي مسودة: يُحجَب أي ضمان أو لغة قناة ممنوعة قبل أن يصل المؤسس ([DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md)).

---

## 5) السعر والحزم

استخدم الأسعار/النطاقات من [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md). لا تخترع أرقاماً، ولا تربط السعر بنتيجة («ندفع لو ما نجح» = ممنوع). الريتينر يأتي **بعد** حزمة إثبات مُسلَّمة، لا قبلها.

---

## 6) حدود صريحة

- لا إرسال آلي للعرض — نسخ ومراجعة وإرسال يدوي بعد موافقة.
- لا ضمان إيراد رقمي في النطاق.
- لا توسعة (retainer/upsell) قبل Proof Pack بمستوى L3 على الأقل (دليل مبيعات خاص بالعميل).

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*يُبنى في هذا الـ PR. آخر تحديث: 2026-06-02.*
