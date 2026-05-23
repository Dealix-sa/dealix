# Pricing Guardrails

Pricing is one of the protected founder decisions. The Pricing Guardrails define what is automatic, what is reviewable, and what is prohibited.

**Source of truth:** `$PRIVATE_OPS/pricing_guardrails.csv`
**Owner:** Founder
**Trust gate:** A2 — all pricing changes require explicit founder approval.

## Three classes of pricing decision

| Class | Definition | Authority |
|-------|-----------|-----------|
| Reference | Published price for a package | Founder, monthly |
| Custom | A specific engagement deviates from reference | Founder, per proposal |
| Exception | A specific engagement deviates from custom band | Founder, with written justification |

Reference prices are listed in `docs/product/DEALIX_PRODUCT_LADDER.md`. They are signals, not contracts.

## Custom-pricing band

A custom price is permitted within ±10% of the reference. Any deviation beyond the band is an Exception.

| Direction | Band | Beyond band |
|-----------|------|-------------|
| Discount | up to 10% | Exception required |
| Premium | up to 10% | Exception required (rare) |
| Payment-term extension | up to net-45 | Exception required (rare) |
| Scope expansion | up to +20% | Exception required |

## Exception process

1. Revenue Lead documents the exception: client, package, proposed price, justification, expected return.
2. Brand Guardian and CS Lead are consulted.
3. Founder reviews and either approves, modifies, or declines.
4. Approved exceptions are logged in `$PRIVATE_OPS/pricing_exceptions.csv` with `expires_at`.
5. Exceptions are reviewed monthly; if a pattern emerges, the reference price is reviewed.

## Prohibited pricing decisions

| Decision | Reason |
|----------|--------|
| Discount in exchange for testimonial | Conflicts with consent integrity (`docs/proof/PROOF_APPROVAL_OS.md`) |
| Discount tied to a referral commitment | Conflicts with `docs/customer_success/REFERRAL_SYSTEM.md` |
| Bundled price below the sum of floor prices | Margin breach |
| "Pay if it works" without contract clauses | Implicit guarantee, prohibited |
| Discount on enterprise without security review | Risk transfer to delivery |

These prohibited decisions are blocked by `policies/dealix_control_policy.yaml`.

## Disclosure

Reference prices are public on the marketing site. Custom prices and exceptions are confidential to the client and Dealix. Aggregated pricing patterns may be published as a sector report with no client identifiable.

## Failure modes

- **Silent custom price:** a proposal is sent below reference without a recorded exception. Detection: weekly pricing audit. Recovery: convert to logged exception or re-issue at reference.
- **Stale reference:** the published price is below the floor implied by current margin (`docs/finance/AI_UNIT_ECONOMICS_SYSTEM.md`). Detection: monthly margin review. Recovery: founder revises reference.
- **Exception sprawl:** more than 30% of proposals in a quarter use exceptions. Detection: quarterly review. Recovery: reference price is wrong; revise.

## Recovery path

If pricing governance is in doubt, the founder freezes new proposals until reference and exceptions are reconciled.

## Metrics

- Exceptions per quarter by class.
- Median discount granted (estimated).
- Exception conversion rate (closed-won vs all exceptions).
- Margin per engagement (verified).

## Disclaimer

Published pricing is reference. Custom pricing requires founder approval. Dealix does not guarantee revenue. Estimated value is not Verified value.
