# Dealix Command Sprint — Customer Delivery Template
# قالب تسليم عميل Dealix Command Sprint

> **هذا المجلد قالب.** يُنسخ كاملاً إلى `customers/<اسم-العميل>/` لكل عميل مدفوع.
> This folder is a template. It is copied in full to `customers/<customer-name>/` for every paid customer.
> لا تُعدِّل هذا القالب ببيانات عميل حقيقي. الحقول `[fill]` تُملأ في النسخة فقط.
> Do not place real customer data in this template. `[fill]` fields are filled only in the copy.

المرجع الأساسي: [`../../docs/00_platform_truth/PLATFORM_TRUTH.md`](../../docs/00_platform_truth/PLATFORM_TRUTH.md)

---

## ما هو Command Sprint — What the Command Sprint is

ارتباط ثابت، مدّته **7 أيام**، نطاق محدّد. المخرجات:
Fixed-scope, **7-day** engagement. Outputs:

Revenue Map · Proof Register · Approval Register · Next Action Board · Executive Command Brief → assembled as a **Proof Pack**.

**الوعد:** وضوح وصورة تشغيلية جاهزة للمراجعة البشرية — **وليس** ضمان إيرادات.
**The promise:** clarity and a human-review-ready operating picture — **not** a revenue guarantee.

---

## خريطة التسليم — 7-Day Delivery SLA Map

| اليوم Day | الناتج Deliverable | الملف File |
|---|---|---|
| **Day 1** | Intake + Company Intelligence | `00_intake.md`, `01_company_intelligence.md` |
| **Day 2** | Diagnostic Summary | `02_diagnostic_summary.md` |
| **Day 3** | Revenue Map | `04_revenue_map.md` |
| **Day 4** | Proof Register | `05_proof_register.md` |
| **Day 5** | Approval Register + Next Action Board | `06_approval_register.md`, `07_next_action_board.md` |
| **Day 6** | Executive Command Brief | `08_executive_command_brief.md` |
| **Day 7** | Proof Pack + Upsell Recommendation | `10_proof_pack.md`, `11_upsell_recommendation.md` |

> `03_command_sprint_scope.md` يُتَّفق عليه عند الـ kickoff (Day 1). `09_delivery_log.md` يُحدَّث يومياً.
> Scope is agreed at kickoff (Day 1). The delivery log is updated daily.

---

## القواعد الصارمة — Hard rules (apply to every file)

- ❌ لا ضمان إيرادات/نتائج/ROI — No guaranteed revenue, results, or ROI. لا «نضمن» ولا «مضمون».
- ❌ لا إرسال خارجي تلقائي (auto-send) — No automatic external sending.
- ❌ لا واتساب بارد ولا scraping ولا blast — No cold WhatsApp, scraping, or list blasting.
- ❌ لا proof مزيّف — No fake proof, testimonials, or fabricated metrics.
- ✅ **موافقة بشرية مطلوبة قبل أي إجراء خارجي** — Human approval required before every external action. سُجِّل كل موافقة في `06_approval_register.md`.
- ✅ كل رقم: مصدر أو `is_estimate=true`. أي بيان ناقص يُسمّى صراحة «مفقود / missing».

> «القيمة التقديرية ليست قيمة مُتحقَّقة» — *Estimated value is not Verified value.*

---

## الحقول التسعة المشتركة — The nine shared fields

كل ملف في هذا القالب يحتوي على هذه الحقول التسعة كي يتتبّع الفريق المصدر والأدلة والموافقة.
Every file in this template carries these nine fields so the team tracks source, evidence, and approval.

`source` · `evidence` · `assumption` · `confidence` · `recommendation` · `approval_required` · `next_action` · `owner` · `due_date`
