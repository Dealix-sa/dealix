# Dealix Revenue Factory

The five-rung revenue ladder, wired to delivery + governance.

## The five rungs

| Rung | Offer | Price (SAR) | Engine |
|---|---|---|---|
| 0 | Free AI Ops Diagnostic | 0 | `dealix/business_now/` |
| 1 | 7-Day Revenue Intelligence Sprint | 499 | `scripts/run_dealix_daily_ops.py` |
| 2 | Data-to-Revenue Pack | 1,500 | `dealix/revenue_ops_autopilot/` |
| 3 | Managed Revenue Ops Retainer | 2,999–4,999/mo | `dealix/revenue_ops_autopilot/` |
| 4 | Custom AI Service Setup | 5,000–25,000 + 1,000/mo | `dealix/execution/` |
| Enterprise | AI Governance Review | 25,000–50,000 | `dealix/governance/` |

## Forecast generator

`make revenue-forecast` runs `scripts/generate_revenue_forecast.py` to
emit `data/revenue_forecast/<YYYY-MM>.md`. It models:

- Top-of-funnel diagnostics shipped (input).
- Conversion to Sprint (default 30%).
- Sprint -> Retainer conversion (default 25%).
- Retainer net-retention (default 0.9 monthly).

Forecast horizon: 6 months rolling.

## Conversion gates

Every rung transition is gated by:
- Proof Pack score >= 70 from the previous rung.
- Capital Asset registered (>= 1 per engagement).
- Approval recorded for the upsell offer.

## Sales motion

- Outreach drafts produced by `dealix-sales` agent.
- All sends route through approval_center.
- No cold WhatsApp / LinkedIn — drafts only.

## Doctrine notes

- NN10: no project without Proof Pack -> blocks invoicing.
- NN11: no project without Capital Asset -> blocks retainer renewal.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
