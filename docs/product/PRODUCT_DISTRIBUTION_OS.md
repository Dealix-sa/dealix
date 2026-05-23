# Product Distribution OS

How each rung of the product ladder gets in front of the right
audience — through the distribution war machine, never through cold,
ungated automation.

## 1. Rung-to-channel map

| Rung | Primary channels | Secondary |
|---|---|---|
| Free Sample / Diagnostic | Founder warm intro, contact-form queue. | LinkedIn draft. |
| Revenue Sprint | Sample-to-Sprint draft, partner referral. | Email draft. |
| Managed Pilot | Proposal factory after a sprint. | ABM playbook. |
| Revenue Desk Retainer | Renewal motion + proof-to-demand. | Founder-led intro. |
| Founder Console | Annualised plan with the existing retainer cohort. | Partner referral. |
| Enterprise Revenue OS | ABM machine + executive briefings. | Sector pulse + intro. |
| Partner Revenue OS | Direct partner program. | Co-brand sector pulse. |

## 2. Routing rules

- Every channel routes drafts to the approval queue.
- A single account never appears in > 1 outbound queue / week.
- A retained customer is excluded from outbound queues automatically.
- Proof-to-demand drafts only target look-alikes of consented proof.

## 3. Distribution events

`product/product_distribution.csv`:
```
account_id,rung_offered,channel,draft_id,status,
approval_at,sent_at,reply_at,next_action,note
```

## 4. KPIs

- Rung exposure per quarter.
- Approval throughput per rung.
- Rung-to-rung promotion rate.
- Conversion by channel × rung.

## 5. Banned patterns

- ❌ Cold-blasting a rung announcement to a purchased list.
- ❌ Offering a rung outside the pricing guardrails.
- ❌ Dual-targeting one account on multiple channels in the same week.
