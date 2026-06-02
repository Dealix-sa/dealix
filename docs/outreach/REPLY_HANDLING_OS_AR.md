# نظام تشغيل معالجة الردود
# Reply Handling Operating System

**الجمهور:** المؤسس + مشغّل مسار الإرسال  
**المرجع التقني:** `auto_client_acquisition/email/reply_classifier.py`  
**الوثائق ذات الصلة:** [UNSUBSCRIBE_POLICY_AR.md](UNSUBSCRIBE_POLICY_AR.md) · [FOUNDER_APPROVAL_QUEUE_AR.md](FOUNDER_APPROVAL_QUEUE_AR.md) · [COLD_EMAIL_COMPLIANCE_AR.md](COLD_EMAIL_COMPLIANCE_AR.md)  
**تدفق WhatsApp بعد الرد:** `docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md` (غير موجود بعد — انظر الروابط غير المُحلَّلة)  
**التقرير اليومي:** `reports/outreach/REPLY_QUEUE.md` (يُولَّد تلقائياً — غير موجود بعد)

---

## ١. المبدأ الجوهري

كل رد يستحق إجراءً فورياً ومُوثَّقاً.  
الردود السلبية (إلغاء الاشتراك، الغضب) تُستثنى فوراً.  
الردود الإيجابية لا تُحوَّل لـ WhatsApp إلا بعد موافقة المستلم الصريحة على التواصل عبر WhatsApp.

---

## ٢. حقول `reply`

كل رد وارد يُسجَّل بالحقول:

```
reply {
  reply_id        -- معرّف فريد للرد
  prospect_ref    -- مرجع الاحتمال في CRM (بدون PII مباشر)
  category        -- التصنيف (انظر القسم 3)
  sentiment       -- positive | neutral | negative
  next_action     -- الإجراء التالي المُقترَح
  requires_founder -- هل يحتاج مراجعة مؤسس؟ (true/false)
  received_at     -- طابع زمني ISO 8601
}
```

---

## ٣. فئات التصنيف وخريطة الإجراءات

`reply_classifier.py` يُصنّف الردود إلى الفئات التالية مع الإجراء المُقابل:

| الفئة | الوصف | next_action | requires_founder | استثناء فوري؟ |
|---|---|---|---|---|
| `interested` | مستعد للبدء / طلب عرض | دعوة اكتشاف — Calendly | نعم | لا |
| `ask_price` | سؤال عن السعر أو التكلفة | إرسال بطاقة العرض + عرض مكالمة | نعم | لا |
| `ask_details` | يريد معرفة المزيد عن المنتج | إرسال proof pack + عرض demo | نعم | لا |
| `ask_demo` | طلب صريح لعرض توضيحي | رابط Calendly — 20 دقيقة | نعم | لا |
| `not_now` | مهتم لكن ليس الآن | جدولة متابعة بعد 30 يوماً | لا (آلي آمن) | لا |
| `wrong_person` | وصل للشخص الخطأ | طلب إحالة للشخص المناسب | نعم | لا |
| `unsubscribe` | STOP أو OPT OUT أو إيقاف | إضافة فورية لقائمة الاستثناء + رد إقرار | لا (آلي إلزامي) | **نعم — فوري** |
| `angry` | رد عدائي أو شكوى | اعتذار + استثناء فوري — لا رد تلقائي | نعم — إلزامي | **نعم — فوري** |
| `auto_reply` | رد غياب تلقائي (out-of-office) | لا إجراء — يُسجَّل فقط | لا | لا |
| `bounce` | ارتداد بريدي | استثناء العنوان فوراً (`reason=bounce`) | لا (آلي إلزامي) | **نعم — فوري** |
| `objection_budget` | الميزانية محدودة | إعادة تأطير عرض Pilot منخفض المخاطرة | نعم | لا |
| `objection_ai` | تحفّظ على الذكاء الاصطناعي | شرح نموذج التعاون البشري | نعم | لا |
| `objection_privacy` | قلق من PDPL أو الخصوصية | إرسال وثيقة الامتثال | نعم — إلزامي | لا |
| `unclear` | الرد غامض لا يمكن تصنيفه | مراجعة بشرية | نعم — إلزامي | لا |

---

## ٤. جدول الإجراءات التفصيلي

| الفئة | الرد الموصى به | القناة | آلي؟ |
|---|---|---|---|
| `interested` | رابط Calendly + تأكيد البيانات الأساسية | بريد إلكتروني → WhatsApp بعد موافقة | لا — موافقة مؤسس |
| `ask_price` | بطاقة العرض (Pilot 499 ريال + خطط الاشتراك) | بريد إلكتروني | لا — موافقة مؤسس |
| `ask_details` | proof pack مختصر + سؤال عن ديمو | بريد إلكتروني | لا — موافقة مؤسس |
| `ask_demo` | رابط Calendly 20 دقيقة | بريد إلكتروني | لا — موافقة مؤسس |
| `not_now` | رد مؤدّب + جدولة متابعة 30 يوماً | بريد إلكتروني | نعم (آمن — تأجيل بسيط) |
| `wrong_person` | طلب إحالة مؤدَّب للمسؤول المناسب | بريد إلكتروني | لا — موافقة مؤسس |
| `unsubscribe` | "تم إيقاف التواصل. لن أتواصل مرة ثانية." | بريد إلكتروني | نعم (إلزامي) |
| `angry` | "أعتذر بشدة على الإزعاج. تم حذف عنوانكم." | لا إرسال تلقائي — مؤسس يُرسل | لا |
| `auto_reply` | لا رد | — | يُسجَّل فقط |
| `bounce` | لا رد | — | استثناء آلي |
| `objection_privacy` | وثيقة الامتثال PDPL | بريد إلكتروني | لا — موافقة مؤسس |
| `unclear` | "هل ممكن توضيح الجانب الذي يهمكم أكثر؟" | بريد إلكتروني | لا — موافقة مؤسس |

---

## ٥. الردود الإيجابية والتحويل لـ WhatsApp

الردود في فئة `interested` أو `ask_demo` يمكن أن تُحوَّل لمتابعة عبر WhatsApp بشرطَين:

1. **موافقة صريحة من المستلم على التواصل عبر WhatsApp** — لا تُفترض الموافقة
2. **موافقة المؤسس على التحويل** — يُسجَّل في `approval_center`

**تسلسل التحويل الصحيح:**

```
رد إيجابي بالبريد الإلكتروني
    ↓
المؤسس يُقرّر في طابور الموافقة
    ↓
إرسال رابط الاجتماع (Calendly) بالبريد أولاً
    ↓
المستلم يُكمل الحجز أو يطلب صراحةً WhatsApp
    ↓
فقط بعد الموافقة الصريحة: التواصل عبر WhatsApp
```

للتفاصيل الكاملة عن مسار WhatsApp بعد الرد:  
`docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md` ← **غير موجود بعد**

---

## ٦. قواعد التصنيف في `reply_classifier.py`

`reply_classifier.py` يعمل بمسارَين:

**المسار السريع (regex):**
- `classify_rule_based(text)` — بدون تكلفة API
- نمط `unsubscribe` له أولوية 100 — يفوز دائماً عند التعارض
- نمط `angry` له أولوية 90 — ثاني أعلى أولوية
- الثقة (confidence): `min(0.9, 0.5 + 0.1 * عدد التطابقات)`

**المسار المحسَّن (LLM):**
- `classify_with_llm(text)` — يعمل إذا كان `GROQ_API_KEY` أو `ANTHROPIC_API_KEY` أو `OPENAI_API_KEY` موجوداً
- يُرجع `None` إذا لم يكن هناك مفتاح → يرجع لـ regex

**حالات المراجعة البشرية الإلزامية:**
- `category in {"angry", "objection_privacy", "unclear"}`
- `confidence < 0.5`
- `len(original_text) > 1000` — الردود الطويلة دائماً للمؤسس

---

## ٧. معالجة فئات الاستثناء الفوري

### `unsubscribe`

```
1. reply_classifier يُصنّف كـ unsubscribe (أولوية 100)
2. next_action = "add_to_suppression_immediately"
3. suppression record: {value=email, type=email, reason=unsubscribe}
4. رد إقرار آلي: "تم إيقاف التواصل. لن أتواصل مرة ثانية. شكراً لوقتكم."
   (auto_send_allowed=True للإقرار فقط)
5. تسجيل في audit log
```

للتفاصيل الكاملة: [UNSUBSCRIBE_POLICY_AR.md](UNSUBSCRIBE_POLICY_AR.md)

### `angry`

```
1. reply_classifier يُصنّف كـ angry (أولوية 90)
2. requires_human_review=True — لا رد تلقائي
3. يظهر في طابور المؤسس كأولوية قصوى
4. المؤسس يراجع ويُرسل اعتذاراً شخصياً
5. بعد إرسال الاعتذار: استثناء فوري من جميع القوائم
6. next_action = "human_review_immediate_then_suppress"
```

### `bounce`

```
1. الإرسال يُكشَف ارتداده من مزوّد البريد
2. compliance.py يضبط bounced_before=True لهذا العنوان
3. suppression record: {value=email, type=email, reason=bounce}
4. لا رد يُرسَل
5. إذا تجاوزت الارتدادات 5% في الدُّفعة → توقف فوري لجميع الدُّفعات
```

---

## ٨. تقرير قائمة الردود اليومية

يُولَّد يومياً في `reports/outreach/REPLY_QUEUE.md` ويتضمّن:

- عدد الردود الواردة اليوم مُصنَّفة حسب الفئة
- قائمة `interested` + `ask_demo` — أولوية متابعة قصوى
- قائمة `unsubscribe` + `bounce` + `angry` — تُعالَج أولاً
- متوسط وقت الرد على الفئات التي تتطلب موافقة
- الردود عالية الثقة (confidence > 0.8) مقابل المحتاجة مراجعة

---

## EN Mirror — Reply Handling Operating System

**Audience:** Founder and outbound pipeline operators  
**Technical reference:** `auto_client_acquisition/email/reply_classifier.py`

### Reply Record Fields

Each incoming reply is recorded with: `reply_id`, `prospect_ref`, `category`, `sentiment`, `next_action`, `requires_founder`, `received_at`.

### Classification Categories

The classifier recognizes: `interested`, `ask_price`, `ask_details`, `ask_demo`, `not_now`, `wrong_person`, `unsubscribe`, `angry`, `auto_reply`, `bounce`, `objection_budget`, `objection_ai`, `objection_privacy`, `unclear`.

### Immediate Suppression Actions

- `unsubscribe` → immediate suppression + auto acknowledgment ("تم إيقاف التواصل") — only case where `auto_send_allowed=True` applies without additional approval
- `angry` → no auto-reply; founder review required; suppress after personal apology is sent
- `bounce` → suppress email immediately; if batch bounce rate exceeds 5%, pause all subsequent batches

### Positive Reply to WhatsApp Routing

Interested replies (`interested`, `ask_demo`) can transition to WhatsApp follow-up only after: (1) explicit consent from the recipient to communicate via WhatsApp, and (2) founder approval on the transfer. WhatsApp outreach never initiates without documented consent. See `docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md` (unresolved — does not yet exist).

### Classifier Logic

Two-tier: fast regex path (zero API cost) with priority order — `unsubscribe=100`, `angry=90` — followed by optional LLM upgrade when an API key is present. Replies classified as `angry`, `objection_privacy`, `unclear`, with confidence below 0.5, or longer than 1,000 characters always require human review.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
