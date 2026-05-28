# Day 3 — Intelligence preview (bilingual)

> Draft template — never auto-sent. Founder approves.

**Merge fields:** `{{customer_name}}`, `{{sprint_id}}`, `{{top_10_url}}`,
`{{dq_report_url}}`, `{{review_call_url}}`, `{{founder_name}}`.

---

## Subject
- AR: اليوم 3 · معاينة Top-10 + تقرير جودة البيانات
- EN: Day 3 — Top-10 preview + Data Quality Report

---

## Body — Arabic

أهلًا {{customer_name}}،

أتممنا أول مرحلتين من Sprint `{{sprint_id}}`. هذه معاينة اليوم 3:

**1. Data Quality Report**
ابحث في التقرير عن:
- إجمالي الـ records المستلمة + النسبة الصالحة للاستخدام
- نسبة email coverage (٪) + phone coverage (٪)
- الـ duplicates المكتشفة
- تصنيف لكل tier (S/A/B/C/D) بالأسباب
- العلامات الحمراء (مثلًا: بيانات قديمة > 18 شهر)

رابط التقرير: [{{dq_report_url}}]({{dq_report_url}})

**2. Top-10 Prospects (شيتل قابل للتعديل)**
رتبناهم حسب الـ ICP fit:
- العمود "Why" يشرح لكل صف لماذا يستحق الاهتمام (event-based دائمًا،
  لا تخمين).
- العمود "Approach hint" يقترح زاوية فتح حوار (لا script جاهز).
- العمود "Compliance" يبين هل البيانات تُغطّى بـ legitimate interest
  أم تحتاج consent صريح.

شيت Top-10: [{{top_10_url}}]({{top_10_url}})

**3. اللاحق (يوم 5)**
نرسل drafts proof pack + رسائل outreach. كلها مفتوحة للتعديل قبل
الإرسال.

**اقتراح مكالمة 15 دقيقة هذا الأسبوع** لمناقشة:
- توافق ICP الفعلي مع المعاينة
- الأولوية: agency intros أم direct reach؟
- أي اعتراضات تحتاج معالجة في outreach drafts

احجز: [{{review_call_url}}]({{review_call_url}})

شكرًا،
{{founder_name}}

---

## Body — English

Hello {{customer_name}},

We've completed the first two stages of Sprint `{{sprint_id}}`. Day 3
preview:

**1. Data Quality Report**
Look for:
- Total records received + usable percentage
- Email coverage % + phone coverage %
- Duplicates detected
- Tier breakdown (S/A/B/C/D) with reasons
- Red flags (e.g. data older than 18 months)

Report: [{{dq_report_url}}]({{dq_report_url}})

**2. Top-10 Prospects (editable sheet)**
Ranked by ICP fit:
- "Why" column = event-based justification (never speculation)
- "Approach hint" = opening angle suggestion (not a script)
- "Compliance" = whether legitimate-interest covers contact or
  explicit consent is needed

Top-10 sheet: [{{top_10_url}}]({{top_10_url}})

**3. Next up (Day 5)**
We'll share draft proof pack + outreach messages. Everything is
editable before any send.

**Suggesting a 15-min call this week** to discuss:
- Real ICP alignment with the preview
- Priority: agency intros or direct reach?
- Objections to address in outreach drafts

Book: [{{review_call_url}}]({{review_call_url}})

Thanks,
{{founder_name}}

---

## Internal review checklist

- [ ] DQ report links to a real generated file
- [ ] Top-10 ranking traces to leadops_spine output
- [ ] Each "Why" column row passes is_estimate=False check
- [ ] Compliance column populated for each row
- [ ] Founder approval before send
