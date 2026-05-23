# Dealix Company OS Scorecard

## Scoring Rules

| Score | Status | Meaning |
|---:|---|---|
| 90–100 | PASS | Ready and verified |
| 75–89 | READY INTERNAL | Usable internally |
| 50–74 | FIX | Needs work |
| 0–49 | BLOCKED | Not ready |

## Systems

| System | Score | Status | Evidence | Verification | Next Action |
|---|---:|---|---|---|---|
| Founder OS | 0 | BLOCKED | docs/founder/ | scripts/verify_founder_os.py | Create CEO docs |
| Strategy OS | 0 | BLOCKED | docs/strategy/ | scripts/verify_strategy_os.py | Create strategy docs |
| Revenue OS | 0 | BLOCKED | docs/revenue/ | scripts/verify_revenue_os.py | Define funnel |
| Acquisition OS | 0 | BLOCKED | docs/acquisition/ | scripts/verify_acquisition_os.py | Define sourcing |
| Sales OS | 0 | BLOCKED | docs/sales/ | scripts/verify_sales_os.py | Define sales motion |
| Delivery OS | 0 | BLOCKED | docs/delivery/ | scripts/verify_delivery_os.py | Lock playbooks |
| Trust OS | 0 | BLOCKED | docs/trust/ | scripts/verify_trust_os.py | Expand governance |
| Finance OS | 0 | BLOCKED | docs/finance/ | scripts/verify_finance_os.py | Define cash rules |
| Client Success OS | 0 | BLOCKED | docs/client_success/ | scripts/verify_client_success_os.py | Define retention |
| Product OS | 0 | BLOCKED | docs/product/ | scripts/verify_product_os.py | Define roadmap rules |
| Content OS | 0 | BLOCKED | docs/content/ | scripts/verify_content_os.py | Define authority engine |
| Learning OS | 0 | BLOCKED | docs/learning/ | scripts/verify_learning_os.py | Define feedback loops |
| Agents OS | 0 | BLOCKED | docs/agents/ | scripts/verify_agents_os.py | Define registry/evals |
| Control Plane | 0 | BLOCKED | control_plane/ | scripts/verify_company_os.py | Build state + brief |

## Aggregate

Company OS Aggregate = average of system scores.
PASS threshold: 90.
READY INTERNAL threshold: 75.
Below 75 = Dealix is files, not a company.

## Update Cadence

- Daily: not required.
- Weekly: refreshed during Weekly CEO Review.
- Monthly: archived snapshot in `docs/learning/MONTHLY_STRATEGY_UPDATE.md`.
