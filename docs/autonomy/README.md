# Dealix — معمار العمليات الذاتية · Autonomous Operations Architecture

**الحالة / Status:** DRAFT — architecture
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18

هذه الطبقة تصمّم **هرم الوكلاء الكامل** الذي يشغّل عمليات Dealix ذاتياً — مع بوابة موافقة عند
كل حدّ خارجي. الأتمتة = المكينة تنجز 100% من التحضير والتحليل والصياغة والتقييم والجدولة
والمراقبة؛ المؤسس يوافق على كل إجراء خارجي (إرسال/دفع). **L5 محظور؛ الحدّ الأقصى L4 (داخلي
ومُدقَّق فقط).** وثائق تصميمية — لا تُرخّص كوداً جديداً (التجميد التجاري نشط).

This layer designs the **full agent pyramid** that runs Dealix operations autonomously, with
an approval gate at every external boundary. Automation = preparation + queuing; the founder
approves every external action. L5 is blocked; max is L4 (internal, audited only). Design
docs — they authorize no new product code while the Commercial Freeze is active.

ابدأ من / Start at: [`AUTONOMOUS_OPS_ARCHITECTURE.md`](AUTONOMOUS_OPS_ARCHITECTURE.md).

| الوثيقة / Document | الغرض / Purpose |
|---|---|
| [AUTONOMOUS_OPS_ARCHITECTURE.md](AUTONOMOUS_OPS_ARCHITECTURE.md) | المعمار الرئيسي: الهرم ثلاثي الطبقات + العمود الفقري للحوكمة · master architecture |
| [AGENT_ROSTER.md](AGENT_ROSTER.md) | سجل كل وكيل: هوية، طبقة، نطاق، مستوى استقلالية، الوحدة الداعمة · full agent roster |
| [ORCHESTRATION_AND_AUTONOMY_LADDER.md](ORCHESTRATION_AND_AUTONOMY_LADDER.md) | التنسيق + سلّم الاستقلالية L0–L4 + توجيه الموافقات · orchestration & ladder |
| [SALES_AUTONOMY_SYSTEM.md](SALES_AUTONOMY_SYSTEM.md) | نظام المبيعات الذاتي — قمع كامل approval-first · autonomous sales funnel |
| [INTERNAL_OPS_AUTONOMY.md](INTERNAL_OPS_AUTONOMY.md) | استقلالية التسليم/المالية/الدعم/البيانات/الحوكمة · internal ops autonomy |
| [AGENT_GOVERNANCE_AND_GUARDRAILS.md](AGENT_GOVERNANCE_AND_GUARDRAILS.md) | حوكمة الوكلاء: الهوية، الحدود الأربع، kill-switch، التدقيق · governance & guardrails |
| [AUTONOMY_BUILD_ROADMAP.md](AUTONOMY_BUILD_ROADMAP.md) | خارطة البناء على مراحل تحترم التجميد · staged, freeze-respecting build roadmap |

**وثائق مرافقة / Companion layers:** [`../launch/MASTER_LAUNCH_OS.md`](../launch/MASTER_LAUNCH_OS.md) ·
[`../commercial/COMMERCIAL_CONTROL_TOWER.md`](../commercial/COMMERCIAL_CONTROL_TOWER.md)

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
