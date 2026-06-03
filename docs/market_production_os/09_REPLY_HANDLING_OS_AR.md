# 09 — معالجة الردود — Reply Handling OS

> الموقع في الطبقة: المكوّن رقم 10 من *Market Production OS*. يأتي مباشرة بعد *Sending Ramp OS*،
> ويسبق *WhatsApp Post-Reply OS*. العمود الفقري: [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md).

هذا المستند يحدّد كيف يستقبل النظام الردود الواردة على المسوّدات المعتمدة والمُرسَلة، ويصنّفها إلى فئات
ثابتة، ويختار لكل فئة **إجراءً واحدًا واضحًا**. كل إجراء تالٍ هو نفسه مسودة جديدة تخضع للقاعدة الحاكمة:
**250 مسودة/يوم، صفر إرسال تلقائي.** لا يتحوّل أي رد إلى رسالة خارجية إلا بموافقة المؤسس.

> القاعدة الأساسية هنا: **التصنيف آلي، الإجراء مُسوَّد، الإرسال بشري.** المعالجة لا تُنشئ قناة باردة جديدة أبدًا.

---

## 0. المبدأ الحاكم لطبقة الردود

- الرد الوارد هو **إشارة موافقة ضمنية على المتابعة** في نفس القناة فقط (البريد يبقى بريدًا حتى يطلب العميل غير ذلك).
- لا فتح قناة جديدة (واتساب/هاتف) إلا إذا طلبها العميل صراحةً — انظر [`10_WHATSAPP_POST_REPLY_OS_AR.md`](10_WHATSAPP_POST_REPLY_OS_AR.md).
- كل رد يُسجَّل بحقل `governance_decision` و `evidence_level`، بلا PII خام في السجلات.
- الكبح (Suppression) لفئتي `unsubscribe` و `angry` **فوري ودائم**، ولا يحتاج موافقة لتفعيله — الموافقة مطلوبة للإرسال، لا للإيقاف.

---

## 1. فئات الردود العشر والإجراء لكل فئة

| الفئة (reply_class) | الوصف المختصر | الإجراء التالي (مسودة) | الكبح |
|---|---|---|---:|
| `positive` | اهتمام واضح / طلب اجتماع | دعوة جلسة اكتشاف (Discovery) + رابط حجز | لا |
| `interested_later` | مهتم لكن التوقيت غير مناسب | جدولة متابعة في `nurture` بتاريخ متّفق + ملاحظة بلا ضغط | لا |
| `price_question` | سؤال عن السعر/الباقات | بطاقة عرض (Offer Card) من السلّم الخماسي الرسمي | لا |
| `send_more_info` | طلب تفاصيل/أمثلة إضافية | حزمة إثبات (Proof Pack) مختصرة + نمط قطاعي آمن | لا |
| `wrong_person` | لست الجهة المعنية | طلب إحالة مهذّب لاسم/قسم الجهة الصحيحة | لا |
| `not_interested` | رفض صريح دون عدائية | شكر مهذّب + إيقاف التسلسل الحالي (no further sends) | لا |
| `unsubscribe` | طلب إزالة من القائمة | تأكيد إزالة فوري | **فوري ودائم** |
| `angry` | استياء/شكوى/تهديد قانوني | اعتذار مختصر + كبح فوري + إخطار المؤسس | **فوري ودائم** |
| `auto_reply` | رد آلي (إجازة/خارج المكتب) | لا إجراء بشري؛ إعادة الجدولة بعد تاريخ العودة إن وُجد | لا |
| `bounce` | فشل تسليم (hard/soft) | كبح البريد عند hard bounce؛ مراقبة soft | كبح البريد |

> ملاحظة تصنيف: `not_interested` يوقف التسلسل لكنه **لا** يُدخِل العنوان قائمة الكبح الدائمة — العميل قد
> يعود لاحقًا عبر قناة واردة جديدة. أمّا `unsubscribe` و `angry` فدائمان بلا استثناء.

---

## 2. تفصيل الإجراءات

### 2.1 `positive` → دعوة اكتشاف
- مسودة رد قصيرة تقترح موعدين محدّدين + رابط حجز ذاتي.
- تسأل العميل عن قناته المفضّلة للمتابعة (بريد / مكالمة / واتساب). لا نفترض واتساب.
- إذا اختار العميل واتساب أو الحجز، يُسلَّم التدفّق إلى [`10_WHATSAPP_POST_REPLY_OS_AR.md`](10_WHATSAPP_POST_REPLY_OS_AR.md).

### 2.2 `price_question` → بطاقة عرض
- لا نخترع سعرًا. مصدر الحقيقة الوحيد هو السلّم الخماسي في
  [العمود الفقري §5](00_MARKET_PRODUCTION_OS_MASTER_AR.md).
- البطاقة تربط السعر بالألم المعلَن وبمستوى الإثبات المتوقّع، دون أي ضمان نتائج.

### 2.3 `send_more_info` → حزمة إثبات
- ترسل نمطًا قطاعيًا آمنًا (case-safe)، أو ملخّص حزمة إثبات، أو رؤية قطاعية مجمّعة.
- ممنوع إرسال أسماء عملاء أو أرقام غير مُتحقَّقة. الأرقام مسموحة فقط إذا كانت Client-Confirmed.

### 2.4 `wrong_person` → طلب إحالة
- رسالة مهذّبة تطلب اسم/قسم الجهة المعنية. لا ضغط، ولا إرسال للعنوان الجديد قبل موافقة المؤسس.

### 2.5 `unsubscribe` / `angry` → كبح فوري
- يُضاف العنوان فورًا إلى `schemas/suppression.schema.json` بحالة `permanent`.
- `unsubscribe`: تأكيد إزالة من سطر واحد، بلا محاولة استبقاء.
- `angry`: اعتذار من جملة واحدة + إيقاف كامل + إخطار المؤسس لمراجعة السبب (قد يكون عيب استهداف).

### 2.6 `auto_reply` / `bounce` → بلا إجراء بشري
- `auto_reply`: لا يُحتسب ردًّا بشريًا؛ إن وُجد تاريخ عودة، يُعاد جدولة المتابعة بعده.
- `bounce`: hard bounce → كبح فوري للبريد (حماية سمعة الدومين). soft bounce → مراقبة وإعادة محاولة محدودة.

---

## 3. المخطط (Schema) وإعادة الاستخدام

- المخطط الرسمي للرد: `schemas/reply.schema.json` (قيد البناء من قِبل المؤسس) — يحمل
  `reply_class`، `confidence`، `recommended_action`، `governance_decision`، `suppression_flag`.
- التصنيف والتوجيه يعيدان استخدام الوحدات الموجودة، ولا يُنشئان منطق صندوق وارد جديد:
  - `auto_client_acquisition/support_inbox/` (مراقبة SLA + مخزن الحالة + التصعيد).
  - `auto_client_acquisition/customer_inbox_v10/` (`reply_suggestion.py`، `routing_policy.py`،
    `consent_status.py`، `escalation.py`).
- التوجيه البرمجي الجديد رقيق: `auto_client_acquisition/market_production_os/reply_router.py`
  (يربط الفئة بالإجراء، ويختم كل إجراء بـ `send_status = "draft"`).

> أعد الاستخدام قبل أن تكتب: منطق الصندوق الوارد، الموافقة، والكبح كلها موجودة. هذا المستند يصف
> **سياسة التصنيف والإجراء**، لا بنية تقنية جديدة.

---

## 4. الكبح والامتثال (Suppression & Compliance)

| الحالة | متى | الأثر | قابل للتراجع؟ |
|---|---|---|---:|
| Unsubscribe | طلب صريح | كبح دائم لكل القنوات | لا (إلا بطلب وارد جديد من العميل) |
| Angry | شكوى/تهديد | كبح دائم + إخطار المؤسس | لا |
| Hard bounce | فشل تسليم نهائي | كبح البريد فقط | لا |
| Not interested | رفض مهذّب | إيقاف التسلسل الحالي | نعم (قناة واردة لاحقة) |

- فحص الكبح إلزامي **قبل** أي مسودة جديدة لأي عنوان (شرط الإرسال في
  [العمود الفقري §7](00_MARKET_PRODUCTION_OS_MASTER_AR.md)).
- لا يُرسَل أي إجراء تالٍ لعنوان موجود في قائمة الكبح، حتى لو كان الرد `positive` لاحقًا عبر تسلسل قديم.

---

## 5. مؤشرات الفئة (تُغذّي التقرير اليومي)

عدد الردود لكل فئة، نسبة `positive` من إجمالي الردود، عدد `unsubscribe` و `angry` (إشارة جودة استهداف)،
ومصدر أعلى `bounce`. تُجمَّع هذه الأرقام في تقرير GTM اليومي — انظر
[`14_GTM_METRICS_AND_LEARNING_AR.md`](14_GTM_METRICS_AND_LEARNING_AR.md). ارتفاع `angry`/`unsubscribe`
من قطاع أو مصدر واحد = جرس إنذار لمراجعة الاستهداف، لا لزيادة الإرسال.

---

## 6. اللاءات المطبَّقة هنا

- لا فتح قناة واتساب باردة من رد بريدي — الانتقال للواتساب بطلب العميل فقط.
- لا إرسال لأي عنوان مكبوح. لا تجاهل opt-out. لا PII في سجلات الردود.
- لا إجراء خارجي (إحالة/عرض/حزمة) بدون موافقة المؤسس. الكبح وحده فوري بلا موافقة.

---

## EN summary

Reply Handling OS is component #10 of the Market Production OS. Every inbound reply is auto-classified
into ten fixed classes (`positive`, `interested_later`, `price_question`, `send_more_info`,
`wrong_person`, `not_interested`, `unsubscribe`, `angry`, `auto_reply`, `bounce`) and mapped to exactly
one next action drafted for founder approval. Mapping: positive → discovery invite; price_question →
offer card (from the official five-tier ladder, never invented); send_more_info → proof pack;
wrong_person → referral ask; not_interested → stop the sequence; unsubscribe → immediate permanent
suppression; angry → one-line apology plus immediate permanent suppression plus founder notification;
auto_reply → reschedule, no human action; bounce → suppress the email on hard bounce. Suppression for
unsubscribe and angry is immediate and permanent and does not require approval — approval gates sending,
not stopping. Classification and routing reuse `support_inbox/` and `customer_inbox_v10/`; the thin new
glue is `market_production_os/reply_router.py` against `schemas/reply.schema.json`. A WhatsApp handoff
happens only when the customer explicitly asks for it (see `10_WHATSAPP_POST_REPLY_OS_AR.md`). No cold
channel is ever opened from a reply; the core rule holds: 250 drafts/day, 0 auto-sends.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
