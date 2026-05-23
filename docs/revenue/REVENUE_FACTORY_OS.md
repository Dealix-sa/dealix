# Revenue Factory Operating System

> One factory, six stations. From signal to cash to proof to referral.

## 1. Stations

```
Lead Intelligence → Score → Approve → Draft → Send (manual)
       → Reply → Sample → Proposal → Payment → Delivery
       → Retention → Proof → Referral
```

Each station ships a machine, a queue, an owner, and a KPI.

## 2. Station map

| Station | Owner | Machine | KPI |
|---|---|---|---|
| Lead Intelligence | Growth Strategist | Market Domination Intelligence | Coverage of Tier-1 ICP |
| Score | Growth Strategist | Account Scoring Model | Scoring stability |
| Approve | Founder | `/approvals` | Latency ≤ 24h |
| Draft | Distribution Operator | Outbound Draft + Email Draft | Brand-pass rate |
| Send | Founder / operator | Manual | — |
| Reply | Distribution Operator | Reply Router | Routing precision |
| Sample | Delivery Copilot | Sample Factory | Time-to-sample, brand-pass |
| Proposal | Sales (founder-led) | Proposal Factory | Conversion to paid |
| Payment | Finance Copilot | Payment Capture OS | Days to cash |
| Delivery | Delivery Copilot | Delivery QA OS | QA-pass rate, NPS |
| Retention | Retention Copilot | Retention OS | Renewal rate, expansion |
| Proof | Brand Guardian + Founder | Proof Approval OS | Consent-gated proof rate |
| Referral | Distribution Operator | Partner / Referral Machine | Referrals per healthy customer |

## 3. Hand-offs

Every hand-off creates an event in the audit log with:

- Source station
- Target station
- Artifact reference
- Trust checks at hand-off

## 4. Trust contract

- No station performs external action without approval.
- Suppression, brand, trust checks reapplied at each station.
- Audit log is the source of truth for what happened.

## 5. Failure handling

If any station's KPI degrades two weeks in a row, the Performance Improvement OS triggers a review surfaced on the daily brief.
