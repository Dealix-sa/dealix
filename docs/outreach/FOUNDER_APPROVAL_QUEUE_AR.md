# صف موافقة المؤسس — Founder Approval Queue

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس
**المخطط:** schemas/approval_action.schema.json
**آخر تحديث:** 2026-06-02

---

## لماذا الصف موجود

**لا إرسال بدون موافقة المؤسس.** المصنع يُنتج 250 مسودة/يوم (docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md)، لكن الإنسان يقرّر ما يُرسَل. الصف يركّز قرار المؤسس على أعلى المسودات قيمة وأعلاها مخاطرة في دقائق، لا ساعات.

## قرارات المؤسس اليومية

لكل مسودة، إجراء واحد يُسجَّل في `action`:

| الإجراء | المعنى | الأثر على الحالة |
|---------|--------|------------------|
| approve | اعتماد للإرسال المرحلي | `approval_status = approved` |
| reject | رفض نهائي لهذه المسودة | `approval_status = rejected` |
| rewrite | يحتاج إعادة صياغة | يعود للمصنع |
| shorten | اختصار الجسم | يعود للمصنع مع ملاحظة |
| make more formal | رفع الرسمية | يعود للمصنع مع ملاحظة |
| change offer | تغيير العرض من السلّم | يعود للمصنع مع العرض البديل |
| move to nurture | غير جاهز الآن | `state = nurture` |
| do_not_contact | استبعاد دائم | `state = do_not_contact` + كبح |

كل إجراء يحمل `prospect_id` و`draft_id` و`reason` اختيارياً، و`actor` (المؤسس) و`timestamp`.

## ماذا يعرض تقرير الموافقة

التقرير اليومي (reports/outreach/APPROVAL_QUEUE.md) يعرض:

- **أفضل 50 مسودة اليوم** — مرتّبة بدرجة العميل × جودة التخصيص، مع العرض المقترح.
- **المسودات عالية المخاطر** — كل ما `risk_level = high` أو `compliance_status = fail`، للمراجعة أو الرفض.
- **أفضل القطاعات اليوم** — القطاعات الأعلى ملاءمة وتجاوباً متوقعاً.
- **دفعة الإرسال المقترحة** — حجم مبدئي يحترم خطة التدرّج (docs/outreach/SENDING_RAMP_OS_AR.md).
- **تحذيرات الانسحاب/الارتداد** — أي ارتفاع في opt-out أو bounce يوقف التوسّع.

## مبادئ القرار

- **عند الشك، لا ترسل.** الرفض أرخص من ضرر السمعة.
- أي مسودة دون P1 أو بلا انسحاب لا تظهر أصلاً — تُحجب في المصنع.
- لا تعتمد دفعة تتجاوز سقف اليوم في خطة التدرّج مهما كانت الجودة.
- `do_not_contact` يُزامَن فوراً مع قائمة الكبح (schemas/suppression.schema.json).
- الموافقة لا تعني إرسالاً فورياً — تعني الأهلية للدخول في الدفعة المرحلية.

## مخرجات الصف

1. مجموعة `approved` جاهزة للنظام المرحلي (بحجم لا يتجاوز سقف اليوم).
2. ملاحظات `rewrite/shorten/...` عائدة للمصنع.
3. تحديث الكبح من `do_not_contact`.
4. تقرير reports/outreach/APPROVAL_QUEUE.md معبّأ.

## حدود لا تُتجاوز

- لا «approve all» بضغطة واحدة دون مراجعة عالية المخاطر.
- لا اعتماد مسودة بموضوع مضلِّل أو `Re:`/`Fwd:` زائف.
- لا اعتماد رسالة واتساب باردة (واتساب بعد رد/موافقة فقط).
- لا تجاوز لطلب توقّف سابق.

## روابط

- المصنع: docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md
- الإرسال المرحلي: docs/outreach/SENDING_RAMP_OS_AR.md
- معالجة الردود: docs/outreach/REPLY_HANDLING_OS_AR.md
- الامتثال: docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
