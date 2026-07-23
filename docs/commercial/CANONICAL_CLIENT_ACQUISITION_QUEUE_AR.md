# Dealix Canonical Client Acquisition Queue

## الهدف

تحويل الإشارات الدافئة أو الواردة أو المحالة أو المعتمدة صراحةً إلى قائمة داخلية مرتبة توضح:

- من يستحق المراجعة أولًا؛
- لماذا؛
- ما العرض الأنسب؛
- ما الاعتراض المتوقع؛
- ما الدليل المطلوب؛
- وما الإجراء التالي الذي يحتاج موافقة المؤسس.

هذه الطبقة ليست CRM مستقلًا، ولا runner يوميًا، ولا نظام إرسال. هي مكتبة صغيرة تُستهلك لاحقًا من Canonical Company OS بعد دمج العمود الموحد.

## سياسة المصدر والإذن

المصادر القابلة لإعداد مسودة تواصل للمراجعة فقط:

- `inbound`
- `warm`
- `referral`
- `existing_permission`
- `opt_in`
- `customer_request`
- `manual_approved`

مصادر البحث فقط:

- `manual_research`
- `public_web_research`
- `seed`
- `unknown`

مصدر البحث فقط يبقى `research_hold` مهما ارتفع score، ويكون:

- `recommended_channel=none_research_only`
- `suggested_copy` فارغًا
- الإجراء التالي: إثبات الإذن أو الحصول على warm introduction

لا تدخل قوائم scraped أو أرقام واتساب باردة أو مصادر غير معروفة للنظام. أي source خارج allowlist يُرفض بدل تمريره بصمت.

## المخرجات

كل Queue Item يحتوي:

- priority score وسبب ترتيبه؛
- حالة الإذن `confirmed` أو `research_only` داخل سبب الترتيب؛
- status: `needs_founder_review` أو `research_hold`؛
- قناة يدوية بعد الموافقة للمصادر المصرح بها فقط؛
- زاوية سعودية/قطاعية؛
- مسودة غير مرسلة للمصادر المصرح بها فقط؛
- اعتراض متوقع؛
- proof to show؛
- `approval_required=true`؛
- `external_action_allowed=false`.

## عقد الأمان

1. الوضع الوحيد المقبول هو `draft-only`.
2. لا توجد دوال إرسال أو نشر أو دفع.
3. لا تُسجل إيرادات قبل دليل دفع مؤكد.
4. لا تُستخدم claims بدون proof.
5. السعر والنطاق والتسليم تحتاج موافقة.
6. أي قناة خارجية تبقى يدوية حتى اعتماد action محدد.
7. score مرتفع لا يتجاوز غياب الإذن.
8. research source لا يتحول تلقائيًا إلى outreach source.

## ترتيب الدمج

1. استعادة Railway production deploy (#898).
2. دمج Canonical Company OS (#886).
3. ربط هذه المكتبة بالـOpportunity Graph والـApproval Queue داخل العمود الموحد.
4. إضافة مصادر دافئة صغيرة فقط: Gmail replies، Calendar notes، CRM/Sheet approved rows.
5. لا يُضاف workflow أو scheduler مستقل.
