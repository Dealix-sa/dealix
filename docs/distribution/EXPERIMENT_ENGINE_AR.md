# محرك التجارب

> النسخة الإنجليزية القانونية: [`EXPERIMENT_ENGINE.md`](./EXPERIMENT_ENGINE.md).

## مرجع الدوكترين
- الالتزامات: #2، #5.
- القرارات المثبّتة: سكربتات التحقق مانعة للإصدار.

## الغرض

تشغيل تجارب مضبوطة على القطاعات، عناوين المشترين، زوايا الرسائل، العروض، الأسعار، أنواع العينات، إيقاع المتابعات، القنوات، والـ CTAs. أي تغيير في الحركة التجارية يؤثر على السلوك الخارجي = تجربة بفرضية وعينة وقياس وتاريخ قرار ونتيجة مسجّلة.

## أنواع التجارب

تجربة قطاع، تجربة عنوان مشتري، تجربة زاوية رسالة، تجربة CTA، تجربة عرض، تجربة سعر، تجربة عينة، تجربة إيقاع متابعة، تجربة قناة.

## الحقول الإلزامية لكل تجربة

`hypothesis`, `variable`, `control`, `sample_size`, `success_metric`, `decision_date`, `result`, `decision`, `owner`, `evidence_link`.

## مقاييس النجاح

معدّل الرد، معدل الرد الإيجابي، معدل طلب العينة، معدل العرض، تحويل الدفع، معدل الشكاوى/opt-out (سور حماية — ما نقايض التحويل بضرر ثقة)، زمن الدورة من أول لمسة إلى عرض.

## القواعد الجوهرية

- لا توسعة بدون سجل تجربة.
- ما تقارن تجارب بظروف ضبط أو أحجام عينات مختلفة.
- لكل تجربة شرط إيقاف (kill condition) — تجاوز الشكاوى/الـ opt-out للعتبة ينهي التجربة حتى لو التحويل ممتاز.
- التجارب اللي تمس إرسالًا خارجيًا تمر بنفس بوابات الموافقة.
- "نتيجة غير حاسمة" نتيجة شرعية؛ ما نتبنى على دليل ضعيف.

## الربط بالتشغيل

- `evals/`.
- `auto_client_acquisition/crm_v10/lead_scoring.py`, `auto_client_acquisition/icp_scorer.py` (الضبط الأساسي).
- `auto_client_acquisition/revenue_memory/event_store.py`.
- `db/models.py::AuditLogRecord`.

## سجل التجارب

اليوم: مكتوب في `docs/growth/` ومواقع مماثلة. الهدف: ملف واحد `evals/experiment_registry.yaml` مع CLI للمراجعة والقرار.

## روابط ذات صلة

- [`./DEALIX_DISTRIBUTION_OS_AR.md`](./DEALIX_DISTRIBUTION_OS_AR.md)
- [`./EMAIL_DELIVERABILITY_SYSTEM_AR.md`](./EMAIL_DELIVERABILITY_SYSTEM_AR.md)
- [`../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md`](../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md)
- `docs/EVALS_RUNBOOK.md`
- [`../founder/REVENUE_WAR_ROOM_OS_AR.md`](../founder/REVENUE_WAR_ROOM_OS_AR.md)

## بنود مفتوحة

- ملف سجل تجارب واحد: غير موجود.
- CLI لعرض تجارب الأسبوع القادم وقرارات الأسبوع الماضي: غير موجود.
- عتبات سور الحماية معرّفة في وثيقة قابلية التسليم، لكنها ما تُفرَض وقت إغلاق التجربة في السجل.
