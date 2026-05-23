# Sector Performance

> Tracks reply, call, and close rates by sector (vertical) to inform ICP
> tuning.

## Format

| Sector | Leads | Replies | Reply Rate | Calls | Calls Rate | Proposals | Won | Close Rate | Avg Deal (SAR) | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|

## Sectors Tracked

- B2B services
- Logistics & supply chain
- Construction / FM
- Industrial / manufacturing
- Financial services (non-bank)
- Clinics & healthcare services
- Education / training
- Multi-branch retail

## ICP Promotion / Demotion Rule

- A sector promotes to **P0** if reply rate ≥ 15% and close rate ≥ 20% across at least 10 leads.
- A sector demotes to **P2** if reply rate < 5% across at least 30 leads.
- Movement requires a decision recorded in `DECISION_LOG.md`.

## Linked Files

- `docs/strategy/ICP_STRATEGY.md` — current ICP tiers.
- `docs/strategy/MARKET_MAP_SAUDI.md` — sector context.

## Cadence

- Updated monthly.
- Reviewed quarterly to update ICP tiers.
