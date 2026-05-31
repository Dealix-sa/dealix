{# قالب البريد الإلكتروني — إنجاز اليوم الثالث من السبرنت #}
{# Email Template — Sprint Day 3 Milestone #}
{# المتغيرات: company_name, contact_name, service_tier, founder_name, engagement_id, dq_score, duplicate_count, top_accounts_count, feedback_question, cta_url, unsubscribe_url #}

---

## الموضوع / Subject Line

**AR:** تحديث اليوم 3 — {{ company_name }}: الحسابات العشرة الأولى مُحدَّدة
**EN:** Day 3 update — {{ company_name }}: top 10 accounts identified

---

## نص المعاينة / Preview Text

**AR:** درجة جودة البيانات + أولى النتائج + سؤال واحد يحتاج رأيكم
**EN:** Data quality score + first findings + one question that needs your input

---

## نص البريد الإلكتروني — النسخة العربية

أهلاً {{ contact_name }}،

اليوم الثالث من سبرنتكم اكتمل. نُشاركم أولى النتائج ونحتاج رأيكم في نقطة واحدة.

**رقم المشروع:** {{ engagement_id }}

---

**ما أُنجز في اليومين الماضيين:**

**اليوم 2 — جودة البيانات:**
- درجة جودة بياناتكم: **{{ dq_score }} / 100** عبر ستة أبعاد (الاكتمال، الصحة، التفرد، الاتساق، الحداثة، المطابقة).
- تكرارات محدَّدة: **{{ duplicate_count }} سجل** تمت معالجتها وفق قواعد الدمج الموثَّقة.

**اليوم 3 — ترتيب الحسابات:**
- **{{ top_accounts_count }} حساباً** صُنِّفت ضمن القائمة الأولوية مع مبررات قابلة للقراءة لكل حساب.
- معايير الترتيب: الملاءمة، قوة الإشارة، مخاطر الحوكمة.
- لا ترتيب بلا تفسير — كل حساب في القائمة مُبرَّر بجملة مقروءة.

---

**سؤال يحتاج إجابتكم:**

{{ feedback_question }}

ردّوا على هذه الرسالة بـ "موافق" أو شاركونا أي ملاحظة. هذا يُساعدنا على ضبط مسودّات اليوم الرابع قبل توليدها.

---

**الخطوة القادمة — اليوم 4:**

توليد مسودّات التواصل (عربي + إنجليزي) وتطبيق مصفوفة قرارات الحوكمة. كل مسودة ستُعلَّم "مسودة فقط" — لا شيء يُرسَل دون موافقتكم.

[اطّلع على النتائج — View Findings]({{ cta_url }})

{{ founder_name }}
Dealix

---

## Email Body — English Version

Hello {{ contact_name }},

Day 3 of your sprint is complete. We are sharing the first findings and need your input on one item.

**Engagement ID:** {{ engagement_id }}

---

**What has been completed in the past two days:**

**Day 2 — Data Quality:**
- Data quality score: **{{ dq_score }} / 100** across six dimensions (completeness, validity, uniqueness, consistency, timeliness, conformance).
- Duplicates identified: **{{ duplicate_count }} records** processed according to documented merge rules.

**Day 3 — Account Ranking:**
- **{{ top_accounts_count }} accounts** ranked as priority with human-readable justifications for each.
- Ranking criteria: fit, signal strength, governance risk.
- No rank without explanation — every account in the list has a readable justification.

---

**One question that needs your response:**

{{ feedback_question }}

Reply to this message with "confirmed" or share any observation. This helps us calibrate the Day 4 draft pack before it is generated.

---

**What comes next — Day 4:**

Bilingual draft pack generation (AR + EN) and governance decision matrix application. Every draft will be marked "draft only" — nothing is sent without your approval.

[View Findings]({{ cta_url }})

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
