# Proposal Template · قالب العرض

> Bilingual. Doctrine-aligned. Every number ties to discovery answers
> — no fabrication. Use after Discovery + Diagnostic, never before.

**Merge fields:** `{{customer_name}}`, `{{company_name}}`, `{{sector}}`,
`{{discovery_pain_summary}}`, `{{recommended_offer}}`, `{{founder_name}}`,
`{{proposal_id}}`, `{{valid_until}}`, `{{dpa_url}}`.

---

## 1. Situation (الوضع الراهن)

**AR:** بناءً على جلسة Discovery في {{discovery_date}}، {{company_name}}
تواجه تحديًا في {{discovery_pain_summary}}. الحجم التقريبي
(is_estimate=True): ~{{leads_per_month}} lead/شهر، {{response_time}}
ساعة وقت الاستجابة، {{conversion_rate}}٪ معدل التحويل.

**EN:** Based on the Discovery session on {{discovery_date}},
{{company_name}} is facing a challenge in {{discovery_pain_summary}}.
Approximate scale (is_estimate=True): ~{{leads_per_month}} leads/mo,
{{response_time}} hr response time, {{conversion_rate}}% conversion.

**Sources for the numbers above:**
- Discovery interview transcript (proof_id: `disc_{{proposal_id}}`)
- Diagnostic intake form (if completed)

If any number is missing from Discovery, mark as `TBD` — do NOT
estimate from category averages.

---

## 2. Recommended approach (المقترح)

**AR:** نقترح **{{recommended_offer}}** كنقطة بداية. الأسباب:

1. {{reason_1_aligned_to_pain}}
2. {{reason_2_aligned_to_scale}}
3. {{reason_3_doctrine_fit}}

**EN:** We recommend **{{recommended_offer}}** as the starting point.
Reasons:

1. {{reason_1_aligned_to_pain}}
2. {{reason_2_aligned_to_scale}}
3. {{reason_3_doctrine_fit}}

---

## 3. Deliverables (التسليمات)

For the chosen offer, list exact files/links the customer receives.
Reference the 14-section Proof Pack structure where applicable.

### If `recommended_offer = pilot_managed` (499 SAR Sprint, 7 days)

| Day | Deliverable | Format |
|-----|--------------|--------|
| 0   | Welcome + kickoff call | Email + 20-min Zoom |
| 1   | Data sources request | Email + secure upload link |
| 3   | DQ Report + Top-10 preview | Markdown + CSV |
| 5   | Proof Pack v1 + 15 outreach drafts | Markdown + approval queue |
| 7   | Final Proof Pack (14 sections, bilingual) + portable assets | Markdown + ZIP |

### If `recommended_offer = managed_revenue_ops_growth` (2,999 SAR/mo)

- Weekly proof events captured (target: ≥4/month, no minimum guarantee)
- Monthly bilingual case-safe report
- Quarterly QBR with founder

### If `recommended_offer = pilot_1sar` (1 SAR launch trial)

- Verifies the full Moyasar transaction loop
- Founder confirms receipt + 1 follow-up email within 24h
- No other deliverables (it's a transaction test by design)

---

## 4. Timeline (الجدول الزمني)

**Sprint (7 days):** kickoff → data → preview → drafts → handoff.
**Managed Ops:** month 1 founder-confirmed, auto-renew after 3
successful cycles (per `auto_client_acquisition.payment_ops.renewal_scheduler`).
**Custom AI:** scoped per engagement, never less than 4 weeks.

Founder is the **only** decision maker on approvals.

---

## 5. Investment (الاستثمار)

| Offer | Amount (SAR) | Type | VAT |
|-------|---------------|------|-----|
| Free Diagnostic | 0 | One-off | N/A |
| 1 SAR pilot | 1 | One-off | Included |
| Managed Sprint | 499 | One-off | Included (ZATCA receipt) |
| Starter (subscription) | 999/mo | Recurring | Included |
| Growth (subscription) | 2,999/mo | Recurring | Included |
| Scale (subscription) | 7,999/mo | Recurring | Included |
| Custom AI | 5,000–25,000 | Scoped | Included |

Payment via Moyasar (Mada / Visa / Mastercard / Apple Pay). ZATCA-
compliant receipts auto-generated.

---

## 6. Assumptions & limits (الافتراضات والحدود)

**AR:**
- بياناتكم تخضع لـ DPA الموقعة قبل الـ data ingest.
- كل outreach يمر بموافقتكم — لا autonomous send بأي حال.
- نسبة response هي signal، ليست ضمان (Doctrine #6).
- الـ refund: لو Sprint لم يكشف data أو فرص قابلة للقياس خلال ٧
  أيام، نعيد المبلغ كاملًا.

**EN:**
- Your data falls under the DPA signed before ingest.
- Every outreach passes your approval — no autonomous send ever.
- Response rate is a signal, not a guarantee (Doctrine #6).
- Refund: if the Sprint reveals no measurable data or opportunities
  within 7 days, full refund.

---

## 7. Approval & next step (الموافقة والخطوة التالية)

| Item | Customer signs | Dealix delivers |
|------|----------------|------------------|
| Proposal | {{customer_signature}} | {{founder_signature}} |
| DPA | {{customer_dpo_signature}} | {{dpa_url}} |
| Payment | Moyasar checkout link sent post-signature | ZATCA receipt within 24h |

**Validity:** This proposal is valid until {{valid_until}} (typically
14 days from issue).

**Next step:** reply with "approved" + signed DPA → Sprint kickoff
within 48h.

---

## Internal review checklist (founder, before sending)

- [ ] All Discovery numbers traced to proof_ledger (no fabrication)
- [ ] Recommended offer matches `auto_client_acquisition.offer_router` logic
- [ ] DPA URL points to the customer's industry-specific template
- [ ] Refund policy reviewed (must match `docs/contributing/REFUND_POLICY.md`)
- [ ] No promises about specific lead counts or revenue figures
- [ ] `proposal_id` recorded in approval_center
- [ ] Founder explicit approval before send
