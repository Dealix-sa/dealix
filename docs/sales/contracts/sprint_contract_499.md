# Dealix Sprint Engagement Agreement · 499 SAR
# اتفاقية Sprint بـ ٤٩٩ ر.س

> Bilingual contract template for the 7-day Sprint. Founder reviews
> + signs. Customer reviews + signs. Both required before kickoff.
> Doctrine-aligned (transparent terms, no hidden clauses).
>
> **Effective:** 2026-06-01

---

## Merge fields

`{{customer_company_name}}`, `{{customer_signatory_name}}`,
`{{customer_signatory_title}}`, `{{customer_email}}`,
`{{customer_cr_number}}`, `{{customer_vat_number}}`,
`{{contract_id}}`, `{{contract_date}}`, `{{sprint_start_date}}`,
`{{sprint_end_date}}`, `{{founder_name}}`, `{{founder_signature_date}}`.

---

## Arabic — العربية

### اتفاقية Dealix Sprint السبعة أيام

**رقم العقد:** `{{contract_id}}`
**التاريخ:** {{contract_date}}

**الطرف الأول (مزود الخدمة):**
Dealix · سامي العسيري (مؤسس)
البريد الإلكتروني: hello@dealix.me
السجل التجاري: (في انتظار اكتمال التسجيل)

**الطرف الثاني (العميل):**
{{customer_company_name}}
ممثلًا بـ: {{customer_signatory_name}}، {{customer_signatory_title}}
البريد الإلكتروني: {{customer_email}}
السجل التجاري: {{customer_cr_number}}
الرقم الضريبي: {{customer_vat_number}}

---

#### 1. نطاق الخدمة

Sprint السبعة أيام يشمل:
- يوم 0–1: kickoff call + تحديد أهداف
- يوم 1: data upload + DPA signed
- يوم 3: DQ Report + Top-10 prospects (bilingual)
- يوم 5: 15 outreach drafts + Proof Pack v1 (للمراجعة)
- يوم 7: Proof Pack نهائي ١٤ قسم + portable assets

#### 2. شروط الدفع

- **المبلغ:** ٤٩٩ ر.س (شامل ضريبة القيمة المضافة وفق ZATCA)
- **طريقة الدفع:** Moyasar (Mada/Visa/Mastercard/Apple Pay)
- **الفاتورة:** تُصدر تلقائيًا بعد الدفع، متوافقة مع ZATCA Phase 2
- **توقيت السداد:** الدفع المسبق قبل بدء Sprint

#### 3. سياسة الاسترجاع

استرجاع كامل ٤٩٩ ر.س لو:
- Sprint اكتمل بدون أي proof event (L3+) في ledger
- لم نقدم Top-10 prospects أو DQ Report ضمن ٧ أيام
- DPA كشف أن البيانات غير قابلة للاستخدام (refund قبل أي outreach)

تفاصيل كاملة: `docs/contributing/REFUND_POLICY.md`

#### 4. حماية البيانات (DPA)

- البيانات تخضع لـ نظام حماية البيانات الشخصية السعودي (PDPL)
- التخزين: Postgres مشفر at-rest، region: KSA (Riyadh)
- الاحتفاظ: ٩٠ يوم من نهاية Sprint ثم حذف تلقائي
- مرجع DPA كامل: `docs/operations/PDPL_PUBLIC_STATEMENT.md`

#### 5. إقرار الـ Doctrine (١١ خط أحمر)

Dealix يلتزم خلال Sprint بـ:
1. لا إرسال خارجي تلقائي (كل draft يمر بموافقتكم)
2. لا cold WhatsApp
3. لا scraping
4. كل رقم في Proof Pack يحمل proof_id أو is_estimate=true
5. PDPL lawful basis مسجل لكل lead
6. لا ضمانات أداء مالي مزيفة
7. أسعار شفافة (هذا العقد علني)
8. كل خطأ موثق ومُكتشف
9. agents بحدود محددة
10. كل تغيير في الـ doctrine يخضع لمراجعة + إشعار العميل
11. لا LinkedIn automation

تفاصيل: `docs/architecture/DOCTRINE_MANIFESTO.md`

#### 6. شروط الإلغاء

- قبل kickoff call: إلغاء بدون أي رسوم
- بعد kickoff لكن قبل day 3: استرجاع ٥٠٪
- بعد day 3: غير قابل للاسترجاع إلا وفق Section 3

#### 7. الملكية الفكرية

- Proof Pack والمحتوى المخصص ملك للعميل
- الـ Dealix doctrine + tools تبقى ملك Dealix
- العميل يستطيع نشر Proof Pack بحرية بعد الموافقة على نشر بياناته
  المسماة (Doctrine #5)

#### 8. القانون الحاكم

- يخضع هذا العقد لأنظمة المملكة العربية السعودية
- النزاعات تُحل عبر التحكيم في الرياض

#### 9. التوقيع

**عن العميل ({{customer_company_name}}):**
الاسم: {{customer_signatory_name}}
المنصب: {{customer_signatory_title}}
التاريخ: ___________
التوقيع: ___________

**عن Dealix:**
الاسم: سامي العسيري
المنصب: مؤسس Dealix
التاريخ: {{founder_signature_date}}
التوقيع: ___________

---

## English

### Dealix 7-Day Sprint Engagement Agreement

**Contract ID:** `{{contract_id}}`
**Date:** {{contract_date}}

**Provider:** Dealix · Sami Assiri (Founder)
Email: hello@dealix.me

**Customer:** {{customer_company_name}}
Represented by: {{customer_signatory_name}}, {{customer_signatory_title}}
Email: {{customer_email}}
CR: {{customer_cr_number}}
VAT: {{customer_vat_number}}

---

#### 1. Scope

The 7-day Sprint includes:
- Day 0–1: kickoff call + goal alignment
- Day 1: data upload + DPA signed
- Day 3: DQ Report + Top-10 prospects (bilingual)
- Day 5: 15 outreach drafts + Proof Pack v1 (for review)
- Day 7: Final 14-section Proof Pack + portable assets

#### 2. Payment terms

- **Amount:** 499 SAR (VAT included, ZATCA-compliant)
- **Method:** Moyasar (Mada/Visa/Mastercard/Apple Pay)
- **Invoice:** auto-issued post-payment, ZATCA Phase 2 compliant
- **Timing:** prepaid before Sprint start

#### 3. Refund policy

Full 499 SAR refund if:
- Sprint completes with zero proof events (L3+) in ledger
- Top-10 prospects or DQ Report not delivered within 7 days
- DPA reveals data was unusable (refund before any outreach)

Full details: `docs/contributing/REFUND_POLICY.md`

#### 4. Data protection (DPA)

- Data governed by Saudi PDPL
- Storage: Postgres encrypted at-rest, region: KSA (Riyadh)
- Retention: 90 days from Sprint end, then auto-delete
- Full DPA reference: `docs/operations/PDPL_PUBLIC_STATEMENT.md`

#### 5. Doctrine attestation (the 11 non-negotiables)

Dealix commits during Sprint to the 11 non-negotiables documented
at `docs/architecture/DOCTRINE_MANIFESTO.md`.

#### 6. Cancellation

- Pre-kickoff: cancel with no fee
- Post-kickoff but pre-Day-3: 50% refund
- Post-Day-3: non-refundable except per Section 3

#### 7. IP rights

- Proof Pack + customized content belongs to Customer
- Dealix doctrine + tools remain property of Dealix
- Customer can publish Proof Pack freely after consenting to named
  data publication (Doctrine #5)

#### 8. Governing law

- Subject to laws of Saudi Arabia
- Disputes resolved via arbitration in Riyadh

#### 9. Signatures

**For Customer ({{customer_company_name}}):**
Name: {{customer_signatory_name}}
Title: {{customer_signatory_title}}
Date: ___________
Signature: ___________

**For Dealix:**
Name: Sami Assiri
Title: Founder, Dealix
Date: {{founder_signature_date}}
Signature: ___________

---

## Internal review checklist (founder before send)

- [ ] Customer name + signatory verified
- [ ] CR number + VAT number captured
- [ ] Sprint start/end dates filled
- [ ] DPA URL points to current version
- [ ] Contract logged in proof_ledger as `contract_drafted`
- [ ] Customer agreed to doctrine attestation explicitly
- [ ] Founder signed before sending to customer
