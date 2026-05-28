# Case Study Template · قالب دراسة الحالة

> Bilingual, 14 sections, doctrine-compliant. Every claim cited.
> No publication without customer's written approval at section 13.

**Merge fields:** `{{customer_handle}}`, `{{anon_label}}` (e.g.
"شركة لوجستيات سعودية متوسطة"), `{{sprint_id}}`, `{{proof_pack_ref}}`,
`{{publication_date}}`, `{{founder_name}}`, `{{customer_signoff_name}}`.

---

## 1. Customer permission level (مستوى الإذن)

Pick one (recorded with timestamp + signature):

- [ ] **Anonymous** — sector + size only, no name
- [ ] **Named** — company name OK, no individual quotes
- [ ] **Featured** — full quote-with-attribution + logo permission

Default: **Anonymous**. Escalation requires written approval.

---

## 2. Sector / Size / Geography (القطاع، الحجم، الموقع)

- Sector: {{sector}}
- Size: {{employee_count_range}} employees
- Geography: {{primary_city}} ({{country}})
- Engagement window: {{start_date}} → {{end_date}}

---

## 3. Pre-Dealix state (الوضع قبل Dealix)

**AR:** قبل التعاون مع Dealix، {{anon_label}} كانت تواجه:
- {{specific_pain_1}}
- {{specific_pain_2}}
- {{specific_pain_3}}

أرقام الوضع الراهن (مؤكدة من Discovery، not estimates):
- {{baseline_metric_1}}
- {{baseline_metric_2}}

**EN:** Before partnering with Dealix, {{anon_label}} was facing:
- {{specific_pain_1}}
- {{specific_pain_2}}
- {{specific_pain_3}}

Baseline metrics (confirmed from Discovery, not estimates):
- {{baseline_metric_1}}
- {{baseline_metric_2}}

**Citation:** Discovery transcript `proof_id: disc_{{sprint_id}}`.

---

## 4. Engagement scope (نطاق التعامل)

- Offer: {{offer_name}} ({{amount_sar}} SAR)
- Duration: {{duration_days}} days
- Deliverables agreed: {{deliverables_list}}
- Doctrine commitments restated to customer: {{commitments_list}}

---

## 5. Process narrative (سرد العملية)

### Week 1

**AR:** بدأ Sprint بـ {{week_1_kickoff}}. خلال أول ٧٢ ساعة، {{week_1_milestones}}.

**EN:** Sprint began with {{week_1_kickoff}}. In the first 72 hours,
{{week_1_milestones}}.

### Week 2 (if Managed Ops)

**AR:** {{week_2_narrative}}

**EN:** {{week_2_narrative}}

**Founder transparency note:** any rough spots in the engagement —
documented honestly (Doctrine #8 / #4). No success-washing.

---

## 6. Proof events captured (الأحداث المسجلة)

| Event ID | Type | Level (L0-L5) | Date | Source |
|----------|------|---------------|------|--------|
| {{evt_1_id}} | {{evt_1_type}} | {{evt_1_level}} | {{evt_1_date}} | {{evt_1_source}} |
| {{evt_2_id}} | {{evt_2_type}} | {{evt_2_level}} | {{evt_2_date}} | {{evt_2_source}} |

Only events at level L3 or higher are publishable. L0-L2 stay
internal.

Reference: `auto_client_acquisition/proof_ledger/file_backend.py`
documented evidence levels.

---

## 7. Outcomes (النتائج) — only verifiable

**AR — مؤكد بالأدلة:**
- {{outcome_1_metric}}: from {{baseline_1}} to {{new_1}} (proof:
  {{evt_1_id}})
- {{outcome_2_metric}}: from {{baseline_2}} to {{new_2}} (proof:
  {{evt_2_id}})

**AR — تحت المراقبة (لم يكتمل التحقق):**
- {{pending_outcome_1}} (estimated, no proof event yet)

**EN — Verified:**
- {{outcome_1_metric}}: from {{baseline_1}} to {{new_1}} (proof:
  {{evt_1_id}})
- {{outcome_2_metric}}: from {{baseline_2}} to {{new_2}} (proof:
  {{evt_2_id}})

**EN — Under observation (not yet verified):**
- {{pending_outcome_1}} (estimated, no proof event yet)

**Hard rule:** if there's no proof event, the outcome is in the
"under observation" section. NEVER promote unverified outcomes to
the verified section.

---

## 8. Founder reflection (تأمل الفاوندر)

**AR:** ما تعلمته من هذا التعامل {{founder_lesson_ar}}. ما كنا
سنفعله مختلفًا {{founder_would_change_ar}}.

**EN:** What I learned from this engagement: {{founder_lesson_en}}.
What we'd do differently: {{founder_would_change_en}}.

This section is mandatory — never publish a case study that's
purely glowing. Honest reflection signals integrity.

---

## 9. Customer testimonial (شهادة العميل)

If permission level = "Featured":

**AR (verbatim — never rewritten):**
> {{customer_quote_ar}}
>
> — {{customer_signoff_name}}, {{customer_title}}

**EN (verbatim):**
> {{customer_quote_en}}
>
> — {{customer_signoff_name}}, {{customer_title}}

If permission level < "Featured": leave this section as `null` and
state "Customer chose not to share a public statement."

---

## 10. ROI table (جدول العائد)

Only fill cells with confirmed numbers. Empty cells stay empty
(NOT zero).

| Metric | Pre-Dealix | After Dealix | Δ | Source |
|--------|------------|---------------|---|--------|
| {{m1}} | {{m1_pre}} | {{m1_post}} | {{m1_delta}} | {{m1_proof_id}} |
| {{m2}} | {{m2_pre}} | {{m2_post}} | {{m2_delta}} | {{m2_proof_id}} |
| {{m3}} | TBD | TBD | TBD | (no proof yet) |

`is_estimate=True` MUST flag any delta where the source is a
customer survey (not a system event).

---

## 11. Replicable pattern (النمط القابل للنسخ)

**AR:** هذا التعامل ينطبق على {{replicable_segment_ar}}. اللحظة التي
استفادت {{anon_label}} منها {{key_inflection_ar}}. الشركات
المشابهة يجب أن تبدأ بـ {{recommended_starting_offer}}.

**EN:** This engagement maps to {{replicable_segment_en}}. The
moment {{anon_label}} benefited most was {{key_inflection_en}}.
Similar companies should start with {{recommended_starting_offer}}.

---

## 12. Next engagement (التعامل التالي)

- Renewal status: {{renewal_status}} (active / pending / declined)
- If declined: documented reason (`docs/reference/CHURN_NOTES.md`)
- Upsell opportunity: {{upsell_path}} (or "none — engagement complete")

---

## 13. Approval signatures (التواقيع)

| Role | Name | Approval | Date | Signature |
|------|------|----------|------|-----------|
| Customer signatory | {{customer_signoff_name}} | [ ] approve [ ] reject | {{date}} | {{signature}} |
| Customer DPO (data privacy) | {{customer_dpo}} | [ ] approve [ ] reject | {{date}} | {{signature}} |
| Dealix founder | {{founder_name}} | [ ] approve [ ] reject | {{date}} | {{signature}} |

**Rule:** all three approvals required before any publication
(internal or external).

---

## 14. Publication readiness checklist (قائمة الجاهزية للنشر)

- [ ] All metrics cite a `proof_id`
- [ ] No unverified outcomes promoted to verified section
- [ ] Permission level matches what's actually used
- [ ] Customer reviewed full draft, written approval on file
- [ ] DPO confirmed no PII leak
- [ ] No internal terminology (V11/V12/agent names) leaked
- [ ] Bilingual quality check (a native AR speaker reviewed AR)
- [ ] Doctrine attestation: "this case study contains zero invented
      figures, zero unverified guarantees, and respects customer
      consent at every claim"
- [ ] Final sign-off by founder
- [ ] Stored in `data/case_studies/{{customer_handle}}.md`
- [ ] Logged in `proof_ledger` as `case_study_published` event

---

## Doctrine reminders (for the founder filling this in)

- **#4 NO_FAKE_PROOF:** every cell that can't cite a proof event
  stays empty.
- **#6 NO_UNVERIFIED_OUTCOMES:** under-observation outcomes stay
  separate from verified outcomes.
- **#5 NO_UNCONSENTED_DATA:** customer's name, logo, quote — each
  requires its own explicit approval level.
- **#8 NO_SILENT_FAILURES:** publish honest reflection in §8.
  Glowing-only case studies are signals of fabrication.
- **#10 NO_UNAUDITED_CHANGES:** every edit after first approval
  requires a new sign-off cycle.
