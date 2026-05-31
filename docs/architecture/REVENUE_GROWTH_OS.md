# Revenue Growth OS

The Revenue Growth OS is the loop:

```
Market Signal → ICP → Pain → Offer → Message → Channel
              → Lead → Call → Proposal → Revenue
              → Outcome → Learning → Better Campaign
```

Three modules co-own it: `growth/`, `money/`, `products/`.

## Growth (`dealix/hermes/growth/`)

| Module | Purpose |
|---|---|
| `campaigns.py` | every campaign declares ICP × offer × channel; no offer → `ValueError` |
| `leads.py` | every lead carries source, campaign, ICP, fit score, pain hypothesis |
| `icp.py` | the ICP library |
| `audiences.py` | targetable segments from ICPs |
| `messages.py` | drafts staged for approval |
| `content.py` | editorial calendar with `backlog → published` state |
| `landing_pages.py` | drafts; `publish()` requires approval |
| `experiments.py` | every experiment has hypothesis, metric, success threshold, kill rule |
| `funnels.py` | stage counts + conversion ratios |
| `attribution.py` | re-exports money attribution |
| `revenue_quality.py` | per-campaign quality score |
| `partner_marketing.py` | co-marketing ledger |
| `retention.py` | cohort retention |
| `geo.py` | the GEO landing-page configurations |

GEO surfaces called out in the spec:
- `/ai-governance-saudi-companies`
- `/agentic-control-plane`
- `/ai-revenue-hunter`
- `/agency-ai-white-label`
- `/mcp-risk-review`

## Money (`dealix/hermes/money/`)

- `dashboard.py` — Sami's primary money view (fastest cash, highest deal, etc.)
- `revenue_streams.py` — typed streams: sprint, data_pack, managed_ops, custom_ai, partner_share, training, report, marketplace, api
- `revenue_assurance.py` — `verify` requires payment + invoice; quality score formula:
  ```
  0.25 margin + 0.20 repeatability + 0.20 retainer
  + 0.15 moat + 0.10 partner - 0.10 delivery_burden
  ```
- `attribution.py` — links revenue to campaign, lead, offer, partner, channel
- `pricing_intelligence.py` — floor/target/ceiling bands
- `cashflow.py` — daily brief with risk flag
- `deal_room.py` — per-deal context room
- `invoice_tracking.py` — open / sent / paid / overdue

## Products (`dealix/hermes/products/`)

Offer library defaults to three productized offers:
- **Revenue Hunter Pilot** (4,999 SAR / 14 days)
- **AI Trust Kit** (24,999 SAR / 30 days)
- **Agency White-label Kit** (49,999 SAR / 60 days)

Every offer must pass `check_readiness` (buyer / pain / promise /
deliverables / price / timeline / metric / cta) before it ships.

`scale_kill.py` evaluates each offer against revenue × paid-customer
thresholds.
