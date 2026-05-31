{# قالب البريد الإلكتروني — الترحيب الفوري (خلال ساعتين من الدفع) #}
{# Email Template — Immediate Welcome (within 2h of payment) #}
{# المتغيرات: company_name, contact_name, service_tier, founder_name, engagement_id, kickoff_time, meeting_link, payment_amount, cta_url, unsubscribe_url #}

---

## الموضوع / Subject Line

**AR:** أهلاً بـ {{ company_name }} في Dealix — سبرنتكم يبدأ خلال 24 ساعة
**EN:** Welcome to Dealix, {{ contact_name }} — your sprint starts within 24 hours

---

## نص المعاينة / Preview Text

**AR:** تأكيد الاستلام + ما يحدث في الساعات القادمة خطوة بخطوة
**EN:** Payment confirmed + what happens next, step by step

---

## نص البريد الإلكتروني — النسخة العربية

أهلاً {{ contact_name }}،

وصلت دفعتكم ({{ payment_amount }} ريال) بنجاح، ورقم مشروعكم جاهز: **{{ engagement_id }}**.

مرحباً بكم في Dealix. هذه الرسالة تُوضّح بالضبط ما يحدث في الساعات الأربع والعشرين القادمة.

---

**خلال اليوم الأول — ما سيحدث:**

- سيتواصل معكم {{ founder_name }} لتأكيد موعد جلسة الانطلاق (45 دقيقة).
- ستصلكم رسالة بتفاصيل الجلسة ورابط الاجتماع.
- لا حاجة لأي إجراء منكم الآن سوى تأكيد الموعد المناسب.

**ما تحتاج تحضيره لجلسة الانطلاق:**

1. ملف بياناتكم — CSV أو تصدير من نظام CRM أو قائمة يدوية.
2. اسم الشخص المسؤول عن متابعة السبرنت من جهتكم.
3. سؤال عمل واحد تريدون الإجابة عنه خلال السبرنت.

**خطوط الحماية — ما لن يحدث أبداً:**

لن يُرسَل أي شيء باسمكم دون موافقتكم الصريحة المُسجَّلة. كل مسودة تواصل تُعلَّم "مسودة فقط" حتى تُعطوا الإذن صراحةً.

**مستوى الخدمة المختار:** {{ service_tier }}

إذا كان لديكم أي سؤال قبل الجلسة، ردّوا على هذا البريد مباشرةً.

[تأكيد موعد الجلسة — Confirm Kickoff Time]({{ cta_url }})

مع التقدير،
{{ founder_name }}
Dealix

---

## Email Body — English Version

Hello {{ contact_name }},

Your payment ({{ payment_amount }} SAR) has been received and your engagement is confirmed: **{{ engagement_id }}**.

Welcome to Dealix. This message explains exactly what happens in the next 24 hours.

---

**Within Day 1 — what will happen:**

- {{ founder_name }} will contact you to confirm your kickoff session time (45 minutes).
- You will receive a message with session details and the meeting link.
- No action required from you right now except confirming a time that works.

**What to prepare for your kickoff session:**

1. Your data file — CSV, CRM export, or a manual list.
2. The name of the person who will own the sprint workflow on your side.
3. One business question you want answered during the sprint.

**What will never happen:**

Nothing will be sent on your behalf without your explicit, logged approval. Every draft is marked "draft only" until you give express permission for each send.

**Service tier selected:** {{ service_tier }}

If you have any questions before the session, reply to this email directly.

[Confirm Kickoff Time]({{ cta_url }})

Best regards,
{{ founder_name }}
Dealix

---

## تذييل الحوكمة / Governance Footer

تمت مراجعة هذه الرسالة من قِبل المؤسس قبل الإرسال.
This message was reviewed by the founder before sending.

لإلغاء الاشتراك: {{ unsubscribe_url }}
To unsubscribe: {{ unsubscribe_url }}

معالجة البيانات وفق نظام حماية البيانات الشخصية السعودي (PDPL) — للاستفسار: dpo@dealix.sa
Data processed under the Saudi Personal Data Protection Law (PDPL) — enquiries: dpo@dealix.sa

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
