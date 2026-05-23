# Dealix Product Ladder

Seven rungs from free diagnostic to white-label OS. Each rung has a single objective, a published reference price, and a clear next-rung path. Custom pricing requires founder approval (`docs/product/PRICING_GUARDRAILS.md`).

**Source of truth:** `$PRIVATE_OPS/product_ladder_state.csv`
**Owner:** Founder
**Trust gate:** A2 — pricing, packaging, and ladder changes require founder approval.

## The ladder

| Rung | Offer | Reference price (SAR) | Term | Outcome |
|------|-------|----------------------|------|---------|
| 1 | Free Sample / Diagnostic | 0 | 1 week | Sector-specific diagnostic |
| 2 | Revenue Sprint | 19,500 | 4 weeks | Reproducible factory station |
| 3 | Managed Pilot | 49,500 | 12 weeks | Two factory stations live |
| 4 | Revenue Desk Retainer | 24,500 / month | 6 months min | Steady-state Revenue Factory |
| 5 | Founder Console / Command Center | 9,500 / month | 12 months min | Founder-grade dashboard + audit |
| 6 | Enterprise Revenue Intelligence OS | Custom | 24 months min | Org-wide deployment with SLAs |
| 7 | Partner / White-label Revenue OS | Custom | 36 months min | Partner distribution rights |

Published prices are reference. They are not commitments. A specific engagement is priced in a written proposal (`docs/revenue/PROPOSAL_FACTORY.md`).

## Rung 1: Free Sample / Diagnostic

Three-page bilingual diagnostic produced by the Sample Factory (`docs/revenue/SAMPLE_FACTORY.md`). Free to qualified prospects. Bounded scope, no commitment. Output is a case-safe sector diagnostic with three observed patterns, one diagnostic question, and a recommended next step.

## Rung 2: Revenue Sprint

Four-week, fixed-scope engagement that stands up one Revenue Factory station with measurable throughput. Sprint scope and outputs are defined in `docs/03_commercial_mvp/SPRINT_SCOPE.md` and `docs/03_commercial_mvp/SPRINT_OUTPUTS.md`.

## Rung 3: Managed Pilot

Twelve weeks, two stations live, with a defined transition plan to the Retainer. The pilot is a paid proof of fit, not a guarantee of revenue.

## Rung 4: Revenue Desk Retainer

Monthly retainer running the active Revenue Factory stations on the client's behalf. Minimum six months. Renewal review at month five.

## Rung 5: Founder Console / Command Center

Monthly subscription to the founder dashboard, audit trail, and weekly executive digest. Often layered with Rung 4. Standalone available for founders running their own ops.

## Rung 6: Enterprise Revenue Intelligence OS

Multi-team deployment with SLAs, named CSM, dedicated eval cadence, and custom integrations. Requires security and procurement review on the client side. Two-year minimum because the deployment is non-trivial.

## Rung 7: Partner / White-label Revenue OS

For consultancies and integrators reselling Dealix under their own brand. Includes a partner contract, training, and revenue share. Three-year minimum.

## Upgrade path

The natural path is 1 → 2 → 3 → 4 → 5, with 6 and 7 as parallel tracks for organisations of scale. Skipping rungs is permitted but each skip is logged in `product_ladder_state.csv` with reason.

## Failure modes

- **Rung mismatch:** a client is sold Rung 4 without passing Rung 2 or Rung 3. Detection: monthly review. Recovery: revisit fit; downgrade if necessary.
- **Hidden discount:** a Rung 2 sold below the published floor without founder approval. Detection: pricing audit. Recovery: cancel or re-approve.
- **Scope drift across rungs:** Rung 4 work expands into Rung 6 territory without re-pricing. Detection: QA layer. Recovery: Change Request and re-price.

## Recovery path

If the ladder loses internal consistency (overlapping scopes, contradictory prices), the founder freezes new proposals until the ladder is realigned and re-published.

## Metrics

- Active engagements by rung.
- Upgrade rate from rung N to rung N+1 (estimated).
- Median engagement duration by rung.
- Margin by rung (verified).

## Disclaimer

Published prices are reference. Custom pricing requires founder approval. Dealix does not guarantee revenue or upgrade outcomes. Estimated value is not Verified value.
