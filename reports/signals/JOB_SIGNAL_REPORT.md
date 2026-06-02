# Job Signal Report — تقرير إشارات التوظيف (قالب)

> جزء من: Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
>
> **النوع:** قالب تقرير — الصفوف أدناه نماذج placeholder تُستبدل بإشارات حقيقية.
> **المصدر:** إعلانات وظائف منشورة علناً، مُراجَعة يدوياً، بموافقة المؤسس لكل تواصل. لا كشط، لا أتمتة.
> **المنهجية الكاملة:** [docs/signals/JOB_SIGNAL_PLAYBOOK_AR.md](../../docs/signals/JOB_SIGNAL_PLAYBOOK_AR.md) · المخطط: [schemas/job_signal.schema.json](../../schemas/job_signal.schema.json)

---

## ملخص الفترة — Period summary

- **الفترة / Period:** [YYYY-MM-DD] → [YYYY-MM-DD]
- **إشارات مرصودة / Signals observed:** [N]
- **بانتظار موافقة / Awaiting approval:** [N]
- **مُعتمَدة للتواصل / Approved to send:** [N]
- **مرفوضة / Declined:** [N]
- **تحوّلت إلى تشخيص / Converted to diagnostic:** [N]

الأرقام أعلاه وصفية للنشاط، لا للإيراد. القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## جدول الإشارات المرصودة — Detected job signals

| الشركة (مُجهَّلة) / Company (anonymized) | الوظيفة / Role | الألم المُرجَّح / Likely pain | العرض المُطابَق / Matched offer | الحالة / Status | قرار المؤسس / Founder decision |
|---|---|---|---|---|---|
| [Company A — services] | Sales Operations | بيانات مبعثرة، لا أولوية | Revenue OS Starter | observed | pending |
| [Company B — SaaS] | CRM Manager | تكرارات، قُمع غير نظيف | CRM / Funnel Cleanup | observed | approved |
| [Company C — retail] | Marketing Coordinator | حملات بلا متابعة | Campaign Follow-up Workflow | reviewed | declined |
| [Company D — logistics] | Customer Support | ردود متأخرة، نبرة غير متسقة | Support Draft OS | reviewed | pending |
| [Company E — fintech] | Growth Manager | تجارب بلا معيار خروج | Growth Experiment OS | contacted | approved |

**قاموس الحالة / Status values:** `observed` · `reviewed` · `approved` · `contacted` · `declined` · `converted`.
**قاموس القرار / Decision values:** `pending` · `approved` · `edit_requested` · `declined`.

كل صف هنا نموذج. تُملأ الصفوف الحقيقية بعد مراجعة يدوية لإعلان منشور علناً، وتُجهَّل هوية الشركة في النشر، ولا تُذكر أي بيانات شخصية.

Every row here is a placeholder. Real rows are filled after manual review of a publicly posted ad, the company is anonymized for any publication, and no personal data is recorded.

---

## مسار الموافقة — Approval trail (template)

| المعرّف / ID | الإشارة / Signal | مسودة الرسالة جاهزة / Draft ready | اعتماد المؤسس / Founder sign-off | الوقت / Timestamp |
|---|---|---|---|---|
| SIG-0001 | [Company A — Sales Ops] | yes | pending | [—] |
| SIG-0002 | [Company B — CRM] | yes | approved | [YYYY-MM-DD HH:MM] |
| SIG-0003 | [Company C — Marketing] | yes | declined | [YYYY-MM-DD HH:MM] |

لا صف ينتقل من `approved` في عمود الحالة دون قيد مقابل في هذا المسار. لا تواصل بلا اعتماد مُسجَّل بالوقت.

No row advances to `approved` status without a matching entry here. No outreach without a timestamped sign-off.

---

## ملاحظات الفترة — Period notes

- **أنماط متكرّرة / Recurring patterns:** [مثال: تكرار وظائف CRM في قطاع SaaS هذا الأسبوع → موضوع محتوى مقترح.]
- **محتوى مشتق / Content spun off:** يُحوَّل النمط لا الشركة إلى منشور عبر [docs/content/CONTENT_ENGINE_AR.md](../../docs/content/CONTENT_ENGINE_AR.md).
- **مرفوضات وأسبابها / Declines and why:** [مثال: الإعلان قديم؛ أو القطاع خارج النطاق؛ أو لا ملاءمة.]

الخطوة التالية الافتراضية لأي إشارة مُعتمَدة: عرض تشخيص مجاني خلال 24 ساعة، صفحتان، باعتماد المؤسس، ولا التزام بعده.

The default next step for any approved signal: offer a Free Diagnostic within 24 hours — two pages, founder-approved, no commitment after.

---

## حدود هذا التقرير — Limits of this report

- لا يتضمّن أي بيانات شخصية (بريد، هاتف، اسم فرد، هوية).
- لا يُسجَّل إلا ما هو منشور علناً.
- الأرقام نشاطية لا إيرادية، وتقديرية لا مُتحقَّقة.

No personal data. Only publicly posted information is recorded. Figures are activity-level and estimated, not revenue or verified.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.**
