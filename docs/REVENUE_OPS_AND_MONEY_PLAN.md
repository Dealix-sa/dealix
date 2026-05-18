# Dealix — Revenue Ops & Money Plan — خطة عمليات الإيراد والمال
<!-- PHASE 12 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** المال محكوم. لا شحنة حيّة، خصم، استرداد، أو دفعة بلا موافقة
> بشرية مُسجَّلة. كل ريال يمرّ عبر سجل. ارفع السعر بعد الإثبات لا قبله.

> **تنبيه — لا ضمانات.** كل أرقام MRR والمسارات هنا **أهداف تشغيلية لا ضمانات**.
> أي رقم لم يتحقق = `insufficient_data`. هذا المستند توسعة الجزء D من
> [`MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md`](MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md).
> **مصدر الأسعار الوحيد** هو [`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md) —
> لا يُعاد تسعير شيء هنا، الجداول أدناه روابط لا بدائل.

---

## 1) نموذج الإيراد — السلّم ذو الست درجات · The 6-Rung Revenue Model

السلّم هو محرك الإيراد. لكل درجة دور واضح وهامش تقديري. **الأسعار مصدرها
[`OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md)** — الجدول التالي خريطة
أدوار وهوامش لا قائمة أسعار.

| Rung · الدرجة | الدور · Role | الهامش الإجمالي التقديري | ملاحظة RevOps |
|---------------|--------------|--------------------------|----------------|
| 0 — Free AI Ops Diagnostic | التقاط lead — Lead capture | لا ينطبق (تكلفة API < 2 ريال) | لا إيراد؛ يُقاس بمعدّل التحويل إلى الدرجة 1 |
| 1 — 7-Day Revenue Proof Sprint | الإنزال / بوابة الإثبات — Land / proof gate | ~85% | محرك النقد المبكّر؛ دفعة واحدة مسبقة |
| 2 — Data-to-Revenue Pack | أول upsell — First upsell | ~75% | يرفع متوسط قيمة العميل بعد Sprint |
| 3 — Managed Revenue Ops | متكرّر (MRR) — Recurring | ~70% | أول مصدر MRR؛ محور NRR |
| 4 — Executive Command Center | توسّع — Expansion | ~65% | يرفع MRR لكل عميل؛ يُفتح بعد 3 pilots |
| 5 — Agency Partner OS | مُضاعِف قناة — Channel multiplier | ~55–60% بعد rev-share | يضيف إيراداً غير-مباشر عبر الشركاء |

> The ladder is the revenue engine: rungs 0–1 land and prove, rungs 2–5 expand.
> Margins are estimates, not guarantees. Canonical prices live only in
> OFFER_LADDER_AND_PRICING.md.

---

## 2) استراتيجية التسعير · Pricing Strategy

- **أبقِ السلّم.** لا يُعاد تسعير الدرجات. السلّم المعتمد ذو الست درجات هو الهيكل الوحيد.
- **العروض المصغّرة = نطاقات مصغّرة داخل الدرجة 1.** عروض الاستراتيجية (مثل تدقيق
  10-Lead أو حزمة إثبات مصغّرة) تُعامَل **متغيّرات مُخفَّضة النطاق من الدرجة 1** —
  *تقليل نطاق لا تخفيض سعر*. قرار يبقى للمؤسس؛ لا تُسعَّر تلقائياً.
- **خفّض النطاق لا السعر.** عند الاعتراض السعري: قلّل ما يُسلَّم، لا الرقم. سجّل كل اعتراض.
- **NRR هو الهدف.** الهدف NRR > 100% — يأتي من إيراد التوسّع (الدرجات 3–5)، لا من
  دخول جدد فقط. كل عميل Sprint ناجح هو فرصة upsell موثّقة بإثبات.
- **التسعير المبني على النتيجة** يبقى تجربة لاحقة لما بعد الأفق 3 فقط، بعد أن تثبت
  حزم الإثبات نمطاً متكرّراً — لا قبل ذلك.

---

## 3) الفوترة والتحصيل · Billing & Collections

المسار: **روابط دفع Moyasar → فاتورة إلكترونية متوافقة مع ZATCA** (`integrations/`
محوّلات Moyasar وZATCA، جدول `zatca_invoices`). يدوي الآن؛ مؤتمت في الأفق 4.

```text
عرض موافَق عليه ──▶ رابط دفع Moyasar ──▶ العميل يدفع ──▶ حدث invoice_paid
        │                                                      │
        └──▶ قيد في Proof Ledger          فاتورة ZATCA إلكترونية ─┘──▶ قيد Capital Ledger
```

- **قيد إيراد #1:** تفعيل حساب Moyasar إجراء يدوي للمؤسس. حتى يكتمل لا يُحصَّل 0 ريال.
- **يُتتبَّع:** النقد المُحصَّل · فواتير مُرسَلة/مدفوعة · أيام-حتى-الدفع · فواتير معلّقة.
- **متابعة التحصيل** يدوية الآن (تذكير مهذّب واحد)؛ تُؤتمت في الأفق 4 (dunning).

---

## 4) الضوابط المالية · Financial Controls

- **أفعال حرجة مُبوَّبة بالموافقة.** الخصم، الاسترداد، تغيير التسعير، والدفعة
  (payout) هي `CRITICAL_ACTIONS` تتطلّب موافقة بشرية مُسجَّلة عبر
  `dealix/governance/approvals.py`. لا تنفيذ بلا قيد موافقة.
- **Capital Ledger.** كل أصل قابل لإعادة الاستخدام (قالب، playbook، تقرير) يُسجَّل
  في `capital_os/capital_ledger.py`.
- **Proof Ledger.** كل حدث إيراد يُسجَّل في سجل الإثبات — لا فاتورة بلا أثر مُوثَّق.
- **مبدأ الفصل:** الوكيل يُحضِّر الفاتورة كمسودة؛ المؤسس وحده يُرسلها ويوافق على الشحن.

| الفعل · Action | الوضع · Mode | المسار |
|----------------|--------------|---------|
| تصيير فاتورة كمسودة | آلي (مسموح) | `payment_ops` يُحضّر |
| إرسال فاتورة / رابط دفع | موافقة مطلوبة | المؤسس عبر `ApprovalGate` |
| خصم / استرداد / تغيير سعر / دفعة | حرج — موافقة مُسجَّلة | `approvals.py` `CRITICAL_ACTIONS` |
| شحن حيّ على بطاقة | ممنوع بلا موافقة صريحة | `safe_send_gateway/doctrine.py` |

---

## 5) مسار الـMRR · MRR Trajectory

أهداف من خطة الـ90 يوماً ([`90_DAY_BUSINESS_EXECUTION_PLAN.md`](90_DAY_BUSINESS_EXECUTION_PLAN.md)) —
**أهداف لا ضمانات**.

| المعلَم · Milestone | MRR هدف (ريال) | المصدر التقريبي |
|---------------------|-----------------|------------------|
| اليوم 7 | ≈ 499 | أول Sprint مدفوع |
| اليوم 30 | ≈ 998 | 2 × Sprint |
| اليوم 60 | ≈ 5,998 | 2 × Managed Ops |
| اليوم 90 | ≈ 8,997–14,997 | 3 retainers + توسّع |

> Any MRR figure not yet collected is reported as `insufficient_data`, never as
> a forecast presented as fact.

---

## 6) اقتصاديات الوحدة لكل Sprint · Unit Economics to Track

تُسجَّل لكل Sprint مدفوع — لاتخاذ قرار رفع السعر بناءً على بيانات لا إحساس.

| المقياس · Metric | كيف يُقاس |
|------------------|------------|
| الإيراد · Revenue | السعر المُحصَّل فعلاً |
| ساعات التسليم · Delivery hours | ساعات المؤسس الفعلية على الـSprint |
| التكلفة الساعية · Hourly cost | قيمة وقت المؤسس المُسنَدة |
| الهامش الإجمالي · Gross margin | الإيراد − (ساعات × تكلفة ساعية + تكلفة LLM) |
| زمن-الوصول-للإثبات · Time-to-proof | من البدء إلى Proof Pack v1 (هدف <48 ساعة) |
| احتمال Sprint→retainer | معدّل تحويل Sprint إلى Managed Ops |

**قاعدة رفع السعر:** ارفع سعر الدرجة 1 فقط بعد 3–5 Sprints مدفوعة + إثبات +
زمن تسليم < ~5 ساعات لكل Sprint. قبل ذلك السعر ثابت.

---

## 7) وضعية التمويل · Funding Posture

- **التمهيد الذاتي أولاً (Bootstrap-first).** المنصة مبنيّة؛ القيد هو البيع لا رأس المال.
- **لا تستخدم عرض المستثمر خارجياً** حتى يُصلِح توحيد السرد (الأفق 0) مبالغاته.
  العرض القديم يخالف `dealix/registers/no_overclaim.yaml`.
- محادثات المستثمرين خيار **لما بعد الأفق 3**، مدعومة بحزم إثبات حقيقية وMRR
  مُحصَّل — لا توقّعات. لا عرض مستثمر قبل إصلاح السرد.

---

## فهرس مراجع الريبو — Repo Cross-reference Index

| الموضوع | الملف المعتمد |
|---------|----------------|
| الخطة الأم (الجزء D الأصلي) | [MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md](MASTER_LAUNCH_AND_COMMERCIALIZATION_PLAN.md) |
| سلم العروض والتسعير (مصدر الأسعار) | [OFFER_LADDER_AND_PRICING.md](OFFER_LADDER_AND_PRICING.md) |
| خطة 90 يوم (مصدر أهداف MRR) | [90_DAY_BUSINESS_EXECUTION_PLAN.md](90_DAY_BUSINESS_EXECUTION_PLAN.md) |
| لوحة التوزيع اليومية | [ops/DISTRIBUTION_DASHBOARD.md](ops/DISTRIBUTION_DASHBOARD.md) |
| محفّزات البناء المشروط | [sales-kit/CONDITIONAL_BUILD_TRIGGERS.md](sales-kit/CONDITIONAL_BUILD_TRIGGERS.md) |
| التجميد التجاري | [ops/COMMERCIAL_FREEZE.md](ops/COMMERCIAL_FREEZE.md) |
| بوابة الموافقات (كود) | `dealix/governance/approvals.py` |
| سجل رأس المال (كود) | `capital_os/capital_ledger.py` |
| فرض الـdoctrine (كود) | `auto_client_acquisition/safe_send_gateway/doctrine.py` |

---

*Version 1.0 | Expands Part D of the Master Launch Plan | Goals not guarantees |
Missing data = insufficient_data | Pricing is canonical only in
OFFER_LADDER_AND_PRICING.md — not re-priced here.*
