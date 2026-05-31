{# قالب البريد الإلكتروني — قرار الاحتفاظ: نعم أو لا، بدون ضغط #}
{# Email Template — Retainer Decision: Yes or No, No Pressure #}
{# المتغيرات: company_name, contact_name, service_tier, founder_name, engagement_id, retainer_price, retainer_tier, discussion_link, cta_url, unsubscribe_url #}

---

## الموضوع / Subject Line

**AR:** {{ contact_name }}: نعم أو لا — لا يوجد بريد رابع بعد هذا
**EN:** {{ contact_name }}: yes or no — there is no fourth email after this one

---

## نص المعاينة / Preview Text

**AR:** قرار بسيط، لا ضغط، مع عرض للحديث إذا أردتم
**EN:** A simple decision, no pressure, with an offer to talk if you would like

---

## نص البريد الإلكتروني — النسخة العربية

أهلاً {{ contact_name }}،

هذا آخر بريد في سلسلة عقد الاحتفاظ.

أُقدّر وقتكم، لذا لن أكرر ما قلته في الرسائل السابقة. سؤال مباشر:

**هل يُلائمكم الانتقال إلى عقد الاحتفاظ الشهري ({{ retainer_price }} ريال / {{ retainer_tier }}) الآن؟**

**نعم:** ردّوا على هذا البريد بـ "نعم" وسأُرسل نطاق العقد ورابط الدفع خلال 24 ساعة.

**لا ليس الآن:** ردّوا بـ "لاحقاً" وسأُدرجكم على قائمة التواصل الدوري كل ثلاثة أشهر — فقط إذا طرأ شيء يُلائم قطاعكم.

**لا أريد الاستمرار:** ردّوا بـ "أغلق" وسيُوقَف التواصل تماماً. لا غضب، لا متابعة.

---

**إذا كان لديكم سؤال:**

الخيار الرابع هو حجز 20 دقيقة للحديث مباشرةً:
[احجز محادثة]({{ discussion_link }})

لا يُوجد عرض "محدود الوقت" هنا. السعر والنطاق ثابتان.

شكراً على وقتكم طوال مسيرة السبرنت.

{{ founder_name }}
Dealix

---

## Email Body — English Version

Hello {{ contact_name }},

This is the final message in the retainer sequence.

I respect your time, so I will not repeat what I said in the previous messages. A direct question:

**Is it the right time for you to move to the monthly retainer ({{ retainer_price }} SAR / {{ retainer_tier }})?**

**Yes:** Reply with "yes" and I will send the contract scope and payment link within 24 hours.

**Not right now:** Reply with "later" and I will add you to a quarterly touch list — only if something relevant to your sector comes up.

**Not interested:** Reply with "close" and all follow-up stops. No pressure, no further messages.

---

**If you have a question:**

A fourth option is booking 20 minutes to talk directly:
[Book a Conversation]({{ discussion_link }})

There is no "limited time" offer here. The price and scope are fixed.

Thank you for your time throughout the sprint.

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
