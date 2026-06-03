# صف الموافقة — Approval Queue

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المصدر:** docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md
**يُولَّد بواسطة:** scripts/verify_market_production_os.py
**التاريخ:** {{ date }}

> قالب — الصفوف عناصر نائبة. لا إرسال بدون موافقة المؤسس. عند الشك، لا ترسل.

## أفضل 50 مسودة اليوم

| # | الشركة | القطاع | الدور | النوع | العرض | درجة العميل | تخصيص | المخاطر |
|---|--------|--------|-------|-------|-------|-------------|--------|---------|
| 1 | {{ d1_company }} | {{ d1_sector }} | {{ d1_role }} | {{ d1_step }} | {{ d1_offer }} | {{ d1_score }} | {{ d1_ptier }} | {{ d1_risk }} |
| 2 | {{ d2_company }} | {{ d2_sector }} | {{ d2_role }} | {{ d2_step }} | {{ d2_offer }} | {{ d2_score }} | {{ d2_ptier }} | {{ d2_risk }} |
| … | … | … | … | … | … | … | … | … |

(يُملأ حتى 50 صفاً)

## مسودات عالية المخاطر (مراجعة/رفض)

| # | الشركة | السبب | compliance_status |
|---|--------|-------|-------------------|
| 1 | {{ hr1_company }} | {{ hr1_reason }} | {{ hr1_compliance }} |

## أفضل القطاعات اليوم

| القطاع | مسودات معتمدة | تجاوب متوقع |
|--------|----------------|--------------|
| {{ sec1 }} | {{ sec1_approved }} | {{ sec1_signal }} |

## دفعة الإرسال المقترحة

| الحقل | القيمة |
|-------|--------|
| الحجم المقترح | {{ suggested_batch_size }} |
| سقف اليوم (خطة التدرّج) | {{ daily_cap }} |
| الحسابات/النطاقات | {{ accounts }} |
| نافذة الإرسال | {{ send_window }} |

> الحجم المقترح لا يتجاوز سقف اليوم في docs/outreach/SENDING_RAMP_PLAN_AR.md.

## تحذيرات الانسحاب/الارتداد

| المؤشر | القيمة | الحالة |
|--------|--------|--------|
| معدل الانسحاب (opt-out) | {{ optout_rate }} | {{ optout_status }} |
| معدل الارتداد (bounce) | {{ bounce_rate }} | {{ bounce_status }} |
| الشكاوى (complaints) | {{ complaint_rate }} | {{ complaint_status }} |

> أي قفزة توقف توسّع الإرسال (docs/outreach/SENDING_RAMP_OS_AR.md).

## الخطوة التالية

- اعتماد/رفض/إعادة صياغة لكل مسودة وفق docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md.
- تمرير المعتمَد إلى reports/outreach/SENDING_BATCH_PLAN.md.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
