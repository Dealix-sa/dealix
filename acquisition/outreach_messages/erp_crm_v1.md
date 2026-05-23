# Outreach Message Library — ERP / CRM Vendors

Each message is referenced by `suggested_message_id` in the batch CSV.

## erp_crm_v1_en — First touch (English)

```
Hi {first_name_or_team},

I'm Sami, building Dealix for Saudi B2B revenue operations.

I noticed {company} works in ERP/CRM implementation and business software.
I'm testing a small Revenue Sprint format: a short list of qualified B2B
opportunity targets, why they fit, and suggested outreach angles your team
can use.

No big pitch — I can send a small sample first so you can judge if it's
useful.

Would it be helpful if I send a sample for your team?

— Sami
Dealix
```

## erp_crm_v1_ar — First touch (Arabic)

```
أهلًا {الفريق_أو_الاسم_الأول}،

أنا سامي أبني Dealix لمساعدة شركات B2B في السعودية على تنظيم فرص المبيعات
بشكل أوضح.

لاحظت أن {الشركة} تعمل في ERP/CRM أو حلول الأعمال. أختبر حاليًا صيغة بسيطة
اسمها Revenue Sprint: قائمة مختصرة بفرص B2B مؤهلة، سبب ملاءمتها، وزوايا
تواصل ممكن يستخدمها الفريق.

بدون عرض طويل — أقدر أرسل عينة صغيرة أولًا وتشوفون هل هي مفيدة.

هل يناسب أرسل لكم sample بسيط للفريق؟

— سامي
Dealix
```

## erp_crm_v1_followup_en — Follow-up (English, day +4)

```
Hi {first_name_or_team},

Just following up on this.

The sample would be simple: a few qualified B2B opportunity targets for
your ERP/CRM business, with why each target fits and a suggested outreach
angle.

If it's useful, we can discuss a focused Revenue Sprint. If not, no
problem — happy to step away.

— Sami
Dealix
```

## erp_crm_v1_followup_ar — Follow-up (Arabic, day +4)

```
أهلًا {الفريق_أو_الاسم_الأول}،

أتابع رسالتي السابقة.

العينة بسيطة: عدد قليل من فرص B2B المؤهلة لشركة ERP/CRM زيكم، مع سبب ملاءمة
كل فرصة وزاوية تواصل مقترحة.

لو كانت مفيدة نقدر نناقش Revenue Sprint مركّز. لو غير مناسبة، لا مشكلة
أبدًا.

— سامي
Dealix
```

## Copy Rules (enforced by `tests/acquisition/test_erp_crm_batch.py`)
- No "guarantee" / "guaranteed" anywhere.
- No revenue / ROI claims with numbers.
- No "promised" replies, meetings, or sales.
- One CTA per message.
- Personalization tokens (`{company}`, `{first_name_or_team}`) must remain
  visible in the library; the founder fills them per send.
