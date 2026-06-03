# Approval Matrix V2

## Purpose
Who can approve what, at what threshold.

## Matrix

| Action | Threshold | Approver | Logged in |
|---|---|---|---|
| Add public claim about a customer | Any | Founder + named customer | `trust/approval_log.csv` |
| Discount > 20% | Any | Founder | `finance/discount_log.csv` |
| Spend (non-standard category) | > 1,000 SAR | Founder | `finance/expenses.csv` |
| Spend (standard) | > 5,000 SAR | Founder | `finance/expenses.csv` |
| Contractor onboarding (production access) | Any | Founder | `people/access_log.csv` |
| Refund | Any | Founder | `trust/approval_log.csv` |
| Data export to external service | Any with customer data | Founder | `trust/approval_log.csv` |
| AI-generated external content | Any | Founder review | `trust/claim_review_log.csv` |
| New retainer beyond 12 months | Any | Founder | `trust/approval_log.csv` |

## Approval workflow
1. **Request** — proposer records the request with `decision=Pending`.
2. **Review** — approver reviews. If more info is needed, status remains Pending until provided.
3. **Decide** — approver sets Approved or Rejected with timestamp.
4. **Execute** — action proceeds only after Approved.

## Out-of-band approval
If something happens before the approval can be recorded (e.g., an emergency rotation of a leaked secret), record the approval within 24 hours with explanation.

## Future state
- When team > 1, the matrix splits: contractor approvals → founder, founder approvals → external advisor.
