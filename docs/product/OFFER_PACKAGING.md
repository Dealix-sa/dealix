# Offer Packaging

Offer packaging is the discipline of turning the Product Ladder rungs into specific, sellable engagements. A package is a named offer with fixed scope, fixed price, and clear deliverables.

**Source of truth:** `$PRIVATE_OPS/offer_packages.csv`
**Owner:** Founder + Revenue Lead
**Trust gate:** A2 — new packages and package retirement require founder approval.

## Package anatomy

Every package has:

| Field | Definition |
|-------|-----------|
| `package_id` | Stable identifier |
| `name_en` | English public name |
| `name_ar` | Arabic public name |
| `ladder_rung` | 1-7 per `docs/product/DEALIX_PRODUCT_LADDER.md` |
| `objective` | One sentence |
| `inclusions` | Bullet list |
| `exclusions` | Bullet list (equal length) |
| `deliverables` | Each with a definition of done |
| `timeline_weeks` | Numeric |
| `price_sar` | Published reference price |
| `payment_terms` | e.g. 50/50 or net-30 |
| `eligibility` | ICP criteria |
| `proof_anchors` | Links to case-safe summaries |
| `status` | draft / active / retired |

Packages live in source-controlled YAML and are mirrored to `$PRIVATE_OPS/offer_packages.csv` for reporting.

## Current packages (illustrative)

| ID | Name | Rung | Reference price |
|----|------|------|-----------------|
| `pkg.diag` | Sample Diagnostic | 1 | 0 |
| `pkg.sprint.factory_v1` | Revenue Sprint — Factory v1 | 2 | 19,500 SAR |
| `pkg.pilot.managed_v1` | Managed Pilot v1 | 3 | 49,500 SAR |
| `pkg.retainer.desk_v1` | Revenue Desk Retainer | 4 | 24,500 SAR / month |
| `pkg.console.founder_v1` | Founder Console | 5 | 9,500 SAR / month |
| `pkg.enterprise.os_v1` | Enterprise Revenue Intelligence OS | 6 | Custom |
| `pkg.partner.whitelabel_v1` | White-label Revenue OS | 7 | Custom |

## Package lifecycle

1. **Draft.** Founder defines the package against an existing rung. Brand Guardian reviews copy.
2. **Pilot.** Package is sold to no more than three clients to validate scope and pricing.
3. **Active.** Package is published in marketing artifacts.
4. **Iterate.** Pricing or scope adjustment goes through Change Request with founder approval.
5. **Retire.** Package is closed to new sales. Existing engagements continue to contract end.

A package is never both "active" and "in flux" in marketing. If scope is being revised, the package goes to status `revision` and is removed from public listing.

## Exclusions discipline

Every package's exclusion list is at least as long as its inclusion list. This forces the package to be a knife, not a sponge. Exclusions prevent scope drift (`docs/delivery/SCOPE_CONTROL.md`).

## Failure modes

- **Sponge package:** a package without exclusions absorbs unrelated work. Detection: monthly review. Recovery: rewrite with explicit exclusions.
- **Ghost package:** a package is listed externally but missing from source-controlled YAML. Detection: weekly diff. Recovery: pull listing or re-create source.
- **Conflicting prices:** the same package appears at different prices across artifacts. Detection: copy audit. Recovery: align to source YAML; correct artifacts.

## Recovery path

If packaging becomes inconsistent across collateral, the founder freezes new proposals until the packages are realigned and re-published.

## Metrics

- Active package count.
- Sales by package per quarter.
- Median proposal cycle time by package.
- Margin by package (verified).

## Disclaimer

Published packages are reference. Specific engagements run on signed proposals. Dealix does not guarantee revenue. Estimated value is not Verified value.
