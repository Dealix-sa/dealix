# طابور موافقة المؤسس اليومي
# Founder Daily Approval Queue

**الجمهور:** المؤسس — قرارات يومية على المسوّدات والدُّفعات  
**المراجع التقنية:** `auto_client_acquisition/approval_center/` · `auto_client_acquisition/approval_center/schemas.py` · `auto_client_acquisition/approval_center/approval_policy.py`  
**الوثائق ذات الصلة:** [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) · [COLD_EMAIL_COMPLIANCE_AR.md](COLD_EMAIL_COMPLIANCE_AR.md) · [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md)  
**التقرير اليومي:** `reports/outreach/APPROVAL_QUEUE.md` (يُولَّد تلقائياً — غير موجود بعد)

---

## ١. دور المؤسس في مسار الإرسال

**لا يُرسَل أي بريد خارجي بدون موافقة المؤسس الصريحة.**

`channel_policy_gateway/email.py` يُعيد `allowed=False` لأي `send_live` بدون `human_approved=True`.  
`safe_send_gateway/middleware.py` يرفع `SendBlocked(reason_code="not_approved")` إذا غابت الموافقة.

الطابور هو نقطة التحكم الوحيدة بين توليد المسوّدة وإرسالها.

---

## ٢. ما يعرضه تقرير الطابور اليومي

يُولَّد التقرير في `reports/outreach/APPROVAL_QUEUE.md` ويُعرض على المؤسس كل صباح قبل ساعات الإرسال. يتضمّن:

| القسم | المحتوى |
|---|---|
| أفضل 50 مسوّدة اليوم | مُرتَّبة حسب ملاءمة ICP + درجة التخصيص + القطاع |
| المسوّدات عالية المخاطرة | `risk_level=high` — تتطلب مراجعة مكثّفة |
| أفضل القطاعات اليوم | القطاعات ذات أعلى درجة ملاءمة في القائمة الحالية |
| الدُّفعة المقترحة | `sending_batch` مُهيَّأ وجاهز للموافقة أو الرفض |
| تحذيرات إلغاء الاشتراك | إلغاءات الاشتراك الجديدة منذ آخر جلسة |
| تحذيرات الارتداد | ارتدادات جديدة تتجاوز عتبة التحذير |
| حالة صحة النطاق | `email_account.health_status` لكل نطاق إرسال نشط |

---

## ٣. قرارات المؤسس المتاحة

يُسجَّل كل قرار في سجل `approval_action`:

| القرار | ما يعنيه | ما يحدث بعده |
|---|---|---|
| `approve` | الموافقة على إرسال المسوّدة أو الدُّفعة كما هي | يُدرَج في طابور الإرسال خلال نافذة الوقت المحددة |
| `reject` | رفض — لا يُرسَل هذا المحتوى | يُحذف من القائمة + يُسجَّل السبب |
| `rewrite` | أعد الصياغة — احتفظ بالهدف وغيّر النص | يعود للتوليد مع تعليق المؤسس |
| `shorten` | قصّر الرسالة — اجعلها أكثر إيجازاً | نسخة مختصرة تُولَّد وتُعاد للطابور |
| `make_formal` | اجعلها أكثر رسمية في الأسلوب | تُعاد الصياغة بلغة أكثر احترافية |
| `change_offer` | غيّر العرض أو زاوية التقديم | تُعاد الصياغة مع عرض بديل |
| `move_to_nurture` | ليس الوقت المناسب — أضف لمسار المتابعة | يُحرَّك الاحتمال إلى تسلسل nurture بدون إرسال فوري |
| `do_not_contact` | لا تتواصل مع هذا الشخص/الشركة مرة أخرى | يُضاف فوراً إلى قائمة الاستثناء بـ `reason=do_not_contact` |

---

## ٤. سجل `approval_action`

كل قرار يُسجَّل بالحقول التالية:

```
approval_action {
  action_id      -- معرّف فريد للقرار
  target_type    -- draft | batch | proposal | payment_handoff
  decision       -- approve | reject | rewrite | shorten | make_formal | change_offer | move_nurture | do_not_contact
  reviewer       -- معرّف المراجع (المؤسس أو CSM)
  decided_at     -- طابع زمني ISO 8601
  notes          -- ملاحظات اختيارية للمراجع
}
```

الحقول في `ApprovalRequest` (من `approval_center/schemas.py`):

```
approval_id     -- معرّف الطلب (apr_<hex>)
object_type     -- نوع الكيان المُراجَع (draft | batch)
object_id       -- معرّف الكيان
action_type     -- draft_email | follow_up_task | ...
action_mode     -- approval_required | draft_only | approved_execute | blocked
channel         -- email
risk_level      -- low | medium | high | blocked
status          -- pending | approved | rejected | expired | blocked
```

---

## ٥. اتفاقية مستوى الخدمة — Approval SLA

| نوع الطلب | المهلة المستهدفة |
|---|---|
| دُفعة إرسال عادية (`risk_level=low`) | قبل نافذة الإرسال اليومية (08:00 - 20:00 بتوقيت الرياض) |
| مسوّدات عالية المخاطرة (`risk_level=high`) | مراجعة يدوية مكثّفة — لا إرسال تلقائي |
| طلب `do_not_contact` أو `move_to_nurture` | فوري — يُنفَّذ قبل أي إرسال لاحق |
| انتهاء صلاحية الطلب (expires_at) | الطلب المنتهي يتحوّل لـ `status=expired` — لا يُرسَل |

**سياسة انتهاء الصلاحية:** لا يُرسَل طلب منتهي الصلاحية. طلبات اليوم لا تُحمَل ليوم الغد بدون موافقة جديدة.

---

## ٦. منع تراكم الطابور

إذا تراكمت في الطابور أكثر من 100 مسوّدة في انتظار الموافقة:

- يُرسل تنبيه للمؤسس
- يتوقف توليد مسوّدات جديدة مؤقتاً
- يُعطى الأولوية للمسوّدات الأقل مخاطرة وأعلى ملاءمة ICP
- المسوّدات المنتهية الصلاحية تُحذف تلقائياً من الطابور

---

## ٧. المسوّدات عالية المخاطرة — High-Risk Drafts

تُحدَّد المسوّدة عالية المخاطرة بأي من:

- `risk_score > 50` في `compliance.py`
- موضوع الرسالة يُطابق نمط خادع (فحص regex)
- المستلم في نطاق شخصي (gmail, hotmail, ...) بدون موافقة مسبقة
- القطاع حساس (جهة حكومية، مستشفى، مدرسة)
- الرسالة تتضمّن أرقاماً تجارية قابلة للتحقق يجب أن تُراجَع

هذه المسوّدات لا تُدرَج في الدُّفعات التلقائية — تعرض في قسم منفصل في التقرير وتتطلب قراراً فردياً من المؤسس.

---

## EN Mirror — Founder Daily Approval Queue

**Audience:** Founder

### Role in the Sending Pipeline

No external email is sent without explicit founder approval. The approval center's `channel_policy_gateway/email.py` blocks any `send_live` without `human_approved=True`. The queue is the single control point between draft generation and sending.

### Daily Report Contents

The daily report (`reports/outreach/APPROVAL_QUEUE.md`) contains: top 50 ranked drafts, high-risk drafts for individual review, top-performing sectors today, a pre-configured suggested sending batch, new unsubscribe and bounce warnings, and current domain health status per sending account.

### Decision Options

The founder chooses from: approve, reject, rewrite, shorten, make_formal, change_offer, move_to_nurture, or do_not_contact. Each decision creates an `approval_action` record with `action_id`, `target_type`, `decision`, `reviewer`, `decided_at`, and optional `notes`.

### SLA

Normal batches must be approved before the daily sending window (08:00–20:00 Riyadh time). High-risk drafts require individual review — no auto-approval. Expired requests (past `expires_at`) are never sent. Requests do not carry over to the next day without fresh approval.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
