# Growth OS

Revenue Marketing + Marketing Attribution + Revenue Assurance + Revenue Proof + Stream Optimization for Dealix.

This module implements sections 32–50 of the commercial spec. It is metadata + pure-function only:

- No external sends (no email, no WhatsApp, no LinkedIn).
- No scraping.
- All "agents" are metadata descriptors. Drafts produced by the engine are surfaced through the API but never auto-sent.
- All revenue is rejected unless backed by a hard verification (payment / signed agreement / invoice / retainer / partner paid).

## Layout

| Subpackage         | Purpose |
| ------------------ | ------- |
| `icp/`             | ICP matrix (7 profiles) + fit scoring |
| `abm/`             | Account-Based Marketing pipeline + metadata agent roster |
| `geo/`             | Generative Engine Optimization blueprint + page registry + checker |
| `content_engine/`  | Content types, Content-to-Cash CTA map, 9 marketing operating rules |
| `revenue_proof/`   | RevenueRecord + statuses + `is_real_revenue` doctrine |
| `revenue_assurance/` | Verification bundle, quality score, margin/effort/retainer checks |
| `attribution/`     | Attribution types + grouping by channel/offer/campaign/asset/agent/partner |
| `experiments/`     | ExperimentCard + scale/iterate/kill decision engine |
| `dashboard/`       | Growth snapshot metrics + 7 red-flag detectors |
| `streams/`         | 25+ stream cards in 5 buckets + scale/optimize/reprice decisions |
| `funnels/`         | Revenue Hunter / AI Trust Kit / Agency White-label funnels |
| `partners/`        | Partner motion stages + per-partner metrics |
| `case_studies/`    | Before/Action/Output/Outcome/Learning/Next template |
| `brand/`           | Hero line + 4 audience messages (AR + EN) |
| `operating_rules.py` | Re-exports rules + `enforce_all(batch)` helper |

## API

All endpoints are mounted under `/api/v1/growth-os/` (see `api/routers/growth_os_revenue.py`). The endpoints are read-only or pure-computation; none perform external sends.

## Verify

```bash
bash scripts/growth_os_master_verify.sh
```
