# اقتصاد الوحدة لاستخدام AI

> النسخة الإنجليزية القانونية: [`AI_UNIT_ECONOMICS.md`](./AI_UNIT_ECONOMICS.md).

## مرجع الدوكترين
- الالتزامات: #2، #5.
- القرارات المثبّتة: سكربتات التحقق مانعة للإصدار.

## الغرض

تتبّع هل استخدام AI ينتج رافعة مربحة. كل استدعاء LLM، تضمين، استرجاع، كتابة في vector store، واستدعاء أداة يكلّف. النظام يقيس **التكلفة لكل نتيجة** (عميل، draft، عينة، عرض، رد مؤهل، عميل مدفوع) ويفرض إعادة توجيه أو تخفيض لما التكلفة تطلع بدون تحسّن تحويل.

## فئات التكلفة

| الفئة | المصدر |
|------|--------|
| Input tokens | سجلات المزوّد |
| Output tokens | سجلات المزوّد |
| Embedding tokens | سجلات مزوّد الـ embeddings |
| Vector store ops | سجلات vector store |
| استدعاءات أدوات/APIs | سجلات لكل مزوّد |
| ARQ + Redis + Action minutes | سجلات البنية |
| تخزين | استخدام DB/التخزين |

## مؤشرات التكلفة لكل نتيجة

تكلفة LLM لكل عميل في قاعدة الذكاء، تكلفة الإثراء، تكلفة التصنيف، تكلفة draft، تكلفة عينة، تكلفة draft عرض، تكلفة لكل رد إيجابي، تكلفة لكل sprint/عميل مدفوع.

## القواعد الجوهرية

- ارتفاع التكلفة بدون تحسّن مماثل في التحويل أو الجودة → خفّض، أعد التوجيه، أو نزّل النموذج.
- فضّل المسارات الحتمية والـ retrieval-augmented على freeform عالي tokens حيث بيانات التحويل متعادلة.
- التوزيع لكل مستأجر إلزامي؛ تذويب التكلفة عبر المستأجرين ممنوع.
- ادعاءات "وفر تكلفة" أو "أتمتة موفّرة" التي تُسلَّم للعملاء لازم تشير لخط أساس مقاس وآخر بعد التغيير مقاس — لا تقديرات.
- ترقية نموذج = قرار تسعير: تحتاج رفع جودة مقاس أو تخفيض تكلفة.

## الإيقاع

- يومي: لوحة التكلفة في الـ digest اليومي.
- أسبوعي: مراجعة التكلفة لكل نتيجة.
- شهري: قرار توجيه النموذج والمزوّد.

## الربط بالتشغيل

- structlog JSON logs + provider usage metrics في `docs/OBSERVABILITY_ENV.md`.
- Langfuse tracing اختياري.
- `db/models.py::BackgroundJobRecord`.
- `auto_client_acquisition/revenue_memory/event_store.py`.
- `dashboard/pages/` (صفحة Costs موجودة).

## روابط ذات صلة

- `docs/UNIT_ECONOMICS_AND_MARGIN.md`
- `docs/company/UNIT_ECONOMICS.md`
- [`./PRICING_YIELD_MANAGEMENT_AR.md`](./PRICING_YIELD_MANAGEMENT_AR.md)
- [`./BILLING_RECEIVABLES_OS_AR.md`](./BILLING_RECEIVABLES_OS_AR.md)
- `docs/AI_OBSERVABILITY_AND_EVALS.md`
- [`../engineering/OBSERVABILITY_SLO_SYSTEM_AR.md`](../engineering/OBSERVABILITY_SLO_SYSTEM_AR.md)
- [`../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md`](../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md)

## بنود مفتوحة

- عرض توزيع التكلفة لكل مستأجر كـ panel من الدرجة الأولى: غير موجود.
- مؤشرات التكلفة لكل نتيجة تعتمد على كل نتيجة كحدث مسجّل؛ النتائج للعينات والعروض جزئية.
- توجيه النموذج اليوم نوعي؛ ملف سياسة توجيه موثّق مفتوح.
