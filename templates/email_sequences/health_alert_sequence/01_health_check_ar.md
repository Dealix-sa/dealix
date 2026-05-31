{# قالب البريد الإلكتروني — فحص الصحة للعميل المعرّض للخطر (عربي أولاً) #}
{# Email Template — Health Check for AT_RISK Customer (Arabic-primary) #}
{# المتغيرات: company_name, contact_name, service_tier, founder_name, engagement_id, health_signal_summary, last_interaction_date, cta_url, unsubscribe_url #}

---

## الموضوع / Subject Line

**AR:** {{ contact_name }} — لاحظنا بعض الإشارات ونريد التأكد من سير الأمور
**EN:** {{ contact_name }} — we noticed some signals and want to check in

---

## نص المعاينة / Preview Text

**AR:** لا شيء سلبي — فقط نريد أن نسمع منكم مباشرةً
**EN:** Nothing negative — we just want to hear from you directly

---

## نص البريد الإلكتروني — النسخة العربية

أهلاً {{ contact_name }}،

أُرسل هذا البريد مباشرةً لأننا لاحظنا بعض الإشارات في مشروعكم تستوقفني.

**رقم المشروع:** {{ engagement_id }}
**آخر تفاعل مُسجَّل:** {{ last_interaction_date }}

---

**ما لاحظناه:**

{{ health_signal_summary }}

هذا لا يعني بالضرورة أن هناك مشكلة. لكنه يعني أننا يجب أن نتحدث قبل أن تتراكم أي احتكاكات صغيرة.

---

**سؤال واحد:**

هل سير الأمور يسير وفق ما توقعتم؟ إذا كان الجواب "لا" بأي درجة — هذا هو الوقت الصحيح لقوله.

Dealix لا يعمل بنظام "أنهينا السبرنت وانتهى". المشروع ينتهي عندما تكونون أنتم راضين عن ما أُنجز.

---

**الخطوة:**

ردّوا على هذا البريد بأي من الآتي:

- "الأمور تسير بشكل جيد" — وسنستمر على المسار الحالي.
- "لدي ملاحظة" — وسأتواصل معكم خلال 24 ساعة.
- "أريد محادثة" — [احجز 30 دقيقة هنا]({{ cta_url }}).

{{ founder_name }}
Dealix

---

## Email Body — English Version

Hello {{ contact_name }},

I am reaching out directly because we noticed some signals in your engagement that have my attention.

**Engagement ID:** {{ engagement_id }}
**Last recorded interaction:** {{ last_interaction_date }}

---

**What we observed:**

{{ health_signal_summary }}

This does not necessarily indicate a problem. But it means we should talk before small frictions accumulate.

---

**One question:**

Is the engagement progressing as you expected? If the answer is "not quite" in any way — now is the right time to say so.

Dealix does not operate on a "sprint complete and done" basis. The engagement is complete when you are satisfied with what was delivered.

---

**Next step:**

Reply to this message with one of the following:

- "All is going well" — and we continue on the current track.
- "I have a note" — and I will contact you within 24 hours.
- "I want a call" — [Book 30 minutes here]({{ cta_url }}).

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
