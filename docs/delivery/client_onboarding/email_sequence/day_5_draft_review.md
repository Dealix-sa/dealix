# Day 5 — Drafts for review (bilingual)

> Draft template — never auto-sent. Founder approves.

**Merge fields:** `{{customer_name}}`, `{{sprint_id}}`, `{{drafts_url}}`,
`{{proof_pack_v1_url}}`, `{{approval_link}}`, `{{founder_name}}`.

---

## Subject
- AR: اليوم 5 · المسوّدات للمراجعة قبل اعتماد Proof Pack
- EN: Day 5 — Drafts ready for review before final Proof Pack

---

## Body — Arabic

أهلًا {{customer_name}}،

وصلنا منتصف Sprint `{{sprint_id}}`. هذه المسوّدات للمراجعة:

**1. Proof Pack v1 (مسودة)**
[{{proof_pack_v1_url}}]({{proof_pack_v1_url}})

تحتوي على:
- ملخص تنفيذي بالعربية والإنجليزية (≤ صفحة واحدة)
- DQ Report نهائي + تحسينات مقترحة
- Top-20 prospects نهائي مع ranking و evidence لكل صف
- 3 رسائل outreach drafts متنوعة (warm intro، direct، follow-up)
- تحليل الفجوات + خارطة طريق 30 يوم

**2. Outreach drafts للمراجعة الفردية**
كل رسالة في الـ approval queue:
- approval ID فردي لكل رسالة
- زر "approve" / "edit" / "reject" مع تعليق
- لا إرسال حتى موافقتك الصريحة

افتح الـ queue: [{{drafts_url}}]({{drafts_url}})

**3. ما نحتاجه منك خلال 48 ساعة**
- ✅ موافقة (أو تعديلات) على Proof Pack v1
- ✅ موافقة فردية على 10 من أصل 15 رسالة outreach (الباقي يدخل
  archive)
- ✅ تأكيد جدول اليوم 7 (handoff call)

تنبيه: لو لم نسمع منك خلال 48 ساعة، ندخل Sprint في "founder review
pause" تلقائيًا. لا ضياع وقت، ولا قرارات بنيابتك.

**رابط موحد للموافقة:** [{{approval_link}}]({{approval_link}})

شكرًا،
{{founder_name}}

---

## Body — English

Hello {{customer_name}},

We're at Sprint mid-point (`{{sprint_id}}`). Drafts ready for review:

**1. Proof Pack v1 (draft)**
[{{proof_pack_v1_url}}]({{proof_pack_v1_url}})

Contains:
- Executive summary in Arabic + English (≤ 1 page)
- Final DQ Report + improvement recommendations
- Final Top-20 prospects with ranking + evidence per row
- 3 outreach drafts in different angles (warm intro, direct, follow-up)
- Gap analysis + 30-day roadmap

**2. Outreach drafts (individual review)**
Each message lives in the approval queue with:
- Unique approval ID
- approve / edit / reject buttons with comment field
- No send until your explicit approval

Open the queue: [{{drafts_url}}]({{drafts_url}})

**3. What we need from you in 48 hours**
- ✅ Approve (or edit) Proof Pack v1
- ✅ Per-message approval on 10 of 15 outreach drafts (rest archived)
- ✅ Confirm Day 7 handoff call slot

Note: if we don't hear from you in 48 hours, the Sprint auto-enters
"founder review pause." No time wasted, no decisions taken on your
behalf.

**Unified approval link:** [{{approval_link}}]({{approval_link}})

Thanks,
{{founder_name}}

---

## Internal review checklist

- [ ] Proof Pack v1 generated from real ledger data
- [ ] Every Top-20 row has Level (L0-L5) evidence assigned
- [ ] 15 outreach drafts queued in approval_center
- [ ] approval_link valid for 48h
- [ ] Auto-pause logic confirmed (no autonomous send after timeout)
- [ ] Founder approval before send
