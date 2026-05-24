# Proposal Factory

> Assembles proposals from the product ladder, pricing guardrails, and customer signal.

## 1. Inputs

- Customer brief (intake form + sales notes).
- Selected offer rung from `docs/product/DEALIX_PRODUCT_LADDER.md`.
- Pricing guardrails (`docs/product/PRICING_GUARDRAILS.md`).
- Relevant proof (from Proof Approval OS).
- Engagement plan template (per rung).

## 2. Output

A bilingual proposal document with:

1. Cover (customer name, prepared-on, prepared-by).
2. The shape of the engagement (rung-specific).
3. Deliverables and timeline.
4. Operating cadence.
5. Trust + security posture.
6. Pricing within guardrails.
7. Acceptance section (no e-signature inside Dealix; founder uses contracted method).

## 3. Trust rules

- Never include a guaranteed-result claim.
- Never include another customer's logo without consent.
- Never commit to terms (refund, discount, custom SLA) that violate guardrails — the proposal goes to `/approvals` for founder review of guardrail variances.
- Pricing fields in the proposal are filled by the founder, not the agent.

## 4. Production

- Drafted by Sales agent (founder-led motion).
- Brand Guardian validates copy and visual conformance.
- Stored in `clients/<customer>/proposals/`.

## 5. KPI

| KPI | Target |
|---|---|
| Time to first draft | ≤ 24 h after qualified call |
| Conversion to paid | tracked by sector |
| Win cycle days | tracked weekly |
