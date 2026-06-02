# تدفق واتساب ما بعد الردّ — WhatsApp Post-Reply Flow
## واتساب قناة علاقة قائمة فقط — لا بارد، لا أتمتة، لا إرسال دون موافقة

**حدود واتساب:** [`docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md`](../02_saudi_positioning/WHATSAPP_BOUNDARY.md)
**سياسة القناة:** `auto_client_acquisition/channel_policy_gateway/whatsapp.py`
**بوت القرار:** `auto_client_acquisition/whatsapp_decision_bot/` (policy.py · approval_preview.py · brief_builder.py · renderer.py · command_parser.py)
**قائمة انتظار ما بعد الردّ:** [`reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md`](../../reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md)
**بطاقات الإجراءات:** [`docs/whatsapp/WHATSAPP_ACTION_CARDS_AR.md`](./WHATSAPP_ACTION_CARDS_AR.md)
**مسح الجاهزية:** [`docs/whatsapp/WHATSAPP_READINESS_SCAN_AR.md`](./WHATSAPP_READINESS_SCAN_AR.md)

---

## الحدود المطلقة — اقرأها أولاً

**واتساب في Dealix ليس قناة تواصل بارد بأي صورة.**
**كل رسالة هي مسوّدة تحت موافقة المؤسس — لا إرسال تلقائي مطلقاً.**

هذا ليس اختياراً تشغيلياً — هو قيد مُدمَج في `channel_policy_gateway/whatsapp.py`:

- `is_cold = True` → محجوب تلقائياً.
- `is_blast = True` → محجوب تلقائياً.
- `human_approved = False` → محجوب تلقائياً.
- `can_ever_live_send()` في `policy.py` يُعيد `False` دائماً.

أي مسوّدة تُنتجها أدوات Dealix يجب أن يُوافق عليها المؤسس يدوياً قبل الإرسال الفعلي.

---

## 1 — شرط الانطلاق: ردّ إيجابي واضح

واتساب لا يُفتح إلا بعد:

1. **ردّ إيجابي صريح** على بريد إلكتروني أو رسالة مباشرة — ليس مجرد فتح الرسالة.
2. **أو موافقة صريحة** في اجتماع أو عبر نموذج تسجيل رسمي.

الردّ الإيجابي يُسجَّل بـ `consent_record_exists = True` في سياسة القناة. بدون هذا السجل، السياسة ترفض كل طلب إرسال.

---

## 2 — التدفق الكامل (6 مراحل)

```
ردّ إيجابي على الإيميل
        ↓
   [مرحلة 1] عرض واتساب أو حجز موعد
        ↓
   [مرحلة 2] مسح الجاهزية
        ↓
   [مرحلة 3] بطاقة المقترح
        ↓
   [مرحلة 4] حزمة الإثبات
        ↓
   [مرحلة 5] تسليم الدفع
        ↓
   [مرحلة 6] إغلاق مهذّب أو انتقال للتنفيذ
```

---

### المرحلة 1 — عرض قناة التواصل

**المُشغِّل:** ردّ إيجابي وارد على البريد الإلكتروني.

**الفعل:** المؤسس يُقرّر: هل تُعرض قناة واتساب؟ أم حجز موعد مباشر؟

إذا كان العميل سعودياً وردّه يوحي بتفضيل واتساب، يُعرَض خيار الانتقال إليه.
هذا العرض نفسه يتمّ عبر الردّ على الإيميل — لا عبر رسالة واتساب ابتدائية.

**البطاقة المرجعية:** `intro_after_reply` في [`WHATSAPP_ACTION_CARDS_AR.md`](./WHATSAPP_ACTION_CARDS_AR.md).

**شرط الإرسال:**
- `consent_record_exists = True`
- موافقة المؤسس على المسوّدة

---

### المرحلة 2 — مسح الجاهزية (Readiness Scan)

**المُشغِّل:** العميل يوافق على المتابعة عبر واتساب أو في اجتماع.

**الفعل:** المؤسس يطرح أسئلة مسح الجاهزية المُحدَّدة في [`WHATSAPP_READINESS_SCAN_AR.md`](./WHATSAPP_READINESS_SCAN_AR.md).

المسح يُحدّد:
- جاهزية البيانات.
- حضور مالك القرار.
- نطاق الميزانية.
- الجدول الزمني.
- قبول الحوكمة.

نتيجة المسح تُوجّه لمنتج محدد في الكتالوج أو تُوقف المسار إذا كانت المعايير غير مكتملة.

---

### المرحلة 3 — بطاقة المقترح

**المُشغِّل:** مسح الجاهزية يُسفر عن درجة مؤهَّلة (راجع WHATSAPP_READINESS_SCAN_AR.md).

**الفعل:** `approval_preview.preview_action()` يبني مسوّدة بطاقة المقترح. المؤسس يُراجعها ويُعدّلها ويُوافق عليها ثم يُرسلها يدوياً.

البطاقة تتضمّن:
- اسم المنتج (السبرنت أو الاشتراك الشهري).
- النطاق والمخرجات.
- السعر.
- الخطوة التالية (كيفية البدء).

**البطاقة المرجعية:** `send_proposal_card` في WHATSAPP_ACTION_CARDS_AR.md.

---

### المرحلة 4 — حزمة الإثبات

**المُشغِّل:** العميل يسأل عن أدلة أو نتائج سابقة مشابهة.

**الفعل:** المؤسس يُرسل حزمة إثبات آمنة — نتائج مُجمَّعة وغير منسوبة لعميل محدد، أو حالة دراسية مُصنَّفة صراحةً كـ "نمط آمن افتراضي".

لا تُشارَك بيانات عميل حقيقي محدد دون إذن صريح منه.

**البطاقة المرجعية:** `send_proof_pack` في WHATSAPP_ACTION_CARDS_AR.md.

---

### المرحلة 5 — تسليم الدفع

**المُشغِّل:** العميل مستعد للمضي قُدُماً.

**الفعل:** المؤسس يُرسل رابط الدفع أو رقم الفاتورة عبر رسالة واتساب مُعتمَدة.

**البطاقة المرجعية:** `payment_handoff` في WHATSAPP_ACTION_CARDS_AR.md.

---

### المرحلة 6 — الإغلاق المهذّب أو الانتقال للتنفيذ

**إذا تمّت الصفقة:** الانتقال لكتاب تشغيل السبرنت [`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md).

**إذا توقّف العميل:** بطاقة الإغلاق المهذّب (`polite_close`) — رسالة واحدة فقط، لا متابعة متكررة.

---

## 3 — كيف يتكامل نظام قرار واتساب (WhatsApp Decision Bot)

`command_parser.py` يُحلّل أوامر المؤسس الداخلية (بالعربية السعودية) ويُعيد intent ومستوى العمل:

| نوع الأمر | نمط العمل |
|---|---|
| "وش الوضع اليوم؟" | `preview_only` — ملخّص داخلي للمؤسس فقط |
| "جهز ردّ للعميل" | `draft_only` — مسوّدة تنتظر الموافقة |
| "اعتمد الردّ" | `approval_required` — يستلزم خطوة موافقة صريحة |

لا أمر يُنتج إرسالاً حياً. `can_ever_live_send()` يُعيد `False` دائماً.

`brief_builder.py` يبني ملخّص اليوم الداخلي (القرارات المعلّقة، تجاوزات SLA) — هذا للاستخدام الداخلي للمؤسس، لا يُرسَل للعميل.

---

## 4 — قائمة مراجعة الامتثال (لكل رسالة)

قبل إرسال أي رسالة واتساب للعميل، تحقّق:

- [ ] `consent_record_exists = True` — هل يوجد ردّ إيجابي موثَّق؟
- [ ] `approved_template_or_24h_window = True` — هل الرسالة ضمن نافذة 24 ساعة أو قالب معتمَد؟
- [ ] `human_approved = True` — هل وافق المؤسس يدوياً؟
- [ ] الرسالة ليست بارداً (`is_cold = False`).
- [ ] الرسالة ليست جماعية (`is_blast = False`).
- [ ] لا PII (لا أرقام هوية، لا بريد إلكتروني لأشخاص آخرين في الرسالة).

---

## English Mirror — WhatsApp Post-Reply Flow

**Hard boundary:** WhatsApp is used ONLY after a positive inbound reply or explicit consent. Every outbound message is a draft under founder approval. No live send is ever automated. `channel_policy_gateway/whatsapp.py` hard-codes `can_ever_live_send() = False`.

**Six-stage flow:**
1. Positive email reply → offer WhatsApp or booking link.
2. Readiness scan (data, owner, budget, timeline, governance).
3. Proposal card (founder-approved draft → manual send).
4. Proof pack (aggregated, non-attributed evidence).
5. Payment handoff (invoice or payment link).
6. Polite close or transition to sprint delivery.

**WhatsApp Decision Bot (internal):** the `command_parser` processes founder Arabic commands into `preview_only`, `draft_only`, or `approval_required` actions. No command ever produces a live customer send. The internal brief from `brief_builder` is for the founder only — never forwarded to clients.

**Pre-send compliance check:** consent record exists + 24h window or approved template + founder manual approval + not cold + not blast + no PII.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
