# ROI Measurement

Dealix measures ROI in cash, not pipeline. We use two layers: **verified
revenue** and **multi-layer attribution**.

## Verified revenue

A revenue event is only counted if it satisfies all of:

- `amount_sar > 0`
- `source` in `{payment_received, signed_agreement, retainer_active, partner_paid_customer}`
- `status` in `{paid, retainer_active, expanded, renewed}`
- `evidence_ref` set (invoice, contract scan, or transaction id)

Enforced in
[`dealix/hermes/money/verified_revenue.py`](../../dealix/hermes/money/verified_revenue.py).

## Revenue quality

Each verified-revenue event is scored 0–100 against:

| Weight | Driver |
| --- | --- |
| 25 | Gross margin |
| 20 | Retainer potential |
| 15 | Repeatability |
| 10 | Data moat |
| 10 | Partner potential |
| 10 | Low delivery burden |
| -15 | Risk |
| -15 | Founder time dependency |

Bands: `kill` < 30, `caution` < 50, `good` < 70, `great` < 85,
`exceptional` ≥ 85. Implementation:
[`dealix/hermes/money/revenue_quality.py`](../../dealix/hermes/money/revenue_quality.py).

## Multi-layer attribution

Every verified-revenue event carries attribution across eight layers
([`dealix/hermes/growth/attribution/`](../../dealix/hermes/growth/attribution/)):

```json
{
  "verified_revenue_sar": 25000,
  "channel": "direct_outreach",
  "campaign": "ai_trust_kit_saudi_b2b",
  "message_variant": "executive_control_angle",
  "asset": "ai_governance_checklist",
  "agent": "proposal_factory",
  "partner": null,
  "geo_surface": "answer_engine_page_001",
  "trust_signal": "evidence_pack_sample",
  "confidence": 0.78
}
```

Confidence is the simple mean of the per-layer confidences. The
dashboard surfaces both the headline number and the lowest-confidence
layer so it is obvious which signal is weakest.

## Founder time cost

Hours that consume the founder without producing an asset or a
retainer are tagged "unproductive" and surfaced separately. See
[`dealix/hermes/sovereignty/founder_time.py`](../../dealix/hermes/sovereignty/founder_time.py).
