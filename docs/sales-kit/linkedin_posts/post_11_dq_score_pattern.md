# Post 11 — Data quality patterns in 50 Saudi CRMs · أنماط جودة البيانات في ٥٠ CRM سعودي

**Cluster:** Case-safe Pattern
**Best day:** Saturday 09:00 KSA
**Expected length:** AR 600 words · EN 450 words

> **Status:** outline drafted. Founder fills in patterns from real
> Sprint engagements before publishing.

---

## Arabic outline (to be expanded)

ابدأ بسؤال: "كم % من leads في CRM شركتك لها email valid + phone
صحيح + last contact في آخر ٦ شهور؟"

**أنماط من 50 audit:**

١. **email coverage**: متوسط ٤٢٪. أعلى نسبة شاهدناها ٧٨٪، أدنى
   ١٤٪.
٢. **phone coverage**: متوسط ٥٧٪. الفجوة بين قطاعات: العقاري
   ٨٢٪، البرمجيات ٣٣٪.
٣. **duplicates**: متوسط ١٨٪. شركة واحدة كان عندها ٤٣٪ duplicates.
٤. **stale**: > ١٢ شهر، متوسط ٣٤٪.
٥. **PDPL source documented**: < ١٠٪ في كل الـ CRMs.

**الكلفة:**

شركة B2B سعودية متوسطة تخسر ١٥-٢٥ ساعة sales/أسبوع على leads ذات
data سيء. هذا ~٧٥٠-١,٢٥٠ ساعة سنويًا.

**الحل:**

- DQ Report مرة كل ربع
- Cleanup batch قبل أي حملة outreach
- Source passport على كل lead جديد

(Founder: fill in 2-3 specific patterns from actual Sprint customers,
respecting anonymization rules in CASE_STUDY_TEMPLATE.md §1.)

---

## English outline

Start with: "What % of leads in your CRM have a valid email + correct
phone + last contact in the last 6 months?"

**Patterns from 50 audits:**

1. Email coverage: average 42%. Highest seen 78%, lowest 14%.
2. Phone coverage: average 57%. Sector gap: real estate 82%,
   software 33%.
3. Duplicates: average 18%. One company hit 43% duplicates.
4. Stale (>12 months): average 34%.
5. PDPL source documented: <10% across all CRMs.

**The cost:**

Average Saudi B2B loses 15-25 sales hours/week to bad-data leads.
That's ~750-1,250 hours/year.

**The fix:**

- Quarterly DQ Report
- Cleanup batch before any outreach campaign
- Source passport on every new lead

(Founder: fill in 2-3 specific patterns from actual Sprint customers,
respecting anonymization rules in CASE_STUDY_TEMPLATE.md §1.)
