# Dealix Canonical Deal Intelligence Core

## الهدف

استخراج ذاكرة الصفقة، تحليل المرحلة، next-best-action، والـweighted forecast كطبقة خالصة قابلة لإعادة الاستخدام، بدون إنشاء Company OS أو runner أو workflow أو sender موازٍ.

هذه الطبقة تُبنى فوق Acquisition Queue في #899 وتُستهلك لاحقًا من Canonical Company OS #886.

## ما الذي لا تفعله

- لا تبحث عن شركات.
- لا تجمع بيانات أو contacts.
- لا تكتب رسائل تواصل.
- لا ترسل أو تنشر.
- لا تنشئ فاتورة أو تخصم.
- لا تحدث CRM خارجيًا.
- لا تشغل schedule.
- لا تعتمد على بيانات عميل committed داخل GitHub.

## العقد

### 1. Consent قبل النشاط الخارجي

تستورد مصادر الاتصال المسموح بها من Acquisition Queue الكانونية. إذا كان المصدر `manual_research` أو `public_web_research` أو `seed` أو `unknown`:

- المرحلة تبدأ `research_hold`؛
- forecast probability = 0؛
- next action هو إثبات الإذن أو warm intro؛
- أي `message_sent` مسجل بلا إذن يصبح anomaly ولا يرفع المرحلة.

### 2. Evidence لا يقفز فوق المتطلبات

المسار المالي الصحيح:

```text
invoice_sent
→ payment_received
→ proof_pack_delivered
→ closed_won (اختياري)
```

- payment بلا invoice سابق لا يسجل إيرادًا.
- proof بلا payment صالح لا يثبت close.
- `closed_won` لا يثبت شيئًا إذا سبق payment+proof.
- أدلة صفقات مختلفة لا تُجمع.

### 3. Revenue وForecast

- recognized revenue = قيمة الصفقات التي لديها `payment_received` صالح بعد `invoice_sent` في نفس DealRecord.
- open pipeline يستبعد المدفوع والمفقود.
- weighted pipeline يستخدم probabilities محافظة للصفقات المفتوحة فقط.
- البحث بلا consent يساوي forecast صفر، مهما كانت قيمة الصفقة النظرية.

### 4. Next Best Action

المكتبة تعيد `action_key + rationale + requires_approval` فقط. لا تولد copy ولا تنفذ action.

أمثلة:

- `obtain_permission_or_warm_intro`
- `prepare_first_touch_draft`
- `prepare_follow_up_draft`
- `prepare_scope_and_proposal`
- `follow_up_payment_evidence`
- `deliver_and_prepare_proof`
- `prepare_referral_or_retainer_review`
- `repair_evidence_chain`

كل action خارجي يبقى `external_action_allowed=false`.

### 5. Durable Memory

`store.py` لا يحدد مسارًا افتراضيًا ولا يكتب بيانات عميل في الريبو. المستدعي يمرر runtime path خاصًا.

- الملف يحمل schema version واضحًا.
- الكتابة atomic عبر temporary file + replace.
- JSON الفاسد أو schema غير الصحيح يفشل بـ`DealBookError`.
- لا يعود إلى CRM فارغ بصمت، لأن ذلك يخفي فساد البيانات وقد يسبب ضياع الحالة.

## ترتيب الدمج

1. #898: استعادة Railway token والنشر.
2. #900 ثم #901: عقد الطلب والإغلاق اليدوي.
3. #886: العمود التنفيذي الكانوني بعد موافقة الدمج.
4. #899: Acquisition Queue داخل العمود الكانوني.
5. هذه الطبقة: ربط الصفقات والforecast والـNBA بالعمود نفسه، بدون runner جديد.

## الاختبارات

تغطي:

- سلسلة evidence صحيحة؛
- رفض payment قبل invoice؛
- عدم دمج أدلة شركات مختلفة؛
- consent gate حتى للصفقة عالية القيمة؛
- عدم رفع stage عند contact بلا إذن؛
- forecast يستبعد paid/lost؛
- `closed_won` بعد payment+proof فقط؛
- stalled rationale بلا تنفيذ؛
- atomic storage؛
- malformed state يفشل بصوت واضح.
