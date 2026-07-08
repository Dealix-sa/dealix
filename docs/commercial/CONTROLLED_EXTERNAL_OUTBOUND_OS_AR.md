# Controlled External Outbound OS

## الهدف

تجهيز الإرسال الخارجي بطريقة عملية وآمنة ومفيدة تجاريًا، بدون تحويل Dealix إلى أداة سبام أو أداة مخالفة.

النظام يسمح بتوليد قوائم ورسائل ومتابعات، لكنه لا يرسل إلا عبر مسار Live مضبوط وموافق عليه.

## لماذا لا نفتح الإرسال العشوائي؟

الإرسال العشوائي يسبب:

- حظر حسابات WhatsApp أو LinkedIn أو البريد.
- سمعة سيئة للبراند.
- مخاطرة قانونية وتنظيمية.
- ردود ضعيفة.
- ضياع الثقة قبل بناء المنتج.

## ما الذي يتم تلقائيًا؟

- اختيار الجمهور.
- ترتيب الأولويات.
- تصنيف القطاع والألم.
- مطابقة العرض.
- كتابة المسودة.
- تجهيز السكربت.
- تجهيز proof attachments.
- إنشاء approval queue.
- تسجيل النتيجة بعد الإرسال اليدوي أو الموافق عليه.

## ما الذي يحتاج موافقة؟

- إرسال Email.
- إرسال WhatsApp.
- إرسال LinkedIn DM.
- نشر LinkedIn post.
- اتصال هاتفي.
- إرسال عرض سعر.
- إرسال فاتورة.
- اعتبار الدفع مستلم.

## حالات الإرسال

```txt
draft_created
-> founder_review
-> approved
-> sent_manually_or_controlled_live
-> reply_received_or_no_reply
-> follow_up_drafted
-> payment_instruction_sent
-> payment_received
-> proof_pack_delivered
```

## القنوات

### Email

مسموح كمسودات، ولاحقًا controlled-live بشرط:

- مصدر العميل واضح.
- وجود سبب تواصل منطقي.
- وجود opt-out عند حملات أوسع.
- عدم استخدام claims كاذبة.

### WhatsApp

مسموح فقط في الحالات التالية:

- inbound.
- referral.
- عميل أعطى رقمه لغرض تجاري.
- سياق دافئ واضح.

ممنوع:

- cold WhatsApp lists.
- إرسال جماعي.
- قوائم مشتراة.

### LinkedIn

مسموح كمسودات ومتابعة يدوية.

ممنوع:

- mass automation.
- bypass limits.
- scraping DMs.

## Controlled-live sender لاحقًا

أي sender مباشر يجب أن يكون PR منفصل بعنوان مثل:

```txt
feat(outbound): add controlled-live email sender with approvals
```

ويجب أن يثبت:

- لا يرسل إلا `approved=true`.
- rate limit منخفض.
- opt-out موجود.
- logs موجودة.
- no secrets in code.
- no WhatsApp cold automation.
- kill switch موجود.
- dry-run default.

## القيمة التجارية

الإرسال ليس الهدف. الهدف هو أن يرى صاحب العمل:

- قائمة فرص مرتبة.
- رسائل جاهزة.
- أولويات واضحة.
- proof لكل خطوة.
- نتائج قابلة للقياس.

الاستهداف الذكي أهم من كثرة الرسائل.
