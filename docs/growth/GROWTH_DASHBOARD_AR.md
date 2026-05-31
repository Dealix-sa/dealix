# Growth Dashboard — لوحة النمو الواحدة

> Section 42. كل المؤشّرات في شاشة واحدة، مع 7 أنماط إنذار وكتاب ردّ لكل نمط.
> Module path: `dealix/growth_os/dashboard/`

---

## مبدأ التصميم — Design Principle

شاشة واحدة. تُقرأ في 90 ثانية. تُجيب على سؤال: "هل النمو سليم اليوم؟" إن احتاجت شرحاً، فهي مكسورة.

One screen. Read in 90 seconds. Answers one question: "Is growth healthy today?"

---

## بنية الشاشة — Dashboard Layout

### Row 1 — Revenue Pulse

| المؤشّر | الوصف | Target |
|---|---|---|
| `revenue_this_month_sar` | الإيراد المُحقَّق هذا الشهر | `<TBD: founder fill>` |
| `signed_pipeline_sar` | proposals موقَّعة لم تُسلَّم بعد | track |
| `weighted_pipeline_sar` | pipeline × probability | track |
| `revenue_quality_score_avg` | متوسط RQS لصفقات الشهر | ≥ 70 |

### Row 2 — Conversion Funnel

| المؤشّر | الوصف |
|---|---|
| `meetings_booked` | اجتماعات هذا الشهر |
| `meeting_to_proposal_rate` | % اجتماع → مقترح |
| `proposal_to_signature_rate` | % مقترح → توقيع |
| `median_cycle_days` | متوسط الأيام من أوّل اتّصال إلى توقيع |

### Row 3 — Channel Health

| المؤشّر | الوصف |
|---|---|
| `geo_attributed_revenue_sar` | إيراد منسوب لـ GEO |
| `abm_attributed_revenue_sar` | إيراد منسوب لـ ABM |
| `partner_attributed_revenue_sar` | إيراد منسوب للشركاء |
| `paid_attributed_revenue_sar` | إيراد منسوب للحملات المدفوعة |
| `channel_concentration_index` | تنوّع القنوات (0=مركَّز، 1=موزّع) |

### Row 4 — Retention & Expansion

| المؤشّر | الوصف |
|---|---|
| `nrr` | Net Revenue Retention |
| `grr` | Gross Revenue Retention |
| `logo_churn_count` | عدد عملاء فُقدوا |
| `expansion_revenue_sar` | إيراد من upsell/cross-sell |

### Row 5 — Governance & Refusals

| المؤشّر | الوصف |
|---|---|
| `assurance_pass_rate` | % صفقات اجتازت كل بوّابات Assurance |
| `refused_deals_count` | عدد صفقات مرفوضة هذا الشهر |
| `claim_safety_incidents` | حوادث ادعاء غير مُسنَد |
| `pdpl_flags` | تنبيهات PDPL |

---

## الإنذارات السبع — 7 Red-Flag Patterns

كل نمط له: detection rule، severity، playbook ردّ.

### 1) Pipeline Famine — جوع الـ Pipeline

- **Detect.** `meetings_booked` < 50% من المستهدف لأسبوعين متتاليين.
- **Severity.** High.
- **Playbook.**
  1. تشغيل SignalRadar manual sweep.
  2. مراجعة آخر 10 رسائل ABM — هل الزاوية ضعفت؟
  3. تشغيل تجربة message angle خلال 14 يوم.
  4. تقليل عدد الـ ICPs المُستهدَفة مؤقّتاً للتركيز.

### 2) Conversion Bleed — نزيف التحويل

- **Detect.** `meeting_to_proposal_rate` يهبط ≥ 15 نقطة عن baseline 30 يوم.
- **Severity.** High.
- **Playbook.**
  1. مراجعة أوّل 10 دقائق من آخر 5 اجتماعات.
  2. تدقيق ICP fit للاجتماعات الأخيرة.
  3. تحديث ICPProfile.disqualifiers.

### 3) Channel Concentration — تركّز القناة

- **Detect.** قناة واحدة > 70% من الإيراد لشهرين.
- **Severity.** Medium-High.
- **Playbook.**
  1. تخصيص ميزانية لقناة ثانية.
  2. تشغيل partner motion إن لم يكن نشطاً.
  3. تجربة GEO إن كانت ABM طاغية.

### 4) Quality Erosion — تآكل الجودة

- **Detect.** `revenue_quality_score_avg` يهبط تحت 60 لشهرين.
- **Severity.** High.
- **Playbook.**
  1. مراجعة الـ offers الأكثر بيعاً — هل margin انخفض؟
  2. تشديد قواعد G1 (Offer Match) في Assurance.
  3. توقّف عن قبول one-off فقط؛ اشترط مسار retainer.

### 5) Retention Crack — تشقّق الإبقاء

- **Detect.** `nrr` < 100% أو `logo_churn_count` ≥ 2 في الشهر.
- **Severity.** High.
- **Playbook.**
  1. مكالمة 1-on-1 مع كل عميل فقدناه — سبب موثَّق.
  2. مراجعة ClientHealthScore لكل العملاء الحاليّين.
  3. تفعيل Expansion Offer Map.

### 6) Assurance Failures — إخفاقات الحوكمة

- **Detect.** `assurance_pass_rate` < 90% أو `claim_safety_incidents` ≥ 1.
- **Severity.** Critical.
- **Playbook.**
  1. إيقاف الإرسال لكل المقترحات حتى مراجعة.
  2. إعادة تدريب على claim-safety.
  3. تحديث policy registry.

### 7) Refusal Spike — قفزة الرفض

- **Detect.** `refused_deals_count` ≥ 3 في الشهر.
- **Severity.** Medium (قد يكون صحّياً، يحتاج تحليل).
- **Playbook.**
  1. تصنيف الأسباب: ICP خطأ / scope خاطئ / governance fail / capacity.
  2. إن السبب ICP → تحديث Top-of-Funnel.
  3. إن السبب capacity → إيقاف paid قنوات الجلب.

---

## إيقاع المراجعة — Review Cadence

- **يومياً.** Founder ينظر 60 ثانية → meetings + pipeline + red flags.
- **أسبوعياً.** Growth review 45 دقيقة → كل الـ rows.
- **شهريّاً.** Quarterly playbook update + experiments shipped.

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
