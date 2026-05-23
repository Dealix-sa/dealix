# قائمة إغلاق فجوات PDPL (تشغيل + منتج)

**تحذير:** لا تغني عن مراجعة قانونية / DPO. تستند إلى فجوات مسجّلة في [dealix/registers/no_overclaim.yaml](../../dealix/registers/no_overclaim.yaml) (`pdpl_readiness`).

## فجوات حالية (من السجل)

- سجل DPO / نقطة اتصال حوكمة.
- Runbook خرق بيانات مع مؤقتات (إشعار SDAIA حيث ينطبق القانون).
- جداول احتفاظ مفعّلة في قاعدة البيانات (ليس فقط وثائق).

## إجراءات تقنية موجودة أو مرجعية

- تدقيق مسارات بيانات شخصية على مستوى API: `AuditLogMiddleware` في [api/middleware/http_stack.py](../../api/middleware/http_stack.py).
- تقليل البيانات في السجلات (تجنب query params في مسار التدقيق).

## قائمة تحقق قبل ادّعاء «جاهزية أعلى»

- [ ] تسجيل أنشطة الوصول للبيانات الشخصية في بيئة الإنتاج (SIEM أو ما يعادلها).
- [ ] إجراءات طلبات الأفراد (وصول/تصحيح/حذف) موثّقة ومُختبَرة على مسار واحد على الأقل.
- [ ] اتفاقيات المعالجة مع البائعين الفرعيين (DPA) للخدمات التي تلمس بيانات أفراد.
- [ ] تمرين خرق وهمي — راجع [dealix/masters/incident_rollback_runbook.md](../../dealix/masters/incident_rollback_runbook.md).

## بعد الإغلاق

- حدّث `no_overclaim` — لا ترفع الحالة إلى «امتثال كامل» دون توقيع قانوني.

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
