# غرفة عمليات الإيرادات

> النسخة الإنجليزية القانونية: [`REVENUE_WAR_ROOM_OS.md`](./REVENUE_WAR_ROOM_OS.md).

## مرجع الدوكترين
- الالتزامات: #1، #2، #5.
- القرارات المثبّتة: السلسلة الذهبية، الموافقة-أولًا.

## الغرض

تجبر Dealix على تحويل النشاط إلى قرارات إيرادات على إيقاع ثابت. الغرفة هي محرّك المؤسس اليومي والأسبوعي لقفل اللفافات وإيقاف ما لا يعمل ومضاعفة ما يعمل.

## الأسئلة اليومية

قبل ما تفتح شيء جديد، جاوب:

1. شي يحرّك النقد اليوم؟
2. أي متابعة متأخرة؟
3. أي عرض يحتاج متابعة دفع؟
4. أي رد إيجابي ما له عينة لحد الآن؟
5. أي قطاع يُظهر إشارة؟
6. ما الذي يجب إيقافه؟

هذي ستة أسئلة هي أجندة الغرفة اليومية. القمرة (`SALES_COCKPIT_SYSTEM_AR.md`) تُظهر السجلات اللي تجاوب عليها.

## القرارات الأسبوعية

- **ضاعف** القطاع/القناة اللي أنتجت ردود مؤهلة أو نقد.
- **أوقف** أضعف قناة/حركة خلال أسبوعين.
- **حسّن** الرسالة، العينة، أو العرض اللي يخسر.
- **عدّل** السعر صعودًا أو هبوطًا بناءً على مراجعة عائد التسعير (`PRICING_YIELD_MANAGEMENT_AR.md`).
- **شحن** عينة أو أصل يفك انسداد رد إيجابي عالق.
- **ادفع** العرض اللي تأخّر متابعة دفعه.
- **اطلب** إحالة واحدة من أقوى عميل نشط.

## القواعد الجوهرية

- لا يُغلَق أسبوع بدون قرار إيرادات مسجّل.
- "نشتغل عليه" ما هو قرار.
- القرار: غيّر X بحلول Y بإشارة Z مع تسجيل النتيجة.
- كل قرار يحمل رابط دليل مصدر.
- القرار اللي طلع غلط يُوثَّق على إنه غلط؛ الدروس في الـ playbook.
- الغرفة ما تنتج وعود نتائج؛ تنتج التزامات بأفعال يتحكم بها Dealix.

## الإيقاع

| الإيقاع | ما يحدث | السطح |
|---------|---------|------|
| كل يوم عمل | الـ digest اليومي يفتح، الستة أسئلة تُجاب، القمرة تُفرَّغ | `make v5-digest`, `daily_digest.yml` |
| نهاية الأسبوع | مراجعة كل قناة، قرار لكل فئة قناة | مذكرة المراجعة الأسبوعية |
| نهاية الشهر | مراجعة KPI على مستوى مجلس | `BOARD_LEVEL_KPI_STACK_AR.md` |

## الربط بالتشغيل

- `.github/workflows/daily_digest.yml`، `make v5-digest`.
- `.github/workflows/daily_snapshot.yml`، `make v5-snapshot`.
- `scripts/dealix_founder_daily_brief.py`.
- `.github/workflows/founder_strongest_ops_daily.yml`, `founder_autonomous_ops_weekly.yml`.
- وثائق الغرفة القائمة: `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md`, `docs/ops/REVENUE_WAR_ROOM_30_DAY_TRACKER.yaml`, `docs/ops/FOUNDER_REVENUE_DAY_ONE_AR.md`.

## روابط ذات صلة

- [`../control_plane/SALES_COCKPIT_SYSTEM_AR.md`](../control_plane/SALES_COCKPIT_SYSTEM_AR.md)
- [`./BOARD_LEVEL_KPI_STACK_AR.md`](./BOARD_LEVEL_KPI_STACK_AR.md)
- [`../distribution/DEALIX_DISTRIBUTION_OS_AR.md`](../distribution/DEALIX_DISTRIBUTION_OS_AR.md)
- [`../distribution/EXPERIMENT_ENGINE_AR.md`](../distribution/EXPERIMENT_ENGINE_AR.md)
- [`../finance/PRICING_YIELD_MANAGEMENT_AR.md`](../finance/PRICING_YIELD_MANAGEMENT_AR.md)
- `docs/transformation/01_doctrine_lock.md`

## بنود مفتوحة

- قالب مذكرة المراجعة الأسبوعية: غير موجود.
- ملف "سجل القرارات" المعياري اللي تكتب فيه المراجعة الأسبوعية: غير موجود.
- الربط بين قرار غرفة العمليات وسجل التجارب: غير رسمي.
