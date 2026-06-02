# خط أنابيب الإعلام — Press Pipeline

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**النوع:** قالب تشغيلي — صفوف نموذجية (placeholder) تُستبدل بجهات حقيقية.
**المالك:** المؤسس (سامي)
**يقرأ القواعد من:** docs/press/PRESS_OUTREACH_OS_AR.md · docs/press/MEDIA_TARGETS_AR.md · docs/BRAND_PRESS_KIT.md
**آخر تحديث:** 2026-06-02

---

## كيف يُستخدم

- صفّ واحد لكل جهة إعلام **مُتواصَل معها**.
- **3 جهات كحدّ أقصى لكل محفّز.** لا إرسال للعشرة دفعة واحدة.
- لا يُفتح صفّ قبل تحقّق محفّز في docs/press/PROOF_MILESTONES_AR.md.
- المراحل: مُختارة → طرح أُرسِل → انتظار → رد → مقابلة/تجهيز → نُشِر → مغلق بلا رد.

## جدول الـ Pipeline (صفوف نموذجية)

| الجهة | الزاوية | المحفّز | تاريخ الطرح | الحالة | الخطوة التالية |
|-------|---------|---------|-------------|--------|-----------------|
| [الجهة 1] | [أفضل زاوية للجهة] | [المحفّز المُحقَّق] | [YYYY-MM-DD] | مُختارة | إرسال طرح مخصّص لصحفي مُسمّى |
| [الجهة 2] | [أفضل زاوية للجهة] | [المحفّز المُحقَّق] | [YYYY-MM-DD] | طرح أُرسِل | انتظار 7 أيام قبل المتابعة |
| [الجهة 3] | [أفضل زاوية للجهة] | [المحفّز المُحقَّق] | [YYYY-MM-DD] | انتظار | متابعة واحدة عند انتهاء النافذة |

> هذه صفوف توضيحية فقط. استبدلها بجهات حقيقية بعد تحقّق المحفّز.

## ملاحظات التسجيل

- التغطية المنشورة تُسجَّل أيضاً في docs/wave6/live/press_log.jsonl.
- لا أسماء عملاء في أي صفّ بدون `signed_publish_permission`.
- الجهة بحالة «مغلق بلا رد» تعود لقائمة docs/press/MEDIA_TARGETS_AR.md لمحفّز لاحق.

## الخطوة التالية

عند تحقّق المحفّز القادم: افتح حتى 3 صفوف، املأ الزاوية وتاريخ الطرح، وحدّث الحالة أسبوعياً.

## English summary

A template tracker for press outreach. One row per outlet contacted, maximum 3 outlets per trigger, never all 10 at once. Columns: outlet, angle, trigger, pitch date, status, next step. Rows are illustrative placeholders to be replaced by real outlets only after a milestone in docs/press/PROOF_MILESTONES_AR.md verifies. Stages run Selected → Pitched → Waiting → Replied → Briefing → Published → Closed-No-Reply. Published coverage is also logged in docs/wave6/live/press_log.jsonl. No customer names appear in any row without signed publish permission. Outlets that go Closed-No-Reply return to docs/press/MEDIA_TARGETS_AR.md for a later trigger.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
