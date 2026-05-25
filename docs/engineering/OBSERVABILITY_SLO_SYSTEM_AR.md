# نظام الرصد و SLO

> النسخة الإنجليزية القانونية: [`OBSERVABILITY_SLO_SYSTEM.md`](./OBSERVABILITY_SLO_SYSTEM.md).

## مرجع الدوكترين
- الالتزامات: #2، #4، #5.
- القرارات المثبّتة: سكربتات التحقق مانعة للإصدار.

## الغرض

ضمان أن العمّال والـ APIs والوكلاء والطوابير والـ Actions في Dealix موثوقة، مرصودة، ومحكومة بـ SLOs صريحة. هذي الوثيقة تكمّل `docs/SLO.md` بـ **SLOs تشغيلية** لمصنع الإيرادات.

## السطح الموجود

- structlog JSON logs (`docs/OBSERVABILITY_ENV.md`).
- Request IDs عبر middleware.
- Provider usage metrics.
- Langfuse tracing اختياري.
- `docs/AI_OBSERVABILITY_AND_EVALS.md`.
- `make v5-verify` (22-point production verifier).
- `make v5-snapshot`, `.github/workflows/daily_snapshot.yml`.

## SLOs تشغيلية

- توليد mission control / daily digest: 99% نجاح/ربع.
- نجاح وظائف التصنيف: ≥ 95%.
- توليد طابور الموافقات: يومي على كل يوم عمل.
- زمن توليد draft عرض: خلال 24 ساعة من الطلب.
- طابور متابعة الدفع: يومي.
- p95 latency للعامل: < 5 دقائق.
- عمر تراكم طوابير الموافقة: < ساعة.
- نجاح Moyasar webhook: ≥ 99.5%.
- تجاوزات SLA مركز الموافقات: < 5%.
- وصول عبر المستأجرين المرفوض: صفر (أي محاولة = حادث أمني).

## شروط التنبيه

- عامل فشل 3 مرات متتالية.
- تراكم طابور تجاوز السقف.
- Action يومية ما أنتجت مخرجاتها.
- محاولة فعل خارجي بدون سجل موافقة (حادث أمني، مو تحذير).
- ارتفاع معدّل أخطاء مزوّد AI على 15 دقيقة.
- ارتفاع التكلفة لكل نتيجة بدون تحسّن تحويل.

## مقاييس DORA الهندسية

تردد النشر، lead time للتغيير، معدّل فشل التغيير، متوسط زمن التعافي.

## القواعد الجوهرية

- لكل SLO مصدر حقيقة. ادعاء "99%" يحتاج مسار استعلام للسجلات.
- تجاوز SLO يُسجَّل ويُراجَع، ما يُمتَّع في المتوسط.
- تكامل خارجي جديد ما يصدر قبل توثيق رصده و SLO.
- ادعاءات uptime / موثوقية / أتمتة موفّرة مغلّقة بأرقام مقاسة.

## الربط بالتشغيل

- `docs/SLO.md`, `docs/OBSERVABILITY_ENV.md`, `docs/AI_OBSERVABILITY_AND_EVALS.md`.
- `make v5-verify`.
- `.github/workflows/daily_digest.yml`, `daily_snapshot.yml`.
- `core/queue/worker.py`.
- `db/models.py::AuditLogRecord`.

## روابط ذات صلة

- `docs/SLO.md`
- `docs/OBSERVABILITY_ENV.md`
- `docs/AI_OBSERVABILITY_AND_EVALS.md`
- [`../runtime/WORKER_QUEUE_ARCHITECTURE_AR.md`](../runtime/WORKER_QUEUE_ARCHITECTURE_AR.md)
- [`../finance/AI_UNIT_ECONOMICS_AR.md`](../finance/AI_UNIT_ECONOMICS_AR.md)
- [`../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md`](../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md)
- [`../founder/BOARD_LEVEL_KPI_STACK_AR.md`](../founder/BOARD_LEVEL_KPI_STACK_AR.md)

## بنود مفتوحة

- توجيه التنبيهات ما مركزي بعد (أي تنبيه يروح وين، من في الـ on-call). RFC صغير.
- مقاييس DORA ما تُحسَب آليًا بعد.
- تنبيه عمر التراكم يحتاج مكتبة صغيرة في `core/queue/`.
- بطاقة SLOs أسبوعية في القمرة: مفتوحة.
