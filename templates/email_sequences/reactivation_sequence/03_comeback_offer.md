{# قالب البريد الإلكتروني — عرض العودة المحدد (إعادة التنشيط النهائي) #}
{# Email Template — Specific Reactivation Offer (final reactivation) #}
{# المتغيرات: company_name, contact_name, service_tier, founder_name, engagement_id, comeback_offer_ar, comeback_offer_en, offer_price, offer_validity_date, cta_url, unsubscribe_url #}

---

## الموضوع / Subject Line

**AR:** {{ contact_name }} — عرض إعادة انطلاق مُحدَّد صالح حتى {{ offer_validity_date }}
**EN:** {{ contact_name }} — a specific restart offer, valid until {{ offer_validity_date }}

---

## نص المعاينة / Preview Text

**AR:** هذا آخر تواصل في هذا الدور — عرض واحد واضح بدون ضغط
**EN:** This is the final outreach in this cycle — one clear offer, no pressure

---

## نص البريد الإلكتروني — النسخة العربية

أهلاً {{ contact_name }}،

هذا آخر تواصل في دورة إعادة التنشيط الحالية.

**رقم مشروعكم السابق:** {{ engagement_id }}

---

**عرض إعادة الانطلاق:**

{{ comeback_offer_ar }}

**التكلفة:** {{ offer_price }} ريال سعودي.
**صلاحية العرض:** حتى {{ offer_validity_date }}.

هذا العرض ليس "خصماً تسويقياً" — هو عرض محسوب بناءً على ما أُنجز في مشروعكم السابق وما يمكن إعادة استخدامه بدون إعادة البناء من الصفر.

---

**ما لا يتضمّنه هذا العرض:**

- لا وعود بنتائج إيرادية مُحدَّدة.
- لا إجراء خارجي دون موافقتكم الصريحة.
- لا امتداد تلقائي للعقد بعد انتهاء النطاق.

---

**بعد {{ offer_validity_date }}:**

إذا لم يصلني رد، أُغلق هذه الدورة ويبقى ملفكم في قاعدة البيانات للتواصل الفصلي العادي فقط. لا إرسال تلقائي، لا متابعة مكثّفة.

[قبول عرض إعادة الانطلاق]({{ cta_url }})

{{ founder_name }}
Dealix

---

## Email Body — English Version

Hello {{ contact_name }},

This is the final outreach in the current reactivation cycle.

**Previous engagement ID:** {{ engagement_id }}

---

**Restart offer:**

{{ comeback_offer_en }}

**Cost:** {{ offer_price }} SAR.
**Offer valid until:** {{ offer_validity_date }}.

This offer is not a "marketing discount" — it is a calculated offer based on what was completed in your previous engagement and what can be reused without rebuilding from zero.

---

**What this offer does not include:**

- No promises of specific revenue outcomes.
- No external action without your explicit approval.
- No automatic contract extension after the scope is complete.

---

**After {{ offer_validity_date }}:**

If no reply is received, I close this cycle and your file remains in the database for regular quarterly outreach only. No automated sending, no intensive follow-up.

[Accept the Restart Offer]({{ cta_url }})

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
