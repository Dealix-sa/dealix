# نظام معالجة الردود — Reply Handling OS

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس + عمليات الـ Outreach
**المخطط:** schemas/reply.schema.json
**آخر تحديث:** 2026-06-02

---

## الغرض

تصنيف كل رد وتحويله إلى **إجراء واحد واضح** بسرعة. الردود تغذّي حالة العميل المحتمل (docs/outreach/PROSPECT_RESEARCH_OS_AR.md) وقائمة الكبح (schemas/suppression.schema.json). الاستجابة للانسحاب والغضب **فورية**.

## فئات الردود والإجراءات

| الفئة (`category`) | الإجراء | تحديث الحالة |
|--------------------|---------|--------------|
| positive | دعوة اكتشاف/تشخيص (discovery invite) | `state = meeting_booked` عند تأكيد الموعد |
| interested_later | جدولة إعادة تواصل لاحقاً | `state = nurture` |
| price_question | إرسال بطاقة العرض من السلّم | يبقى في الحوار |
| send_more_info | إرسال حزمة إثبات آمنة (proof pack) | يبقى في الحوار |
| wrong_person | طلب إحالة للشخص الصحيح | تحديث `decision_maker_role` |
| not_interested | إغلاق مهذّب، لا متابعة | `state = lost` |
| unsubscribe | **كبح فوري** | `state = do_not_contact` |
| angry | **اعتذار + كبح فوري** | `state = do_not_contact` |
| auto_reply | لا إجراء بشري؛ إعادة جدولة بعد العودة | يبقى كما هو |
| bounce | **كبح البريد المرتدّ** | `send_status` يُعلَّم، يُحدّث الكبح |

كل رد يُسجَّل بـ `prospect_id`, `category`, `received_at`, `action_taken`.

## قواعد فورية (لا تأخير)

- **unsubscribe → كبح فوري.** لا رسالة وداع، لا «هل أنت متأكد». احترام الطلب لحظياً.
- **angry → اعتذار قصير + كبح فوري.** لا جدال، لا دفاع.
- **bounce → كبح عنوان البريد** لحماية صحة النطاق (docs/outreach/SENDING_RAMP_OS_AR.md).

أي تأخير في الكبح يخالف العقيدة وقد يضرّ النطاق والسمعة.

## مسارات الإجراء بالتفصيل

- **positive:** ردّ شخصي قصير + دعوة اكتشاف/تشخيص مجاني بخطوة واحدة. عند رغبة العميل بواتساب وموافقته الصريحة، يُحوَّل المسار إلى docs/whatsapp/ — **واتساب بعد رد/موافقة فقط، لا بارد مطلقاً**.
- **price_question:** بطاقة عرض من السلّم (التشخيص المجاني 0 · Sprint 499 · Data-to-Revenue Pack 1,500 · Managed Revenue Ops 2,999–4,999/شهر · Custom AI Setup 5,000–25,000 · Enterprise Governance Review 25,000–50,000). الأسعار حقيقة؛ النتائج تقديرية لا مضمونة.
- **send_more_info:** حزمة إثبات آمنة (أنماط افتراضية بلا أسماء عملاء، منهجية، نطاق). لا أرقام إيراد مخترعة.
- **wrong_person:** شكر + طلب إحالة مهذّب للشخص المسؤول؛ تحديث الدور في سجل العميل.
- **interested_later:** تثبيت موعد إعادة تواصل وتحويل إلى `nurture`؛ لا إلحاح.

## التحويل إلى واتساب (شرط الموافقة)

- يُسمح بواتساب **فقط** بعد رد إيجابي صريح وموافقة العميل على القناة.
- لا رسائل واتساب باردة. لا عروض غير مطلوبة. التفاصيل في docs/whatsapp/.

## مخرجات النظام

1. كل رد مصنّف ومحوّل لإجراء.
2. كبح فوري لـ unsubscribe/angry/bounce.
3. تحديث حالات العملاء المحتملين.
4. ردود positive مؤهَّلة لمسار الاجتماع/واتساب-بعد-الموافقة.
5. تقرير reports/outreach/REPLY_QUEUE.md معبّأ.

## روابط

- بحث العملاء والحالات: docs/outreach/PROSPECT_RESEARCH_OS_AR.md
- صف الموافقة: docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md
- الإرسال المرحلي والكبح: docs/outreach/SENDING_RAMP_OS_AR.md
- الانسحاب: docs/outreach/UNSUBSCRIBE_POLICY_AR.md
- واتساب بعد الموافقة: docs/whatsapp/

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
