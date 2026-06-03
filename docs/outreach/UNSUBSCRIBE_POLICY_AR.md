# Unsubscribe & Suppression Policy — سياسة الإلغاء والكبح

جزء من: Dealix Market Production OS — انظر [docs/market_os/MARKET_PRODUCTION_OS_AR.md](../market_os/MARKET_PRODUCTION_OS_AR.md)

> القاعدة: من طلب التوقّف يتوقّف فورًا — احترام opt-out أصل ثقة، وليس خيارًا.

المخطط المرتبط: [`schemas/suppression.schema.json`](../../schemas/suppression.schema.json)

---

## 1. كل رسالة فيها مخرج

- one-click unsubscribe (RFC 8058) في كل رسالة تسويقية — حقل `email_account.one_click_unsubscribe`.
- رابط/رأس إلغاء واضح، لا خطوات مخفية، لا تسجيل دخول مطلوب.
- التذييل يحوي هوية مرسِل وعنوانًا صحيحًا.

---

## 2. عند ورود طلب إلغاء أو إشارة سلبية

| الإشارة | الإجراء | السرعة |
|---|---|---|
| unsubscribe | أضِف إلى suppression، أوقف كل تسلسلات | فورًا |
| angry / شكوى | اعتذار قصير + suppression | فورًا |
| bounce (hard) | كبح العنوان/النطاق | فورًا |
| not_interested | nurture أو كبح حسب النبرة | نفس اليوم |

نظام CAN-SPAM يمنح حدًّا أقصى 10 أيام عمل لاحترام opt-out؛ سياستنا: **فورًا**.

---

## 3. قائمة الكبح (Suppression List)

- مصدر الحقيقة الوحيد لمن لا يُتواصَل معهم.
- تُفحَص قبل **كل** دفعة إرسال (`sending_batch`) — أي مطابقة توقف إدراج المستلم.
- القائمة الحيّة بيانات runtime مكبوتة في git (`data/prospects/`)؛ لا تُرفع عناوين حقيقية.
- يُفضّل تخزين `email_sha256` بدل العنوان الخام (حقل في المخطط).
- لا حذف من القائمة إلا بطلب صريح موثّق من صاحب العنوان.

---

## 4. التحقق

- الاختبار `tests/test_market_production_os.py` يتأكد أن أمثلة الـ drafts فيها `unsubscribe_included = true`
  وأن آلية الكبح موصوفة وموجودة في المخطط.

انظر أيضًا: [COLD_EMAIL_COMPLIANCE_AR](COLD_EMAIL_COMPLIANCE_AR.md) · [REPLY_HANDLING_OS_AR](REPLY_HANDLING_OS_AR.md).

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
