# Proposal Factory | مصنع المقترحات

## Purpose | الغرض
Convert a qualified, sample-validated opportunity into a clear, founder-approved
proposal document. Proposals are drafted by the system, edited by the founder,
and only ever leave the queue after explicit founder approval.

Proposals contain pricing and terms — therefore this is the most tightly gated
factory in Dealix.

## Inputs | المدخلات
- Reply Router intent: "wants proposal" OR Sample feedback positive
- Full account dossier
- Buyer's stated scope (extracted from reply transcripts)
- Pricing & packaging catalog (internal)
- Standard contract template
- Delivery capacity check (can Dealix actually deliver this scope now?)

## Outputs | المخرجات
- `proposals.documents`: proposal_id, account_id, buyer_id, scope_summary,
  price, terms_pointer, state, drafted_at, approved_at, sent_at, response_state
- A buyer-ready proposal (PDF) + cover note
- Linked invoice template (sent only after proposal acceptance)

## Proposal structure | بنية المقترح
1. Restate buyer's situation and goal (in their language)
2. Scope: what Dealix will do (clear, bounded)
3. What Dealix will NOT do (out of scope)
4. Timeline and milestones
5. Investment: price, payment schedule, payment terms
6. Trust pack: PDPL stance, security posture, references (anonymized OK)
7. Acceptance: how to accept (signed document or PO)

## Pricing rules | قواعد التسعير
- Always reference the published packaging catalog
- Custom pricing requires founder-explicit approval (no AI auto-pricing)
- Discounts require founder explicit note
- Multi-currency: KSA default SAR; USD allowed for cross-border with founder note

## Scope safety | سلامة النطاق
- Scope must match Dealix's current delivery capacity (Delivery OS capacity check)
- Out-of-scope section is mandatory
- Change-request mechanism referenced explicitly

## Data source | مصدر البيانات
`proposals.documents`, `pricing.catalog`, `contracts.templates`,
`delivery.capacity`.

## Approval class | فئة الموافقة
- A1: drafting structure, pulling boilerplate
- A2: every proposal requires founder approval before send
- A3: any proposal with custom pricing, non-standard terms, regulated buyer, or
  scope outside delivery capacity

## Trust gate | بوابة الثقة
- Pricing matches catalog or has founder note
- No revenue/outcome guarantees written into scope
- Standard contract template referenced explicitly
- Delivery capacity verified at draft time
- Policy snapshot + audit row per proposal version

## Owner | المالك
Founder approves every proposal. No exceptions.

## Worker name
`revenue.proposal_factory`

## KPI | المؤشرات
- Median time: request → proposal sent (target ≤ 5 business days)
- Proposal → accepted rate
- Proposal → paid rate
- Discount frequency (should remain modest and tracked)
- Out-of-capacity-rejection rate (should be near zero)

## Failure mode | حالات الفشل
- Auto-generated pricing slips past founder review
- Scope exceeds delivery capacity
- Proposal references stale references or expired terms

## Recovery path | مسار الاسترداد
- Pricing field locked until founder explicitly confirms
- Delivery capacity check is a hard gate, blocks send
- Reference freshness check at draft time; expired references stripped
