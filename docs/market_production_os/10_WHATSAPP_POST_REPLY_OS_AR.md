# 10 — واتساب بعد الرد — WhatsApp Post-Reply OS

> الموقع في الطبقة: المكوّن رقم 15 من *Market Production OS*. لا يبدأ هذا التدفّق إلا **بعد** رد إيجابي
> ومعالجته في [`09_REPLY_HANDLING_OS_AR.md`](09_REPLY_HANDLING_OS_AR.md). العمود الفقري:
> [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md).

هذا المستند يحدّد كيف ينتقل العميل من **رد بريدي إيجابي** إلى متابعة على واتساب أو حجز موعد — وذلك
فقط حين يطلب العميل ذلك صراحةً. واتساب في Dealix **ليس قناة باردة أبدًا**: لا توجد رسالة واتساب أولى
بلا رد/موافقة سابقة. كل خطوة هنا **بطاقة إجراء (Action Card)** تُسوَّد للمؤسس، لا رسالة تُرسَل تلقائيًا.

> القاعدة الأساسية: **القناة تُفتح بطلب العميل، تُدار ببطاقات، وتُرسَل بموافقة المؤسس.** 250 مسودة/يوم، صفر إرسال تلقائي.

---

## 0. الحدود غير القابلة للتفاوض

- **لا واتساب بارد.** لا رسالة أولى بلا رد وارد سابق وموافقة مُسجَّلة.
- **لا واتساب جماعي (bulk).** لا قوائم بث، لا قوالب مُرسَلة على دفعات، لا تواصل خارجي مُؤتمت.
- **لا إرسال خارجي تلقائي.** كل رسالة واتساب صادرة تمرّ ببوابة موافقة المؤسس.
- **توجّه Meta 2026:** تتجه Meta لتقييد روبوتات الدردشة عامة الغرض (general-purpose AI chatbots) على
  WhatsApp Business. لذلك Dealix هو **مساعد سير عمل أعمال** (خدمة / حجز / تسليم طلب)، وليس
  "ChatGPT داخل واتساب". كما أن WhatsApp Cloud API يتطلب **تكامل مزوّد (provider integration)** معتمد،
  وليس اتصالًا مباشرًا غير مُحوكَم.

---

## 1. شرط الدخول (Entry Condition)

لا يبدأ هذا التدفّق إلا عند توفّر **كل** ما يلي:

1. رد بريدي مُصنَّف `positive` في [`09`](09_REPLY_HANDLING_OS_AR.md).
2. طلب صريح من العميل للمتابعة عبر واتساب أو الحجز (لا نفترض القناة).
3. عدم وجود العميل في قائمة الكبح (`suppression`).
4. موافقة مُسجَّلة على فتح القناة (`consent_status`).

> إذا اختار العميل البقاء على البريد، تبقى المتابعة بريدية. واتساب خيار العميل، لا الافتراض.

---

## 2. تدفّق ما بعد الرد (Post-Reply Flow)

| # | المرحلة | البطاقة (Action Card) | البوابة |
|---|---|---|---|
| 1 | رد إيجابي على البريد | تأكيد التصنيف `positive` | تلقائي (تصنيف) |
| 2 | سؤال القناة | بطاقة: "واتساب أم حجز موعد؟" | موافقة المؤسس |
| 3 | مسح الجاهزية (Readiness Scan) | تحقّق: ألم واضح + مالك قرار + بيانات جاهزة | تلقائي (فحص) |
| 4 | بطاقة العرض (Proposal Card) | الدرجة المناسبة من السلّم الخماسي | موافقة المؤسس |
| 5 | حزمة الإثبات (Proof Pack) | نمط قطاعي آمن + أقسام الإثبات | موافقة المؤسس |
| 6 | تسليم الدفع (Payment Handoff) | رابط/خطوة دفع رسمية | موافقة المؤسس |

كل بطاقة تحمل: نص مُسوَّد، `send_status = "draft"`، `governance_decision`، ومستوى التخصيص.
لا تتحوّل أي بطاقة إلى رسالة صادرة قبل اعتماد المؤسس في `approval_center`.

---

## 3. مسح الجاهزية (Readiness Scan)

قبل بطاقة العرض، يُجري النظام فحصًا داخليًا (بلا رسالة خارجية) للتحقّق من نضج الفرصة:

- **ألم واضح:** هل عبّر العميل عن مشكلة محدّدة (leads متفرقة، متابعات ضائعة، فواتير متأخّرة)؟
- **مالك قرار:** هل المُحاوِر هو صاحب القرار أو قريب منه؟ (إن لا → مسار إحالة في [`09`](09_REPLY_HANDLING_OS_AR.md)).
- **بيانات جاهزة:** هل لدى العميل CRM/CSV قابل للمعالجة؟
- **قدرة دفع:** إشارة مبدئية تتسق مع الدرجة المقترحة.

نتيجة المسح تحدّد **أي درجة** من السلّم الخماسي تُقترح في بطاقة العرض — دون أي وعد بنتائج.

---

## 4. بطاقة العرض وحزمة الإثبات

- بطاقة العرض تستخدم السلّم الرسمي حصرًا (انظر [العمود الفقري §5](00_MARKET_PRODUCTION_OS_MASTER_AR.md)).
  ممنوع اختراع سعر أو باقة خارج السلّم.
- حزمة الإثبات تُرسِل نمطًا آمنًا (case-safe) وأقسام الإثبات. لا أسماء عملاء، لا أرقام غير مُتحقَّقة.
- لا ضمان مبيعات أو تحويل. الصياغة دائمًا "تقديري / نمط آمن".

---

## 5. تسليم الدفع (Payment Handoff)

- بطاقة الدفع تقدّم خطوة رسمية واحدة (رابط/طريقة معتمدة)، بموافقة المؤسس.
- لا خصم حيّ تلقائي، ولا معالجة دفع بلا موافقة صريحة من العميل ومن المؤسس.

---

## 6. إعادة الاستخدام (Reuse)

التدفّق يعيد استخدام الوحدات الموجودة، ولا يُنشئ روبوت دردشة عام:

- `auto_client_acquisition/whatsapp_decision_bot/` — منطق البطاقات والموجز والمعاينة:
  `command_parser.py`، `brief_builder.py`، `approval_preview.py`، `policy.py`، `renderer.py`.
- `auto_client_acquisition/channel_policy_gateway/whatsapp.py` — بوابة سياسة القناة (تمنع الصادر البارد/الجماعي).
- حالة الموافقة والقناة: `auto_client_acquisition/customer_inbox_v10/consent_status.py`.

> الطبقة الجديدة هنا = **سياسة تدفّق**، لا تكامل واتساب جديد. تكامل WhatsApp Cloud API عبر مزوّد معتمد
> يبقى شرطًا تشغيليًا منفصلًا، ولا يُفعَّل أي إرسال آلي عبره.

---

## 7. اللاءات المطبَّقة هنا

- لا واتساب بارد. لا واتساب جماعي. لا إرسال خارجي تلقائي. لا قوائم بث.
- لا فتح قناة بلا طلب العميل وموافقة مُسجَّلة. لا إرسال لعنوان مكبوح.
- لا روبوت دردشة عام على واتساب — مساعد سير عمل أعمال فقط، عبر تكامل مزوّد.
- كل بطاقة صادرة بموافقة المؤسس. الكبح يبقى فوريًا كما في [`09`](09_REPLY_HANDLING_OS_AR.md).

---

## EN summary

WhatsApp Post-Reply OS is component #15. WhatsApp is never a cold channel: the flow starts only after a
positive email reply (handled in `09_REPLY_HANDLING_OS_AR.md`) and only when the customer explicitly
asks to continue on WhatsApp or to book. The post-reply flow is a sequence of consent-gated action
cards: ask channel (WhatsApp or booking) → internal readiness scan (clear pain, decision owner, ready
data, payment ability) → proposal card (from the official five-tier ladder, never invented) → proof
pack (case-safe, no client names, no unverified numbers) → payment handoff (one official step, no live
auto-charge). Every card is drafted with `send_status = "draft"` and requires founder approval; nothing
is sent automatically. There is no cold WhatsApp, no bulk WhatsApp, no automated outbound, and no
broadcast lists. We note Meta's 2026 direction limiting general-purpose AI chatbots on WhatsApp
Business: Dealix is a business workflow assistant (service / booking / order handoff), not "ChatGPT
inside WhatsApp," and the WhatsApp Cloud API requires an approved provider integration. The flow reuses
`whatsapp_decision_bot/` and `channel_policy_gateway/whatsapp.py`; the new layer is flow policy, not a
new chatbot. Core rule holds: 250 drafts/day, 0 auto-sends.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
