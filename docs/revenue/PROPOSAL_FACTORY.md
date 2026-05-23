# Proposal Factory

The Proposal Factory turns an accepted diagnostic into a signed scope of work. It is the most error-prone station in the Revenue Factory and therefore the most heavily gated.

**Source of truth:** `$PRIVATE_OPS/proposal_factory_state.csv`
**Owner:** Founder
**Trust gate:** A2 — every proposal sent externally requires founder approval. No automated send.

## Scope

A proposal is a fixed-scope, fixed-price commitment. It contains:

1. Engagement objective in one sentence.
2. Scope inclusions (bullet list).
3. Scope exclusions (bullet list, equal length).
4. Deliverables with definitions of done.
5. Timeline with named milestones.
6. Price with currency, VAT treatment, payment schedule.
7. Trust and data clauses referencing `docs/14_trust_os/`.
8. Acceptance criteria.

Bilingual EN + AR. Same length each section.

## Stages

| # | Stage | Output | Gate |
|---|-------|--------|------|
| 1 | Draft from template | Filled Jinja2 template | A0 |
| 2 | Pricing fit | Price within `docs/product/PRICING_GUARDRAILS.md` band | A1 |
| 3 | Legal pass | Trust clauses present | A1 |
| 4 | Founder review | Founder annotates | A2 |
| 5 | Send | Logged send event | A2 |
| 6 | Track | Reply state in factory | A0 |

## Templates

Reference templates live in `templates/PROPOSAL_*.md.j2`. Each carries the variables:

```
client_name, client_arabic_name, sector, sprint_type,
price_sar, payment_terms, start_date, end_date,
deliverables[], exclusions[], acceptance_criteria[]
```

Jinja2 strict mode is enforced — missing variables fail the render. This prevents "TBD" placeholders from leaving the building.

## No-guarantee rule

Proposals never include sentences such as "guaranteed revenue", "X meetings booked", or "Y% conversion". The Brand Guardian agent rejects drafts that contain these patterns (`docs/ai/BRAND_GUARDIAN_AGENT.md`). All forecasts are framed as "case-safe estimates based on prior pattern" with the disclaimer "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Pricing band

The Pricing Guardrails doc defines the published reference price for each rung of the offer ladder. Custom pricing (discount above 10%, scope expansion above 20%, payment-term extension beyond 60 days) requires explicit founder approval and a written justification logged in `$PRIVATE_OPS/pricing_exceptions.csv`.

## Failure modes

- **Scope drift:** the proposal adds work outside the engagement objective. Detection: founder review (stage 4). Recovery: split into two proposals or reject the addition.
- **Price below floor:** proposal price below the published floor. Detection: pricing gate (stage 2). Recovery: blocked; founder must explicitly approve.
- **Send without approval:** an agent attempts to send a proposal at A1. Detection: policy engine `policies/dealix_control_policy.yaml`. Recovery: send blocked, audit row written.

## Recovery path

If a proposal is sent in error (wrong client, wrong price, missing exclusion), the founder issues a written correction within 24 hours. The error and correction are logged in `$PRIVATE_OPS/proposal_corrections.csv`. The Proposal Factory state machine forces the opportunity back to stage 4 until re-approved.

## Metrics

- Proposals drafted this week.
- Proposals approved this week.
- Proposals sent this week.
- Proposal-to-close conversion (estimated).
- Median cycle time from diagnostic to sent proposal.

## Disclaimer

Pricing in any proposal is the floor for that engagement only. Published pricing is reference, not commitment. Dealix does not guarantee revenue. Estimated value is not Verified value.
