{# قالب البريد الإلكتروني — خطة الإنقاذ (إذا لم يكن هناك رد) #}
{# Email Template — Rescue Plan Proposal (if no response to previous messages) #}
{# المتغيرات: company_name, contact_name, service_tier, founder_name, engagement_id, days_silent, rescue_scope_ar, rescue_scope_en, rescue_cost, close_date, cta_url, unsubscribe_url #}

---

## الموضوع / Subject Line

**AR:** {{ contact_name }} — خطة إنقاذ واضحة أو إغلاق نظيف: {{ close_date }}
**EN:** {{ contact_name }} — a clear rescue plan or clean close: {{ close_date }}

---

## نص المعاينة / Preview Text

**AR:** بعد {{ days_silent }} يوماً من الصمت: هذا آخر عرض قبل إغلاق المشروع
**EN:** After {{ days_silent }} days of silence: this is the final offer before engagement closes

---

## نص البريد الإلكتروني — النسخة العربية

أهلاً {{ contact_name }}،

لم يصلني رد على رسالتَي السابقتَين. أحترم ذلك.

**رقم المشروع:** {{ engagement_id }}

---

**الوضع الحالي:**

{{ days_silent }} يوماً دون تواصل. لا أفترض السبب — قد يكون ضغط عمل، أو تغيير أولويات، أو رأي مختلف حول المشروع. كل هذا مفهوم.

---

**خياران واضحان:**

**الخيار الأول — خطة الإنقاذ:**

{{ rescue_scope_ar }}

التكلفة: {{ rescue_cost }} ريال. المدة التقديرية: مُحدَّدة في نطاق الخطة.

إذا اخترتم هذا الخيار، ردّوا على هذا البريد بـ "أرسل خطة الإنقاذ" وسأُرتّب محادثة خلال 48 ساعة.

**الخيار الثاني — الإغلاق النظيف:**

يُوثَّق ما أُنجز، تُحفَظ بياناتكم وفق سياسة PDPL، ويُغلَق المشروع برسالة اختتام رسمية. لا رسوم إضافية. لا متابعة مستقبلية إلا إذا طلبتم ذلك.

---

**التاريخ النهائي للرد:** {{ close_date }}

بعد هذا التاريخ يُغلَق المشروع تلقائياً وفق الخيار الثاني — الإغلاق النظيف.

[اختر الخطة المناسبة]({{ cta_url }})

{{ founder_name }}
Dealix

---

## Email Body — English Version

Hello {{ contact_name }},

I have not received a reply to my two previous messages. I respect that.

**Engagement ID:** {{ engagement_id }}

---

**Current situation:**

{{ days_silent }} days without contact. I am not assuming the reason — it may be work pressure, shifting priorities, or a different view of the engagement. All of that is understandable.

---

**Two clear options:**

**Option 1 — Rescue Plan:**

{{ rescue_scope_en }}

Cost: {{ rescue_cost }} SAR. Estimated duration: specified in the plan scope.

If you choose this option, reply with "send rescue plan" and I will arrange a conversation within 48 hours.

**Option 2 — Clean Close:**

What was completed is documented, your data is preserved according to PDPL policy, and the engagement closes with a formal closure message. No additional fees. No future follow-up unless you request it.

---

**Final response date:** {{ close_date }}

After this date, the engagement automatically closes under Option 2 — the clean close.

[Choose the Right Path]({{ cta_url }})

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
