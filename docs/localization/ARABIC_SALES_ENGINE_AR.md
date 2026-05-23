# محرّك المبيعات العربية

> النسخة الإنجليزية القانونية: [`ARABIC_SALES_ENGINE.md`](./ARABIC_SALES_ENGINE.md).

## مرجع الدوكترين
- الالتزامات: #2، #5.
- القرارات المثبّتة: الموافقة-أولًا.

## الغرض

يخلّي Dealix يبيع بشكل طبيعي بالعربية والإنجليزية للمشتري السعودي B2B. الجانب العربي ليس طبقة ترجمة — هو حركة مبيعات من الدرجة الأولى لها لهجتها ومفرداتها وعباراتها القطاعية وإثباتاتها. الترجمة الحرفية من الإنجليزية = فشل.

## الأصول

- تواصل عربي قطاعي.
- تواصل إنجليزي مقابل.
- عروض ثنائية اللغة.
- نسخة landing عربية قطاعية.
- إثبات قطاعي بالعربية السعودية للأعمال.
- دليل لهجة أعمال سعودية.
- قوائم مفردات قطاعية.

## قواعد اللهجة

- العربية تشبه التواصل التجاري السعودي، مو الفصحى الأدبية، ولا العامية المصرية.
- اللهجة تتغير حسب القطاع وأقدمية المشتري (مشتريات vs CEO vs CTO).
- الألقاب والتحيات تتبع أعراف الأعمال السعودية.
- لا ترجمة حرفية من تراكيب إنجليزية (إيقاع الجمل، أمثلة، شعارات).
- الأرقام والتواريخ بالعرف اللي يتوقعه القارئ في وثائق الأعمال.
- أسماء العلامة والمنتج تبقى بالشكل الإنجليزي إلا إذا فيه شكل عربي راسخ.

## القواعد الجوهرية

- الأصل العربي اللي بدأ كـ draft إنجليزي يُعاد كتابته بمراجِع سعودي للأعمال، مو يطلع من LLM وينشحن مباشرة.
- أي ادعاء عام ثنائي اللغة يُراجَع باللغتين؛ التعارض بين العربي والإنجليزي = خرق جودة.
- التواصل العربي محكوم بالموافقة مثل أي تواصل.
- ملاحظات المشتري بالعربية تُسجَّل بشكلها الأصلي (لا خسارة ترجمة).
- دليل اللهجة وثيقة حية؛ المراجعون يضيفون المفردات القطاعية الجديدة.

## الإيقاع

- لكل حملة: نسختان (AR/EN) تُراجَعان.
- أسبوعي: مفردات قطاعية جديدة من محادثات المشترين.
- شهري: مراجعة دليل اللهجة.

## الربط بالتشغيل

- `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md`, `docs/ops/FOUNDER_REVENUE_DAY_ONE_AR.md`, `README.ar.md`, وملفات `_AR.md` المرافقة عبر التوثيق.
- `docs/localization/` (موجود).
- `docs/commercial/operations/targeting/ABM_WAVE1_ICP_AR.md`.
- `auto_client_acquisition/approval_center/approval_policy.py`.
- [`../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md`](../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md).

## روابط ذات صلة

- `docs/localization/`
- [`../distribution/DEALIX_DISTRIBUTION_OS_AR.md`](../distribution/DEALIX_DISTRIBUTION_OS_AR.md)
- [`../distribution/EMAIL_DELIVERABILITY_SYSTEM_AR.md`](../distribution/EMAIL_DELIVERABILITY_SYSTEM_AR.md)
- [`../distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md`](../distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md)
- [`../intelligence/COMPETITIVE_INTELLIGENCE_MACHINE_AR.md`](../intelligence/COMPETITIVE_INTELLIGENCE_MACHINE_AR.md)
- [`../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md`](../evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md)
- `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md`

## بنود مفتوحة

- "دليل لهجة الأعمال السعودية" كملف مرجعي واحد في `docs/localization/`: غير موجود.
- قوائم المفردات القطاعية: جزئية.
- LLM ينتج drafts عربية لكنها تستفيد من مراجِع بشري؛ عملية مراجعة من خطوتين موثّقة مفتوحة.
- قائمة فحص مراجعة landing عربية مفتوحة.
