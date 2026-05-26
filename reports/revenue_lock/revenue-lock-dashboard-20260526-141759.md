# Revenue Execution Lock Dashboard

Generated: 2026-05-26 14:17:59

## Next Action: CREATE_PAYMENT_REQUESTS

```powershell
For each qualified proposal: .\scripts\start_paid_delivery.ps1 -Client "Client Name" -Offer "ai-trust" -Amount "5000"
```

## Revenue

- Proposed / invoice pipeline: SAR 0.00
- Paid / collected / won: SAR 0.00
- Invoice/payment entries: 0
- Paid entries: 0

## Funnel

- Proposal / interested leads: 4
- Invoice / paid leads: 0
- Active deliveries: 1

## Lead Status Counts

| Status | Count |
|---|---:|
| contacted | 15 |
| proposal_sent | 3 |
| complete | 2 |
| call_booked | 1 |

## Proposal / Collection Candidates

| Company | Sector | Offer | Status | Suggested Move |
|---|---|---|---|---|
| Naqel Express | Logistics | delivery-accuracy | proposal_sent | create payment request |
| Al-Namaa Consulting | Consulting | ai-trust | proposal_sent | create payment request |
| Mena Ads | Marketing Agency | ai-trust | proposal_sent | create payment request |
| "Al-Majd Group" | Technology | ai-trust | call_booked | convert to proposal/payment |

## CEO Rule

No new build until every proposal_sent lead has either: payment request, follow-up, lost reason, or nurture status.