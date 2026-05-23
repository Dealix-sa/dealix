# Dealix Company OS Scorecard

## Purpose
Track readiness and operating quality for each Dealix company system.

## Owner
Sami / Founder CEO.

## Review Cadence
Weekly.

## Inputs
- Verification scripts.
- GitHub Actions status.
- Private ops evidence.
- Revenue metrics.
- Delivery metrics.
- Trust logs.

## Outputs
- System score.
- PASS / READY INTERNAL / FIX / BLOCKED status.
- Next action per system.

## Rules
- 90-100 = PASS.
- 75-89 = READY INTERNAL.
- 50-74 = FIX.
- 0-49 = BLOCKED.
- No system is PASS without evidence.

## Metrics
- Number of PASS systems.
- Number of blocked systems.
- Time since last review.
- Evidence completeness.

## Evidence
- scripts/verify_company_os_deep.py
- scripts/verify_full_ops.py
- GitHub Actions
- private ops logs

| System | Score | Status | Evidence | Verification | Next Action |
|---|---:|---|---|---|---|
| Founder OS | 0 | BLOCKED | docs/founder/ | scripts/verify_founder_os.py | Use daily brief |
| Strategy OS | 0 | BLOCKED | docs/strategy/ | scripts/verify_strategy_os.py | Lock 90-day plan |
| Revenue OS | 0 | BLOCKED | docs/revenue/ | scripts/verify_revenue_os.py | Send 25 DMs |
| Acquisition OS | 0 | BLOCKED | docs/acquisition/ | scripts/verify_acquisition_os.py | Define sourcing |
| Sales OS | 0 | BLOCKED | docs/sales/ | scripts/verify_sales_os.py | Define sales motion |
| Delivery OS | 0 | BLOCKED | docs/delivery/ | scripts/verify_delivery_os.py | Prepare 3 samples |
| Trust OS | 0 | BLOCKED | docs/trust/ | scripts/verify_trust_os.py | Enforce approvals |
| Finance OS | 0 | BLOCKED | docs/finance/ | scripts/verify_finance_os.py | Verify payment path |
| Client Success OS | 0 | BLOCKED | docs/client_success/ | scripts/verify_client_success_os.py | Define retention |
| Product OS | 0 | BLOCKED | docs/product/ | scripts/verify_product_os.py | Tie features to revenue |
| Content OS | 0 | BLOCKED | docs/content/ | scripts/verify_content_os.py | Build proof engine |
| Learning OS | 0 | BLOCKED | docs/learning/ | scripts/verify_learning_os.py | Write first review |

## Last Reviewed
YYYY-MM-DD
