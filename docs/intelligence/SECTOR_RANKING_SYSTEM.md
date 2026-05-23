# Sector Ranking System

> Ranks sectors weekly by a composite of fit, velocity, contract value, proof, and capacity.

## 1. Sectors tracked

1. ERP / CRM
2. Cybersecurity
3. B2B agencies
4. Logistics / industrial services
5. Consulting / digital transformation
6. SaaS / software
7. Enterprise services
8. Saudi high-ticket B2B providers

## 2. Composite score

| Factor | Weight | Source |
|---|---|---|
| Fit | 0.25 | ICP signal density |
| Velocity | 0.20 | Days lead → cash collected |
| Contract value (ARR) | 0.20 | Closed deals + Proposal Factory |
| Proof readiness | 0.15 | Approved proofs per sector |
| Capacity | 0.10 | Founder + delivery bandwidth |
| Strategic fit | 0.10 | Founder override |

Each factor normalised 0-1; composite reported 0-100.

## 3. Decision rules

| Composite | Action |
|---|---|
| ≥ 70 | Promote — increase distribution allocation |
| 50-69 | Hold — maintain current allocation |
| 30-49 | Watch — pause new acquisition, finish open deals |
| < 30 | Exit — stop new outreach; finish or refund existing |

Decisions are recommendations — final say is at `/approvals`.

## 4. Output

`growth/sector_targets.csv` columns:

```
sector_id, name_en, name_ar, composite, fit, velocity, arr, proof_ready, capacity, strategic, recommendation, source
```

## 5. Cadence

- Weekly recompute (Sunday 08:00 KSA).
- Monthly audit of weights.
- Quarterly sector list review.

## 6. Trust posture

Sector decisions never auto-pause outreach. Operator must confirm any "Exit" recommendation.
