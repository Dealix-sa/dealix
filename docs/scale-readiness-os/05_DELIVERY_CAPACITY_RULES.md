# قواعد قدرة التسليم | Delivery Capacity Rules

> **AR:** يحدّد هذا المستند حدود قدرة Dealix على التسليم، لأن التوسّع الذي يتجاوز القدرة يدمّر الجودة والثقة. القاعدة: لا نقبل ما لا نستطيع تسليمه بالجودة المطلوبة، ولا نتوسّع قبل أن تتوفّر قدرة فائضة مثبتة.
>
> **EN:** This document defines Dealix's delivery capacity limits, because scaling beyond capacity destroys quality and trust. The rule: never accept what we cannot deliver to standard, and never scale before proven spare capacity exists.

## مؤشرات القدرة | Capacity Metrics

| المؤشر Metric | الوصف Description |
|---|---|
| القدرة القصوى / Max capacity | أقصى عدد التزامات متزامنة بالجودة / max concurrent commitments at quality |
| الاستغلال الحالي / Current utilization | نسبة القدرة المستخدمة / % of capacity in use |
| القدرة الفائضة / Spare capacity | الفرق المتاح للنمو / available headroom |
| جودة التسليم / Delivery quality | ضمن المعايير المتفق عليها / within agreed standards |

## حدود التشغيل | Operating Limits

| المنطقة Zone | الاستغلال Utilization | الإجراء Action |
|---|---|---|
| آمنة / Safe | < 70% | يمكن قبول مزيد / can accept more |
| تحذير / Caution | 70–85% | مراقبة وعدم التوسّع / monitor, hold scaling |
| حرجة / Critical | > 85% | تجميد القبول + محفّز توظيف / freeze intake + hiring trigger |

## قواعد القبول | Intake Rules

1. لا يُقبل التزام جديد يتجاوز القدرة القصوى. / No new commitment beyond max capacity.
2. الجودة تسبق النمو دائمًا. / Quality precedes growth, always.
3. عند المنطقة الحرجة، يتوقف القبول حتى تتوفر قدرة. / In the critical zone, intake stops until capacity frees.

## العلاقة بالتوسّع | Relation to Scaling

- التوسّع مشروط بقدرة فائضة مثبتة (انظر `01`). / Scaling requires proven spare capacity (see `01`).
- المنطقة الحرجة محفّز توظيف (انظر `03`). / The critical zone is a hiring trigger (see `03`).

## قاعدة الأمان | Safety Rule

> لا قبول ولا توسّع يتجاوز القدرة. لا عائد مضمون يبرّر خفض الجودة. / No intake or scaling beyond capacity. No guaranteed ROI justifies lowering quality.

## مراجع | References

- متى نتوسّع / When to scale: `01_WHEN_TO_SCALE.md`
- محفّزات التوظيف / Hiring triggers: `03_HIRING_TRIGGER_RULES.md`
- التقرير الإثباتي / Evidence report: `99_SCALE_READINESS_REPORT.md`
