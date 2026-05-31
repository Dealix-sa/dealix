# Dealix Custom AI Engagement Agreement (Milestone-Based)
# اتفاقية Custom AI Engagement (milestone)

> Scoped custom engagement (5,000–25,000 SAR). Milestone-based payment.
> Founder + Customer sign before kickoff.

---

## Merge fields

`{{customer_company_name}}`, `{{customer_signatory_name}}`,
`{{engagement_scope_summary}}`, `{{total_amount_sar}}`,
`{{milestone_1_description}}`, `{{milestone_1_amount}}`,
`{{milestone_2_description}}`, `{{milestone_2_amount}}`,
`{{milestone_3_description}}`, `{{milestone_3_amount}}`,
`{{estimated_weeks}}`, `{{contract_id}}`, `{{founder_name}}`.

---

## Arabic

### اتفاقية Custom AI Engagement (Milestone)

**رقم العقد:** {{contract_id}}
**نطاق العمل:** {{engagement_scope_summary}}
**المبلغ الإجمالي:** {{total_amount_sar}} ر.س
**المدة المتوقعة:** {{estimated_weeks}} أسبوع

#### 1. الـ Milestones والمدفوعات

| Milestone | الوصف | المبلغ (ر.س) | الـ Delivery |
|-----------|-------|--------------|--------------|
| 1 | {{milestone_1_description}} | {{milestone_1_amount}} | اعتماد كتابي |
| 2 | {{milestone_2_description}} | {{milestone_2_amount}} | اعتماد كتابي |
| 3 | {{milestone_3_description}} | {{milestone_3_amount}} | اعتماد + Proof Pack |

- **Milestone 1 (kickoff):** ٣٠٪ من المبلغ
- **Milestone 2 (midway):** ٤٠٪
- **Milestone 3 (delivery):** ٣٠٪

كل milestone: invoice منفصل (ZATCA-compliant)، charge عبر Moyasar،
proof_ledger event مسجل.

#### 2. سياسة الاسترجاع

- استرجاع للـ milestone غير المكتمل
- لا استرجاع للـ milestone الذي اعتمده العميل كتابيًا
- لو تم اكتشاف عدم قابلية تنفيذ الـ scope بعد kickoff → استرجاع ١٠٠٪
  من Milestone 1

#### 3. الملكية الفكرية

- الـ deliverables المخصصة تنتقل ملكيتها للعميل عند اعتماد Milestone 3
- الـ Dealix doctrine + tools generic تبقى ملك Dealix
- العميل يحق له نشر الـ deliverables ضمن business legitimate
  internal use

#### 4. شروط الإنهاء

- الإنهاء بالاتفاق المتبادل: استرجاع Milestone غير المكتمل
- الإنهاء من Dealix: لو العميل خرق doctrine — استرجاع Milestone غير
  المكتمل + إعادة بيانات
- الإنهاء من العميل: لو فشل Dealix في تسليم Milestone خلال ١٥ يوم
  بعد الموعد المتفق عليه → استرجاع كامل لـ Milestone غير المكتمل

#### 5. Doctrine attestation

كل clauses Doctrine #1-11 تنطبق. تفاصيل في
`docs/architecture/DOCTRINE_MANIFESTO.md`.

#### 6. التوقيع

[نفس بلوك التوقيع في Sprint contract]

---

## English

### Custom AI Engagement Agreement (Milestone)

**Contract ID:** {{contract_id}}
**Scope:** {{engagement_scope_summary}}
**Total amount:** {{total_amount_sar}} SAR
**Estimated duration:** {{estimated_weeks}} weeks

#### 1. Milestones + payments

| Milestone | Description | Amount (SAR) | Delivery |
|-----------|-------------|--------------|----------|
| 1 | {{milestone_1_description}} | {{milestone_1_amount}} | Written acceptance |
| 2 | {{milestone_2_description}} | {{milestone_2_amount}} | Written acceptance |
| 3 | {{milestone_3_description}} | {{milestone_3_amount}} | Acceptance + Proof Pack |

- **Milestone 1 (kickoff):** 30%
- **Milestone 2 (midway):** 40%
- **Milestone 3 (delivery):** 30%

Each milestone: separate invoice (ZATCA-compliant), Moyasar charge,
proof_ledger event recorded.

#### 2. Refund policy

- Refund for any incomplete milestone
- No refund for milestones customer accepted in writing
- If scope discovered infeasible after kickoff → 100% refund of
  Milestone 1

#### 3. IP rights

- Custom deliverables transfer to Customer at Milestone 3 acceptance
- Generic Dealix doctrine + tools remain Dealix property
- Customer may publish deliverables within legitimate business
  internal use

#### 4. Termination

- Mutual termination: refund of incomplete milestones
- Termination by Dealix: if Customer breaches doctrine — refund
  incomplete milestones + return data
- Termination by Customer: if Dealix fails to deliver a milestone
  within 15 days of agreed date → full refund of incomplete milestone

#### 5. Doctrine attestation

All Doctrine #1-11 clauses apply. Details:
`docs/architecture/DOCTRINE_MANIFESTO.md`.

#### 6. Signatures

[Standard signature block]

---

## Internal review checklist

- [ ] Scope summary specific (not vague)
- [ ] Each milestone has acceptance criteria written
- [ ] Total amount aligns with 30/40/30 split
- [ ] Refund triggers documented
- [ ] IP transfer trigger explicit
- [ ] Customer signatory has authority
- [ ] Founder signed before customer
