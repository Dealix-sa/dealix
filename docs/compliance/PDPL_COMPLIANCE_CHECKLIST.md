# قائمة التحقق من الامتثال — PDPL Compliance Checklist — Dealix

---

## Arabic / عربي

### مبادئ تقليل البيانات

Dealix تجمع البيانات الشخصية بالحد الأدنى الضروري لتقديم الخدمة فقط.

| المبدأ | التطبيق في Dealix |
|---|---|
| الضرورة | لا نجمع بيانات إلا إذا استلزمتها الخدمة المتعاقد عليها |
| الدقة | نتحقق من دقة البيانات عند الجمع ونصحح الأخطاء عند اكتشافها |
| التخزين الآمن | البيانات مشفّرة في التخزين والنقل |
| الحد الزمني | نحدد مدة الاحتفاظ قبل الجمع — لا احتفاظ غير محدود |

---

### متطلبات الموافقة للتواصل

قبل أي تواصل مباشر مع شركة أو فرد:

- [ ] مصدر بيانات الاتصال موثّق (source_url أو مصدر عام معلوم)
- [ ] لا بيانات شخصية حساسة (هوية وطنية، عنوان سكني، تاريخ ميلاد)
- [ ] رسالة التواصل تتضمن طريقة واضحة للانسحاب (opt-out)
- [ ] الاستهداف محدود لشركات B2B العامة — لا أفراد
- [ ] لا رسائل جماعية تلقائية — كل رسالة تُراجع بشرياً قبل الإرسال

**الموافقة الصريحة مطلوبة لـ:**
- أي تواصل مع عميل بعد انتهاء العقد لأغراض تسويقية
- إرسال تقارير أو تحليلات تخص بيانات العميل لطرف ثالث

---

### التزامات الانسحاب (Opt-Out)

- كل تواصل تجاري يتضمن خيار "إيقاف التواصل"
- طلب الانسحاب يُنفَّذ خلال 48 ساعة من الاستلام
- سجل الانسحابات يُحفظ ويُراجع شهرياً
- بيانات من طلب الانسحاب تُحذف أو تُبقى في قائمة "لا تتواصل" فقط

---

### سياسة الاحتفاظ بالبيانات

| نوع البيانات | مدة الاحتفاظ | ما يحدث بعدها |
|---|---|---|
| بيانات العملاء المحتملين (prospects) | 90 يوماً من آخر تواصل | حذف تلقائي من النظام + مراجعة يدوية |
| بيانات العميل النشط | مدة العقد + 12 شهراً | حذف أو أرشفة مجهّلة بموافقة العميل |
| سجلات التدقيق (audit logs) | 5 سنوات | أرشفة آمنة وفق النظام السعودي |
| الفواتير والعقود | 5 سنوات | أرشفة قانونية |
| مخرجات AI | 30 يوماً من تسليمها | حذف إلا إذا طلب العميل الاحتفاظ |

**الحذف عند الطلب:** أي شخص أو شركة يطلب حذف بياناته يُستجاب لطلبه خلال 72 ساعة.

---

### ما نجمعه ولماذا

| البيانات | السبب | الأساس القانوني |
|---|---|---|
| اسم الشركة + القطاع | تأهيل العميل المحتمل | مصلحة مشروعة (B2B عام) |
| اسم المسؤول + المسمى الوظيفي | التواصل المهني | مصلحة مشروعة (B2B عام) |
| معلومات الاتصال المهنية | التواصل التجاري | مصلحة مشروعة (B2B عام) |
| بيانات التشغيل (يقدمها العميل) | تقديم الخدمة المتعاقد عليها | تنفيذ العقد |
| سجلات الاجتماعات والمراسلات | التوثيق والامتثال | تنفيذ العقد + التزام قانوني |

**ما لا نجمعه أبداً:** هوية وطنية، عنوان سكني، بيانات مالية شخصية، بيانات صحية، بيانات ما دون 18 سنة.

---

### مقارنة PDPL السعودي و GDPR الأوروبي

| الجانب | PDPL السعودي | GDPR الأوروبي |
|---|---|---|
| نطاق التطبيق | البيانات الشخصية للأفراد | البيانات الشخصية للأفراد (أوسع تعريفاً) |
| حق الحذف | نعم | نعم |
| حق الوصول | نعم | نعم |
| الموافقة | مطلوبة (مع استثناءات B2B) | مطلوبة (صارمة) |
| الإبلاغ عن الاختراق | نعم — خلال 72 ساعة للجهة المختصة | نعم — خلال 72 ساعة |
| الغرامات | تحددها الهيئة السعودية | حتى 4% من الإيراد العالمي |
| المسؤول | الهيئة السعودية لحماية البيانات الشخصية | سلطات حماية البيانات الوطنية في الاتحاد الأوروبي |
| البيانات عبر الحدود | قيود على نقل البيانات خارج المملكة | قيود نقل البيانات خارج الاتحاد الأوروبي |

**الموقف:** Dealix تطبق معايير PDPL بالكامل وتتبع مبادئ GDPR كأفضل ممارسة إضافية حيث لا يتعارضان.

---

### التعامل مع بيانات الموظفين

- بيانات الموظفين (الحاليين والسابقين) تُعامل بأعلى مستوى حماية
- لا مشاركة بيانات الموظفين مع أي طرف خارجي دون موافقة صريحة
- سجلات الرواتب والأداء تُحفظ لمدة 5 سنوات بعد انتهاء العلاقة
- حق كل موظف في الاطلاع على بياناته المحفوظة

---

### التعامل مع بيانات مخرجات AI

- كل مخرج AI يُعلَّم كـ "مسودة" — لا يُعد قراراً نهائياً
- مخرجات AI لا تتضمن PII إلا إذا استلزمتها الخدمة بشكل صريح
- مخرجات AI تُحذف بعد 30 يوماً من تسليمها إلا إذا طلب العميل الاحتفاظ
- لا نستخدم بيانات عميل واحد لتدريب نماذج أو تحسين خدمة عميل آخر

---

### المراجعة السنوية

كل يناير، يُجري المؤسس مراجعة امتثال PDPL تشمل:
- [ ] مراجعة البيانات المحتفظ بها وحذف ما انتهت مدته
- [ ] مراجعة سياسة الخصوصية ومطابقتها للنظام الحالي
- [ ] التحقق من تحديث سجل الانسحابات
- [ ] مراجعة أي تغييرات في نظام PDPL السعودي
- [ ] توثيق نتائج المراجعة في ملف امتثال موقّت بالتاريخ

---

## English

### Data Minimisation Principles

Dealix collects personal data only to the minimum necessary to deliver the contracted service.

| Principle | Application at Dealix |
|---|---|
| Necessity | We collect no data unless required by the contracted service |
| Accuracy | We verify data accuracy at collection and correct errors when discovered |
| Secure storage | Data encrypted at rest and in transit |
| Time limit | Retention period defined before collection — no indefinite retention |

---

### Consent Requirements for Outreach

Before any direct contact with a company or individual:

- [ ] Contact data source is documented (source_url or known public source)
- [ ] No sensitive personal data (national ID, residential address, date of birth)
- [ ] Communication includes a clear opt-out method
- [ ] Targeting limited to public B2B companies — not individuals
- [ ] No automated bulk messages — every message reviewed by a human before sending

**Explicit consent required for:**
- Any post-contract marketing communication with a former client
- Sending reports or analyses containing client data to a third party

---

### Opt-Out Obligations

- Every commercial communication includes an "unsubscribe" option
- Opt-out requests are executed within 48 hours of receipt
- Opt-out records are maintained and reviewed monthly
- Data of opt-out requesters is deleted or retained in a "do not contact" list only

---

### Data Retention Policy

| Data Type | Retention Period | What Happens After |
|---|---|---|
| Prospect data | 90 days from last contact | System deletion + manual review |
| Active client data | Contract duration + 12 months | Delete or anonymised archive with client consent |
| Audit logs | 5 years | Secure archive per Saudi regulations |
| Invoices and contracts | 5 years | Legal archive |
| AI outputs | 30 days from delivery | Delete unless client requests retention |

**Deletion on request:** Any person or company requesting deletion of their data is responded to within 72 hours.

---

### What We Collect and Why

| Data | Reason | Legal Basis |
|---|---|---|
| Company name + sector | Prospect qualification | Legitimate interest (public B2B) |
| Responsible person name + title | Professional communication | Legitimate interest (public B2B) |
| Professional contact information | Commercial communication | Legitimate interest (public B2B) |
| Operational data (provided by client) | Delivering contracted service | Contract performance |
| Meeting and correspondence records | Documentation and compliance | Contract performance + legal obligation |

**What we never collect:** National ID, residential address, personal financial data, health data, data relating to persons under 18.

---

### Saudi PDPL vs. GDPR Comparison

| Aspect | Saudi PDPL | EU GDPR |
|---|---|---|
| Scope | Personal data of individuals | Personal data of individuals (broader definition) |
| Right to erasure | Yes | Yes |
| Right of access | Yes | Yes |
| Consent | Required (with B2B exceptions) | Required (stricter) |
| Breach notification | Yes — within 72 hours to competent authority | Yes — within 72 hours |
| Penalties | Set by Saudi Personal Data Protection Authority | Up to 4% of global revenue |
| Regulator | Saudi Personal Data Protection Authority | National data protection authorities in EU |
| Cross-border transfers | Restrictions on transferring data outside Saudi Arabia | Restrictions on transfers outside EU |

**Position:** Dealix fully applies PDPL standards and follows GDPR principles as additional best practice where they do not conflict.

---

### Employee Data Handling

- Employee data (current and former) is treated at the highest protection level
- No employee data is shared with any external party without explicit consent
- Salary and performance records are retained for 5 years after the relationship ends
- Every employee has the right to access their stored data

---

### AI Output Data Handling

- Every AI output is labelled "Draft" — it is not treated as a final decision
- AI outputs do not include PII unless explicitly required by the service
- AI outputs are deleted 30 days after delivery unless the client requests retention
- We do not use one client's data to train models or improve service for another client

---

### Annual Review Requirement

Each January, the founder conducts a PDPL compliance review covering:
- [ ] Review of retained data and deletion of expired records
- [ ] Review of privacy policy and alignment with current regulations
- [ ] Verification that opt-out records are up to date
- [ ] Review of any changes to Saudi PDPL regulations
- [ ] Documentation of review findings in a timestamped compliance file

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*

**Related documents:** [`docs/compliance/PDPL_OUTREACH_AND_AI_TRUST_CHECKLIST_AR.md`](PDPL_OUTREACH_AND_AI_TRUST_CHECKLIST_AR.md) · [`docs/04_data_os/DATA_RETENTION_POLICY.md`](../04_data_os/DATA_RETENTION_POLICY.md) · [`docs/ops/PDPL_BREACH_RUNBOOK.md`](../ops/PDPL_BREACH_RUNBOOK.md) · [`docs/compliance/ZATCA_READINESS_GUIDE_AR.md`](ZATCA_READINESS_GUIDE_AR.md)
