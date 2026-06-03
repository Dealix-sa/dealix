# خطة دفعة الإرسال — Sending Batch Plan

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المصدر:** docs/outreach/SENDING_RAMP_OS_AR.md
**سياسة التسليم (مرجع):** docs/outreach/SENDING_RAMP_PLAN_AR.md
**يُولَّد بواسطة:** scripts/verify_market_production_os.py
**التاريخ:** {{ date }}

> قالب — الصفوف عناصر نائبة. 250 مسودة/يوم لا تعني 250 إرسالة/يوم. الإرسال يتدرّج ببطء.

## ملخّص اليوم

| الحقل | القيمة |
|-------|--------|
| سقف اليوم (خطة التدرّج) | {{ daily_cap }} |
| إجمالي المجدوَل | {{ total_scheduled }} |
| الحسابات النشطة | {{ active_accounts }} |
| النطاقات الصحية | {{ healthy_domains }} |

## الدفعات

| batch_id | الحجم | الحساب | النطاق | القطاع | خطوة التسلسل | المخاطر | approved_at | نافذة الإرسال |
|----------|------|--------|--------|--------|---------------|---------|-------------|----------------|
| {{ b1_id }} | {{ b1_size }} | {{ b1_account }} | {{ b1_domain }} | {{ b1_sector }} | {{ b1_step }} | {{ b1_risk }} | {{ b1_approved_at }} | {{ b1_window }} |
| {{ b2_id }} | {{ b2_size }} | {{ b2_account }} | {{ b2_domain }} | {{ b2_sector }} | {{ b2_step }} | {{ b2_risk }} | {{ b2_approved_at }} | {{ b2_window }} |
| … | … | … | … | … | … | … | … | … |

## فحص Pre-flight (لكل دفعة)

| الفحص | الحالة |
|-------|--------|
| انسحاب مضمَّن في كل رسالة | {{ check_unsubscribe }} |
| موافقة المؤسس (approved_at) | {{ check_approval }} |
| تخصيص ≥ P1 | {{ check_personalization }} |
| لا مستلم مكبوح | {{ check_suppression }} |
| النطاق صحي | {{ check_domain_health }} |
| لا قفزة ارتداد/شكوى | {{ check_bounce_spike }} |

> أي فحص يفشل يوقف الدفعة بالكامل.

## المراقبة اللحظية

| المؤشر | القيمة | عتبة الإيقاف |
|--------|--------|---------------|
| الارتداد (bounce) | {{ bounce_now }} | {{ bounce_threshold }} |
| الشكاوى (complaints) | {{ complaint_now }} | {{ complaint_threshold }} |
| الانسحاب (opt-out) | {{ optout_now }} | {{ optout_threshold }} |

## الخطوة التالية

- تنفيذ الدفعات ضمن نوافذها ومراقبة المؤشرات.
- الردود تُوجَّه إلى reports/outreach/REPLY_QUEUE.md.
- أي تجاوز عتبة → إيقاف فوري + إبلاغ المؤسس + مراجعة docs/outreach/SENDING_RAMP_PLAN_AR.md.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
