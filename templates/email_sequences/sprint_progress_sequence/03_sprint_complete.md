{# قالب البريد الإلكتروني — اكتمال السبرنت واستدعاء مراجعة التسليم #}
{# Email Template — Sprint Complete, Proof Pack Delivered, Invite Review Call #}
{# المتغيرات: company_name, contact_name, service_tier, founder_name, engagement_id, proof_score, capital_asset_summary, second_payment_amount, payment_link, review_call_link, cta_url, unsubscribe_url #}

---

## الموضوع / Subject Line

**AR:** السبرنت مكتمل — {{ company_name }}: حزمة الإثبات مُسلَّمة
**EN:** Sprint complete — {{ company_name }}: Proof Pack delivered

---

## نص المعاينة / Preview Text

**AR:** 7 أيام، 14 قسماً، درجة {{ proof_score }} — وما الخطوة التالية
**EN:** 7 days, 14 sections, score {{ proof_score }} — and what comes next

---

## نص البريد الإلكتروني — النسخة العربية

أهلاً {{ contact_name }}،

سبرنت ذكاء الإيرادات اكتمل. حزمة الإثبات مُسلَّمة في مشروعكم.

**رقم المشروع:** {{ engagement_id }}
**درجة الإثبات النهائية:** {{ proof_score }} / 100

---

**ملخص ما أُنجز في سبعة أيام:**

| البند | النتيجة |
|-------|---------|
| جواز المصدر | موقَّع ومُودَع |
| درجة جودة البيانات | مُقاسة ومُوثَّقة |
| التكرارات | مُحدَّدة ومُدمَجة |
| الحسابات المُرتَّبة | أفضل 10 مع مبررات مقروءة |
| مسودّات التواصل | ثنائية اللغة، مُعلَّمة "مسودة فقط" |
| سجل الحوكمة | كل قرار مُسجَّل بهوية ووقت |
| حزمة الإثبات | 14 قسماً مكتملة |
| الأصل الرأسمالي | {{ capital_asset_summary }} |

---

**الدفعة الثانية:**

رابط الدفع ({{ second_payment_amount }} ريال): [{{ payment_link }}]({{ payment_link }})

تُرسَل فاتورة ZATCA إلكترونية خلال يوم عمل من الاستلام.

---

**جلسة المراجعة (اختياري):**

إذا أردتم مراجعة الحزمة معاً بعد قراءتها، الجلسة متاحة لمدة 30 دقيقة خلال الأيام الثلاثة القادمة.

[احجز جلسة المراجعة]({{ review_call_link }})

---

**الخطوة التالية:**

بناءً على درجة الإثبات ومؤشر الاعتماد، سنُشاركم خلال الأسبوع القادم تقييماً لمدى أهليتكم لعقد الاحتفاظ الشهري — لا التزام من جهتكم للاطلاع عليه.

شكراً لثقتكم في Dealix.

{{ founder_name }}
Dealix

---

## Email Body — English Version

Hello {{ contact_name }},

The Revenue Intelligence Sprint is complete. The Proof Pack has been delivered to your engagement folder.

**Engagement ID:** {{ engagement_id }}
**Final Proof Score:** {{ proof_score }} / 100

---

**Seven-day summary:**

| Item | Result |
|------|--------|
| Source Passport | Signed and filed |
| Data Quality Score | Measured and documented |
| Deduplication | Identified and merged |
| Ranked Accounts | Top 10 with readable justifications |
| Draft Pack | Bilingual (AR + EN), marked "draft only" |
| Governance Log | Every decision logged with identity and timestamp |
| Proof Pack | 14 sections complete |
| Capital Asset | {{ capital_asset_summary }} |

---

**Second payment:**

Payment link ({{ second_payment_amount }} SAR): [{{ payment_link }}]({{ payment_link }})

A ZATCA-compliant e-invoice will be sent within one business day of receipt.

---

**Review session (optional):**

If you would like to walk through the Proof Pack together after reading it, a 30-minute session is available within the next three business days.

[Book Review Session]({{ review_call_link }})

---

**What comes next:**

Based on your proof score and adoption indicators, we will share an assessment of your eligibility for the monthly retainer within the coming week — no commitment required from your side to receive it.

Thank you for your trust in Dealix.

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
