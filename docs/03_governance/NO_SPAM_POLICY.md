# No-Spam Policy — سياسة منع الإزعاج

> طبقة: Governance OS · غير قابلة للتفاوض

## المبدأ

> هدف Targeting OS ليس إرسال 400 رسالة. هدفه أن يعرف من يستحق 5 رسائل فقط
> اليوم — ولماذا.

نبحث 400، ونرسل 3–5 يدويًا فقط بعد مراجعة. هذا يحمي سمعة Dealix ويجعله شركة
**Intelligence محترمة، لا spam machine**.

## ممنوع منعًا باتًا

- mass email / mass WhatsApp / cold WhatsApp automation
- LinkedIn automation أو DM آلي
- أرقام جوالات شخصية
- قوائم PII مشتراة أو مسربة
- scraping خلف login أو تجاوز CAPTCHA
- وعود مبيعات أو ضمانات أو ادعاءات مبالغ فيها

## حدود الإرسال اليومية (سقوف صلبة)

| المرحلة | السقف اليومي |
|---|---|
| Raw research candidates | 300–400 |
| Manual sends | **3–5 كحد أقصى** |

أي إرسال يجب أن يكون: يدوي · بموافقة المؤسس · مع opt-out محترم · مربوط بدليل.

## ما يفرضه الكود

- لا توجد قناة إرسال في أي script ضمن Targeting OS.
- `validate_draft()` يرفض عبارات الضمان/الضغط.
- `blocked_sources.yml` يمنع mass_whatsapp / mass_email_list / personal_mobile_number.

## روابط

- [Outreach Approval Policy](OUTREACH_APPROVAL_POLICY.md)
- دستور: [docs/00_constitution/WHAT_DEALIX_REFUSES.md](../00_constitution/WHAT_DEALIX_REFUSES.md)
