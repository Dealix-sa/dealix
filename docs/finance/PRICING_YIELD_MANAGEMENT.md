# Pricing Yield Management

## Doctrine Anchor
- Non-negotiables touched: #2 (no value claim without source evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: offer architecture remains five doors with productized service ladders.

## Purpose

Optimize Dealix pricing based on demand, delivery effort, risk, and conversion. This document does **not** restate the price list — that lives in `docs/PRICING_STRATEGY.md` and `docs/OFFER_LADDER_AND_PRICING.md`. This document specifies the **weekly yield decision** that takes a price up, splits an offer, kills an offer, or routes demand to a retainer.

## Weekly Pricing Yield Review

Each week, for every active offer rung, review:

- Proposal-to-payment rate
- Average deal size
- Delivery hours per engagement
- Gross margin (after AI / tool costs)
- Retainer probability (was this engagement a one-off, or did it open recurring scope?)
- Discount impact (which discounts converted, which gave away margin)
- Bad-fit revenue (engagements that should not have been sold)

## Possible Decisions

For each rung:

- **Raise price** — high demand + constrained delivery capacity, or strong proof.
- **Reduce scope** — same price, less scope, faster delivery.
- **Split offer** — separate a popular sub-deliverable into its own rung.
- **Kill weak offer** — low conversion, low margin, not strategic.
- **Create premium tier** — a top-end SKU above the current ceiling.
- **Move to retainer** — convert successful one-off scope into recurring scope.

## Core Rules

- A pricing decision requires source-evidence: the conversion data, the delivery hours, the margin calc.
- No pricing exception below floor without founder approval and a recorded reason (see `docs/control_plane/APPROVAL_CENTER_V2.md` Pricing Exception Queue).
- A discount that converts is studied for repeatability before becoming a standing offer.
- A "bad-fit" engagement that already sold is delivered, then the offer or the qualification gate is fixed for next time.
- "If demand is high and delivery capacity is constrained, raise price before hiring."

## Connection to Doctrine and Existing Material

- Pricing strategy and price list: `docs/PRICING_STRATEGY.md`, `docs/OFFER_LADDER_AND_PRICING.md`.
- Unit economics (the inputs to yield decisions): `docs/UNIT_ECONOMICS_AND_MARGIN.md`, `docs/company/UNIT_ECONOMICS.md`.
- Offer architecture (the five doors): `docs/transformation/01_doctrine_lock.md`.

## Runtime Wiring

- Proposals (source of proposal-to-payment data): proposal worker + revenue events.
- Revenue events (source of conversion data): `auto_client_acquisition/revenue_memory/event_store.py`.
- Audit log (source of pricing exception data): `db/models.py::AuditLogRecord`.
- Pricing exception queue: `docs/control_plane/APPROVAL_CENTER_V2.md`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Proposal-to-payment rate per rung | tracked, experimented against | revenue events |
| Gross margin per rung after AI / tool cost | tracked, improving | unit economics |
| Pricing exceptions per week | tracked; root-cause investigated if rising | approval log |
| Offers killed per quarter | non-zero (a portfolio that never kills is not optimizing) | pricing decisions log |
| Conversions from a recorded discount | tracked, studied before repeating | revenue events |

## Cross-Links

- `docs/PRICING_STRATEGY.md`
- `docs/OFFER_LADDER_AND_PRICING.md`
- `docs/company/UNIT_ECONOMICS.md`
- `docs/UNIT_ECONOMICS_AND_MARGIN.md`
- `docs/finance/AI_UNIT_ECONOMICS.md`
- `docs/finance/BILLING_RECEIVABLES_OS.md`
- `docs/founder/REVENUE_WAR_ROOM_OS.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`

## Open Items

- A pricing decisions log file does not yet exist in `docs/finance/`.
- The link between a pricing exception in the Approval Center and the next-week yield review is informal.
- Margin-per-rung calculation depends on AI / tool cost-per-outcome data, which is partially wired (see `docs/finance/AI_UNIT_ECONOMICS.md`).
