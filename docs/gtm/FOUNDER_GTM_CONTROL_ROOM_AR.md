# غرفة قيادة المؤسس للسوق — Founder GTM Control Room

غرفة قيادة واحدة تعطي المؤسس قرار اليوم في دقائق: ماذا نرسل؟ ماذا نوقف؟ أي قطاع
وأي عرض اليوم؟ هذه الوثيقة تُعرّف مكوّنات الغرفة ومصادر بياناتها. التنفيذ يكون إمّا
كصفحة تشغيل تحت `/[locale]/ops/gtm-control` أو كتقرير مركزي يُجمَّع يوميًا — كلاهما
يقرأ نفس المخططات والبيانات والتقارير في هذا النظام.

> لا إرسال خارجي من هذه الغرفة بلا موافقة مُسجّلة. الغرفة تعرض وتقترح؛ المؤسس يقرر.

---

## أعلى الشاشة — Today’s GTM Command

| العنصر | المصدر |
|---|---|
| أمر اليوم (Today’s GTM Command) | تجميع آلي من التقارير أدناه |
| أفضل 50 مسودة | [reports/outreach/APPROVAL_QUEUE](../../reports/outreach/APPROVAL_QUEUE.md) |
| دفعة الإرسال المعتمدة | [reports/outreach/SENDING_BATCH_PLAN](../../reports/outreach/SENDING_BATCH_PLAN.md) |
| الردود الإيجابية | [reports/outreach/REPLY_QUEUE](../../reports/outreach/REPLY_QUEUE.md) |
| عناصر عالية الخطورة | بوابة الجودة (`draft_quality_gate`) |
| أفضل قطاع اليوم | [reports/sectors/SECTOR_PRIORITY_REPORT](../../reports/sectors/SECTOR_PRIORITY_REPORT.md) |
| توصية الغد | [reports/gtm/DAILY_GTM_REPORT](../../reports/gtm/DAILY_GTM_REPORT.md) |

---

## التبويبات — Tabs

| التبويب | يعرض | المصدر |
|---|---|---|
| Brand | الهوية والصوت وسياسة الادعاءات | [docs/brand/](../brand/) |
| Products | الكتالوج وحدود التسعير | [PRODUCT_CATALOG_AR](../commercial/PRODUCT_CATALOG_AR.md) |
| Sectors | أولوية القطاعات والمحفّزات | [SECTOR_PRIORITY_REPORT](../../reports/sectors/SECTOR_PRIORITY_REPORT.md) |
| Prospects | الحالات والنقاط | [PROSPECT_RESEARCH_REPORT](../../reports/outreach/PROSPECT_RESEARCH_REPORT.md) |
| Drafts | إنتاج اليوم ومزيجه | [DAILY_DRAFT_PRODUCTION](../../reports/outreach/DAILY_DRAFT_PRODUCTION.md) |
| Approvals | قرارات الاعتماد | [APPROVAL_QUEUE](../../reports/outreach/APPROVAL_QUEUE.md) |
| Sending | الدفعات وصحة الدومين | [SENDING_BATCH_PLAN](../../reports/outreach/SENDING_BATCH_PLAN.md) · [DOMAIN_HEALTH_REVIEW](../../reports/outreach/DOMAIN_HEALTH_REVIEW.md) |
| Replies | تصنيف الردود والإجراءات | [REPLY_QUEUE](../../reports/outreach/REPLY_QUEUE.md) |
| Job Signals | الوظائف كمؤشرات شراء | [JOB_SIGNAL_REPORT](../../reports/signals/JOB_SIGNAL_REPORT.md) |
| Content | تقويم المحتوى | [CONTENT_CALENDAR](../../reports/content/CONTENT_CALENDAR.md) |
| Press | خط الأنابيب الإعلامي | [PRESS_PIPELINE](../../reports/press/PRESS_PIPELINE.md) |
| Partners | خط أنابيب الشركاء | [PARTNER_PIPELINE](../../reports/partnerships/PARTNER_PIPELINE.md) |
| WhatsApp | طابور ما بعد الرد | [WHATSAPP_POST_REPLY_QUEUE](../../reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md) |
| Metrics | المقاييس اليومية والأسبوعية | [GTM_METRICS_AR](GTM_METRICS_AR.md) · [DAILY_GTM_REPORT](../../reports/gtm/DAILY_GTM_REPORT.md) |
| Risks | تحذيرات الكبت/الارتداد/السمعة | [DELIVERABILITY_REVIEW](../../reports/outreach/DELIVERABILITY_REVIEW.md) |

---

## مصدر الحقيقة — Source of Truth

- المخططات: [schemas/](../../schemas/) — تُتحقَّق عبر `scripts/verify_market_production_os.py`.
- البيانات: [data/](../../data/) (prospects · outreach · signals · partners · content · sectors).
- المحرّك المحوكم: [dealix/marketing_factory/market_production_os.py](../../dealix/marketing_factory/market_production_os.py).
- واجهات التشغيل الموجودة: `/[locale]/ops/founder` · `/ops/marketing` (راجع AGENTS.md).
- الفهرس الرئيسي: [MARKET_PRODUCTION_OS_AR](MARKET_PRODUCTION_OS_AR.md).

---

## EN Mirror (condensed)

A single control room that gives the founder the day’s decision in minutes: what to
send, what to pause, which sector and offer to push. It renders the command summary
and 15 tabs from the same schemas, seed data, and reports defined in this OS. It
displays and recommends; it never sends externally without a recorded approval.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
