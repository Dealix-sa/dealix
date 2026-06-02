# بطاقات أفعال واتساب — WhatsApp Action Cards

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس (سامي)
**جزء من التدفّق:** docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md
**مجموعة القوالب الكاملة:** data/templates/whatsapp_templates_collection.md · data/templates/warm_intro_whatsapp_ar.md — هذه البطاقات تربط كل مرحلة بقالبها، ولا تكرّر القوالب.
**آخر تحديث:** 2026-06-02

---

## القاعدة الحاكمة

كل بطاقة هنا **1:1 وبموافقة المؤسس قبل الإرسال**. لا إرسال جماعي، لا أتمتة، لا جدولة بلا مراجعة. تُستخدم **فقط بعد ردّ إيجابي أو موافقة** (انظر التدفّق). الوسم في كل قالب: `NO_LIVE_SEND` حتى الموافقة.

## البطاقات الخمس

### 1) مقدّمة ما بعد الرد (Post-Reply Intro)

**متى**: مباشرة بعد ردّ إيجابي على البريد.

```
{{ name }} — شكراً على ردّك.

نكمل هنا على واتساب أو تفضّل نحجز 20 دقيقة؟ أيّهما يناسبك.

— {{ founder_name }} | Dealix
```

**[حوكمة: موافقة المؤسس قبل الإرسال — NO_LIVE_SEND]**

### 2) إرسال العرض (Send Proposal Card)

**متى**: بعد فحص الجاهزية واختيار العرض من السلّم.

```
{{ name }} — بناءً على ما ذكرت، أنسب بداية لكم: {{ offer_name }}.

النطاق باختصار: {{ scope_line }}
السعر: {{ price }} — الصلاحية: 14 يوماً.

أرسل لك التفاصيل الكاملة الآن؟

— {{ founder_name }} | Dealix
```

**[حوكمة: موافقة المؤسس قبل الإرسال — NO_LIVE_SEND]**

### 3) إرسال حزمة الإثبات (Send Proof Pack)

**متى**: عند طلب العميل دليلاً. الحزمة **مُجهَّلة الهوية** — لا أسماء عملاء بلا إذن.

```
{{ name }} — أرفقت تقريراً نموذجياً مُجهَّل الهوية يوضّح مخرجات السبرنت (14 قسماً، درجة جودة، حسابات مُرتَّبة بمبرّرات).

مرجع لا التزام. تحبّ أمشي معك في أي قسم؟

— {{ founder_name }} | Dealix
```

**[حوكمة: موافقة المؤسس قبل الإرسال — NO_LIVE_SEND]**

### 4) رابط الحجز (Booking Link)

**متى**: عندما يفضّل العميل مكالمة بدل المتابعة الكتابية.

```
{{ name }} — تفضّل نختار وقت يناسبك:

{{ booking_link }}

20 دقيقة تكفي نمشي على بياناتكم تحديداً.

— {{ founder_name }}
```

**[حوكمة: موافقة المؤسس قبل الإرسال — NO_LIVE_SEND]**

### 5) تسليم الدفع (Payment Handoff)

**متى**: **فقط** بعد قبول العرض كتابياً.

```
{{ name }} — تأكيد قبولكم للعرض. رابط الدفعة الأولى:

{{ payment_link }}

بعد الدفع أؤكّد موعد جلسة الانطلاق خلال ساعتين.
رقم المشروع: {{ engagement_id }}

— {{ founder_name }} | Dealix
```

**[حوكمة: موافقة المؤسس قبل الإرسال — NO_LIVE_SEND]**

## المتغيرات

| المتغير | المعنى |
|---------|--------|
| `{{ name }}` | الاسم الأول للمستلم |
| `{{ founder_name }}` | اسم المؤسس |
| `{{ offer_name }}` | اسم العرض من السلّم |
| `{{ scope_line }}` | سطر نطاق مختصر |
| `{{ price }}` | السعر من السلّم المعتمد |
| `{{ booking_link }}` | رابط الحجز |
| `{{ payment_link }}` | رابط الدفع الميسَّر |
| `{{ engagement_id }}` | رقم المشروع |

> القوالب الكاملة (متابعات، تحديثات يومية، عروض الاحتفاظ) في data/templates/whatsapp_templates_collection.md.

## الحدود

- الحد الأقصى: الأحد–الخميس 9ص–6م الرياض. لا مساء ولا عطلة.
- لا «نضمن» نتائج؛ فرص مُثبتة بأدلة والنتائج تقديرية.
- لا رابط دفع قبل قبول كتابي. لا حزمة إثبات بأسماء عملاء بلا إذن.

## الخطوة التالية

اختر البطاقة حسب مرحلة الصفّ في reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md، املأ المتغيرات، واعرضها على المؤسس للموافقة قبل الإرسال.

## English summary

Five approval-gated 1:1 action cards, each tied to a stage of docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md and used only after a positive reply or consent: post-reply intro (offer WhatsApp or a booking), send proposal card (the selected ladder offer with scope, price, 14-day validity), send proof pack (anonymized, no customer names without permission), booking link, and payment handoff (only after written acceptance). Every card carries the `NO_LIVE_SEND` tag and requires founder approval before sending — no bulk, no automation, no scheduling without human review, within Riyadh business hours (Sun–Thu, 9am–6pm). No payment link before written acceptance; no proof pack with customer names without permission; no guarantees — evidenced opportunities, estimated results. The full template set (follow-ups, daily updates, retainer upsells) lives in data/templates/whatsapp_templates_collection.md; these cards map stages to templates rather than duplicating them.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
