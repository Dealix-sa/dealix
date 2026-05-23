# Dealix Market Attack & Scaling System

> Layer 3 of the Dealix operating stack. Sits on top of Company OS (Layer 1)
> and the Launch Command Layer (Layer 2). Turns "launch-ready" into
> "market-attacking, sector-focused, learning, and scaling".

## 1. Why this layer exists

After Company OS is built and the Launch Command Layer is wired, Dealix is
still not yet *attacking* the market. It is only ready. This layer adds
the discipline of:

1. **Choosing one beachhead sector** at a time.
2. **Testing offer-market fit** with structured experiments.
3. **Generating demand** through proof-safe campaigns.
4. **Running a Strategic Account List** instead of scattering effort.
5. **Building a founder-led Authority Engine** so trust precedes outreach.
6. **Operating a Conversion Command Room** to watch the funnel daily.
7. **Applying Scale / Fix / Kill rules** every week.
8. **Feeding a Market Learning Memory** so every experiment compounds.

## 2. Non-negotiables (inherited)

This layer never bypasses Dealix doctrine:

1. No external sending without founder approval.
2. No proof publishing without proof-pack validation.
3. No secrets in repo.
4. No guaranteed revenue / sales / meetings claims.
5. No pricing, contract, refund, or payment commitments outside the
   approved offer ladder.
6. No automation that bypasses approval / trust / audit.
7. Preserve existing architecture (Company OS, Launch Layer).
8. Every machine has: docs, owner, source of truth, KPI, risk, verifier.

## 3. The 12 sub-systems

| #   | System                          | Owner             | Source of truth                                          |
| --- | ------------------------------- | ----------------- | -------------------------------------------------------- |
| 01  | First Beachhead Sector          | Founder           | `market_attack/beachhead_sector_scorecard.csv`           |
| 02  | Offer-Market Fit Test           | Founder + Sales   | `market_attack/offer_market_fit_tests.csv`               |
| 03  | Demand Creation Campaigns       | Marketing         | `campaigns/campaign_registry.csv` + `campaign_queue.csv` |
| 04  | Strategic Account List          | Sales             | `market_attack/strategic_accounts.csv`                   |
| 05  | Proof-Safe Sales Assets         | Sales + Brand     | `sales_assets/sales_asset_registry.csv`                  |
| 06  | Founder-Led Authority Engine    | Founder           | `authority/founder_posts.csv` + `authority/content_angles.csv` |
| 07  | Multi-Channel Distribution Plan | Marketing         | `campaigns/campaign_queue.csv`                           |
| 08  | Partner Attack Plan             | BD / Founder      | `partners/partner_pipeline.csv`                          |
| 09  | Objection Intelligence          | Sales             | `market_attack/objection_library.csv`                    |
| 10  | Conversion Command Room         | Founder           | `campaigns/campaign_results.csv`                         |
| 11  | Scale / Fix / Kill System       | Founder           | derived: scorecards + results                            |
| 12  | Market Learning Memory          | Founder           | derived: postmortems + learnings                         |

## 4. Daily / weekly cadence

**Daily:**

```bash
make ceo-daily-brief          PRIVATE_OPS=/opt/dealix-ops-private
make revenue-forecast         PRIVATE_OPS=/opt/dealix-ops-private
make beachhead-scorecard      PRIVATE_OPS=/opt/dealix-ops-private
```

**Weekly:**

```bash
make weekly-growth-review     PRIVATE_OPS=/opt/dealix-ops-private
make offer-market-fit         PRIVATE_OPS=/opt/dealix-ops-private
make objection-intel          PRIVATE_OPS=/opt/dealix-ops-private
make campaign-command         PRIVATE_OPS=/opt/dealix-ops-private
```

**Decision rules (Scale / Fix / Kill):** see
`SCALE_FIX_KILL_SYSTEM.md` for the exact thresholds.

## 5. Layers above and below

```
Level 1 — Company OS           (all systems exist)
Level 2 — Launch Layer         (everything is ready to go live)
Level 3 — Market Attack Layer  (focused, measured offensive)  ← this file
Level 4 — Scaling Layer        (scale/fix/kill + learning loop)
```

## 6. Risks and what stops them

| Risk                              | Mitigation                                              |
| --------------------------------- | ------------------------------------------------------- |
| Scattering across many sectors    | Beachhead scorecard forces one priority sector          |
| Vanity demand creation            | Campaign results must include positive_replies + proposals + payments |
| Selling on promises               | Proof-safe asset policy; "no guaranteed revenue" linter |
| Outreach burnout / spammy motion  | Approval-class on each campaign asset                   |
| Forgetting what worked            | Market Learning Memory + campaign postmortems           |
| Partner channel cannibalization   | Partner referral terms guardrails                       |

## 7. Verifier

```bash
make market-attack-system
```

runs `scripts/verify_market_attack_system.py`, which checks:

- docs presence
- CSV bootstrap headers
- scripts exist and are runnable
- Makefile targets exist
- frontend pages exist (if `apps/web` is present)
- no "guaranteed" language in customer-facing markdown
