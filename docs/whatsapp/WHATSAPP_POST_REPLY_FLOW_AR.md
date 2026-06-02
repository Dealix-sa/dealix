# تدفّق واتساب بعد الرد — WhatsApp Post-Reply Flow

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس (سامي)
**يبني على ولا يكرّر:** docs/outreach/REPLY_HANDLING_OS_AR.md (معالجة الردود) · docs/ops/reply_playbooks_ar.md (16 فئة رد) · docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md (حدود القناة)
**القوالب:** data/templates/whatsapp_templates_collection.md · data/templates/warm_intro_whatsapp_ar.md
**آخر تحديث:** 2026-06-02

---

## القاعدة الحاكمة (حرجة)

**واتساب ليس قناة باردة أبداً.** يُستخدم **فقط بعد ردّ إيجابي عبر البريد أو موافقة صريحة**. لا إرسال جماعي، لا أتمتة، لا blast. كل رسالة **1:1 وبموافقة المؤسس**. هذا التدفّق لا يبدأ إطلاقاً قبل وجود ردّ أو موافقة واردة.

## نقطة البداية (Entry Gate)

- **المُحفِّز الوحيد**: ردّ إيجابي على بريد (انظر فئات docs/ops/reply_playbooks_ar.md) **أو** موافقة صريحة من جهة الاتصال.
- بلا هذا المُحفِّز، **لا صفّ** في reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md ولا رسالة.

## التدفّق (بعد الرد فقط)

1. **عرض القناة**: بعد الرد الإيجابي، اعرض واتساب أو حجز موعد — العميل يختار. لا فرض.
2. **فحص الجاهزية**: أسئلة قصيرة 1:1 (المصادر، حجم العملاء، الأدوات الحالية، صانع القرار، التوقيت) — التفاصيل في docs/whatsapp/WHATSAPP_READINESS_SCAN_AR.md.
3. **بطاقة العرض (Proposal Card)**: بناءً على الفحص، تُجهَّز بطاقة عرض من السلّم المعتمد للموافقة قبل الإرسال (انظر docs/whatsapp/WHATSAPP_ACTION_CARDS_AR.md).
4. **حزمة الإثبات (Proof Pack)**: عند الطلب، تُرسَل حزمة إثبات مُجهَّلة الهوية كمرجع — لا أسماء عملاء بلا إذن.
5. **تسليم الدفع (Payment Handoff)**: فقط بعد قبول العرض كتابياً، يُرسَل رابط الدفع 1:1 بموافقة المؤسس.

## خريطة المراحل

| المرحلة | المُحفِّز | الفعل (بعد موافقة) |
|---------|----------|---------------------|
| عرض القناة | ردّ إيجابي/موافقة | اعرض واتساب أو حجز |
| فحص الجاهزية | اختار العميل واتساب | أرسل أسئلة الفحص القصيرة |
| بطاقة العرض | اكتمل الفحص | أرسل بطاقة عرض من السلّم |
| حزمة الإثبات | طلب العميل دليلاً | أرسل حزمة مُجهَّلة الهوية |
| تسليم الدفع | قبول كتابي للعرض | أرسل رابط الدفع 1:1 |

## السلّم المعتمد (لاختيار بطاقة العرض)

التشخيص المجاني (0) · Revenue Intelligence Sprint (499؛ premium 3,500–15,000) · Data-to-Revenue Pack (1,500) · Managed Revenue Ops (2,999–4,999/شهر) · Custom AI Setup (5,000–25,000) · Enterprise Governance Review (25,000–50,000).

## الحدود (غير قابلة للتفاوض)

- لا cold WhatsApp، لا أتمتة، لا إرسال جماعي/مجدول بلا مراجعة بشرية.
- الحد الأقصى للتوقيت: الأحد–الخميس 9ص–6م بتوقيت الرياض (يطابق data/templates/whatsapp_templates_collection.md).
- كل رسالة تُراجَع وتُعتمَد من المؤسس قبل الإرسال — لا استثناء.
- Dealix لا يرسل أي رسالة خارجية نيابةً عن العميل بدون موافقته الصريحة.
- لا «نضمن» نتائج؛ فرص مُثبتة بأدلة والنتائج تقديرية.

## الخطوة التالية

عند ورود ردّ إيجابي: صنّفه عبر docs/ops/reply_playbooks_ar.md، افتح صفّاً في reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md، وابدأ من «عرض القناة» باستخدام بطاقات docs/whatsapp/WHATSAPP_ACTION_CARDS_AR.md.

## English summary

WhatsApp is never a cold channel. This flow starts only after a positive email reply or explicit consent — without that inbound trigger there is no queue row and no message. The flow: offer WhatsApp or booking (customer chooses) → short 1:1 readiness scan (sources, lead volume, current tools, decision-maker, timeline) → an approval-gated proposal card drawn from the canonical ladder → an anonymized proof pack on request (no customer names without permission) → payment handoff only after written acceptance, sent 1:1 with founder approval. Every message is 1:1, founder-approved, within Riyadh business hours (Sun–Thu, 9am–6pm); no automation, no bulk, no blast, no scheduled sends without human review. Dealix never sends any external message on a customer's behalf without explicit consent. No guarantees — evidenced opportunities, estimated results. Builds on docs/outreach/REPLY_HANDLING_OS_AR.md, docs/ops/reply_playbooks_ar.md, and docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
