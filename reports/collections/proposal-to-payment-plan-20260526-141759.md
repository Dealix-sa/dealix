# Proposal to Payment Plan

Generated: 2026-05-26 14:17:59

## Objective

Convert proposal/interested leads into payment requests or clear lost/nurture reasons.

| Company | Status | Offer | Amount | Action | Command |
|---|---|---|---:|---|---|
| Naqel Express | proposal_sent | delivery-accuracy | 5000 | Start paid delivery / payment request | `.\scripts\start_paid_delivery.ps1 -Client "Naqel Express" -Offer "delivery-accuracy" -Amount "5000"` |
| Al-Namaa Consulting | proposal_sent | ai-trust | 5000 | Start paid delivery / payment request | `.\scripts\start_paid_delivery.ps1 -Client "Al-Namaa Consulting" -Offer "ai-trust" -Amount "5000"` |
| Mena Ads | proposal_sent | ai-trust | 5000 | Start paid delivery / payment request | `.\scripts\start_paid_delivery.ps1 -Client "Mena Ads" -Offer "ai-trust" -Amount "5000"` |
| "Al-Majd Group" | call_booked | ai-trust | 5000 | Generate proposal first | `py -3 .\scripts\proposal_from_lead.py ""Al-Majd Group""` |

## Founder Rule

Do not create more new leads until these proposal/interested leads are moved forward or closed.