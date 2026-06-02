# نظام الإرسال المرحلي (عمليات) — Sending Ramp OS

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس + عمليات الـ Outreach
**المخطط:** schemas/sending_batch.schema.json
**سياسة التسليم (مرجع):** docs/outreach/SENDING_RAMP_PLAN_AR.md
**آخر تحديث:** 2026-06-02

---

## نطاق هذا المستند

هذا **مستند العمليات اليومية** لتنفيذ الإرسال المرحلي: كيف تُبنى الدفعة وتُجدوَل وتُنفَّذ. **سياسة** التدرّج وأرقام السقوف وصحة النطاق مُعرّفة في docs/outreach/SENDING_RAMP_PLAN_AR.md — لا نكرّرها هنا، بل نلتزم بها.

## العقيدة

**250 مسودة/يوم هدف إنتاج — وليست هدف إرسال.** الإرسال يتدرّج ببطء من أرقام صغيرة ويرتفع فقط بعد سجل صحة نطاق نظيف، وانسحاب يعمل، وقائمة كبح محدّثة، وموافقة المؤسس. لا قوائم مشتراة. لا إرسال جماعي دفعة واحدة.

## حقول الدفعة (مرجع المخطط)

```
batch_id, batch_size, account, domain, sector, sequence_step,
risk_level, approved_at, send_window, status
```

- `batch_size`: ضمن سقف اليوم في خطة التدرّج (docs/outreach/SENDING_RAMP_PLAN_AR.md).
- `account` / `domain`: حساب ونطاق مُهيّأ ومُتحقَّق (انظر schemas/email_account.schema.json).
- `sequence_step`: first-touch / follow-up-1 / follow-up-2 / proposal-intro / breakup.
- `send_window`: نافذة زمنية في ساعات عمل KSA، موزّعة لا دفعة لحظية.
- `approved_at`: ختم موافقة المؤسس — بلا قيمة لا إرسال.

## شروط الإرسال (Pre-flight) — لا تُرسل دفعة إذا

- **لا انسحاب:** أي رسالة بلا `unsubscribe_included = true`.
- **لا موافقة:** `approved_at` فارغ أو `approval_status ≠ approved`.
- **لا تخصيص:** أي مسودة دون P1 (docs/outreach/PERSONALIZATION_RULES_AR.md).
- **مستلم مكبوح:** تطابق مع قائمة الكبح (schemas/suppression.schema.json).
- **نطاق غير صحي:** مؤشرات صحة النطاق دون الحد في خطة التسليم.
- **قفزة ارتداد:** ارتفاع bounce/complaint فوق العتبة — يوقف الإرسال فوراً.

أي شرط يفشل يوقف الدفعة بالكامل، لا الرسالة وحدها.

## سير العمل اليومي

1. **استلام المعتمَد:** أخذ مجموعة `approved` من صف المؤسس (docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md).
2. **تكوين الدفعات:** تقسيم حسب `account`/`domain`/`sector`/`sequence_step` بأحجام ضمن سقف اليوم.
3. **فحص Pre-flight:** تطبيق كل شروط الإرسال أعلاه على كل دفعة.
4. **الجدولة:** توزيع `send_window` على ساعات العمل، لا إرسال لحظي مكثّف.
5. **التنفيذ والمراقبة:** متابعة الارتداد/الشكاوى/الانسحاب لحظياً؛ أي قفزة توقف التوسّع.
6. **التقرير:** تعبئة reports/outreach/SENDING_BATCH_PLAN.md.

## التصعيد والإيقاف

- قفزة ارتداد أو شكوى → إيقاف فوري + إبلاغ المؤسس + مراجعة خطة التسليم.
- انسحاب لا يعمل → إيقاف كل الإرسال حتى الإصلاح.
- نطاق غير صحي → تجميد الحساب المعني، تحويل لخطة التسليم.

## ما هذا النظام ليس مسؤولاً عنه

- لا يحدّد سياسة الأرقام/الإحماء — تلك في docs/outreach/SENDING_RAMP_PLAN_AR.md.
- لا يرسل واتساب — واتساب بعد رد/موافقة فقط (docs/whatsapp/).
- لا يتجاوز موافقة المؤسس مهما كانت الأولوية.

## روابط

- سياسة التدرّج والتسليم: docs/outreach/SENDING_RAMP_PLAN_AR.md
- صحة النطاق والتسليم: docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md
- الانسحاب: docs/outreach/UNSUBSCRIBE_POLICY_AR.md
- صف الموافقة: docs/outreach/FOUNDER_APPROVAL_QUEUE_AR.md
- معالجة الردود: docs/outreach/REPLY_HANDLING_OS_AR.md

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
