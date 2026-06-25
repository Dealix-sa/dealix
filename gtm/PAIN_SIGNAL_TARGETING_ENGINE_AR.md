# Pain Signal Targeting Engine

## الهدف

تحويل الاستهداف من رسائل عامة إلى تشخيص تجاري مخصص لكل شركة.

Dealix لا يبدأ بالسؤال: ماذا نرسل؟

Dealix يبدأ بالسؤال: ما الألم المرجح؟ من صاحب القرار؟ ما العرض الأصغر الذي يثبت القيمة؟

## الحقول الأساسية

| Field | Required | Notes |
|---|---:|---|
| company_name | yes | اسم الشركة |
| sector | yes | القطاع |
| city | optional | المدينة |
| source_url | yes | مصدر علني للتحقق |
| verification_status | yes | unverified, website_found, ready_for_review, approved |
| buyer_persona | yes | المالك، مدير المبيعات، العمليات، التسويق |
| pain_hypothesis | yes | فرضية وليست حقيقة مؤكدة |
| pain_evidence | optional | إشارة عامة من الموقع أو القطاع |
| recommended_offer | yes | العرض المناسب |
| confidence | yes | low, medium, high |
| next_action | yes | review, call, draft, discard |

## pain signals حسب القطاع

### العيادات

- حجوزات ومتابعات تضيع.
- واتساب بدون queue واضح.
- لا يوجد تقرير يومي للمالك.

Best offer: Follow-up Recovery OS.

### العقار

- lead leakage.
- follow-up غير موحد.
- العروض لا تملك next action.

Best offer: Revenue Command Room OS.

### اللوجستيات

- دورة بيع B2B طويلة.
- عروض ومتابعات مع أكثر من صاحب قرار.
- صعوبة معرفة الحسابات الساخنة.

Best offer: Revenue Command Room OS.

### التدريب

- استفسارات تسجيل كثيرة.
- cohort pipeline غير واضح.
- متابعة قبل بداية الدفعة ضعيفة.

Best offer: Follow-up Recovery OS.

### وكالات التسويق والخدمات

- تقارير العملاء متفرقة.
- proof of work ضعيف.
- renewal conversation متأخر.

Best offer: Client Delivery OS.

## قواعد الاستهداف

- 100 بحث يوميًا لا يعني 100 إرسال.
- لا يتم التواصل بدون review.
- كل target يحتاج source_url.
- كل pain يكتب كفرضية.
- لا تستخدم لغة تهديد أو ادعاء معرفة داخلية.
- الأولوية للشركات التي يظهر لديها ألم تشغيلي واضح.

## daily funnel

| Stage | Daily target |
|---|---:|
| researched accounts | 100 |
| verified accounts | 40 |
| sales packs | 25 |
| founder-reviewed drafts | 10-15 |
| calls | 3 |
| discovery calls | 1-2 |
| proposals | 1 |

## output

كل شركة مؤهلة تحصل على sales pack فيه:

- company snapshot
- pain hypothesis
- recommended product
- first message draft
- discovery questions
- objection notes
- proposal angle
- next action
