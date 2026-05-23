# Proposal Factory

How Dealix turns an approved meeting into a scoped, signable
proposal — branded, bilingual, audit-ready.

## 1. Proposal templates

| Template | For | Branding |
|---|---|---|
| `t-diagnostic` | Free diagnostic engagement. | Cover with full lockup. |
| `t-revenue-sprint` | 30-day revenue sprint. | Cover + sector eyebrow. |
| `t-managed-pilot` | 90-day managed pilot. | Cover + ZATCA fields. |
| `t-revenue-desk-retainer` | Monthly retainer. | Cover + monthly cycle. |
| `t-founder-console` | Annual platform. | Cover + governance schedule. |
| `t-enterprise-revenue-os` | Multi-BU rollout. | Cover + control plane appendix. |
| `t-partner-white-label` | Partner / agency reseller. | Cover + co-brand block. |

## 2. Inputs

- Account intelligence and scoring.
- Conversation notes from the founder.
- Pricing guardrails (`docs/product/PRICING_GUARDRAILS.md`).
- Brand templates.

## 3. Outputs

- PDF proposal (bilingual AR + EN).
- Row in `revenue/proposal_register.csv`:
  ```
  proposal_id,account_id,template_id,scope_summary,
  price_band,terms_summary,founder_signed,
  pdf_url,sent_at,status
  ```

## 4. Trust gate

- Pricing comes only from the guardrails table — no improvised numbers.
- Scope statements are reviewed by the founder before "send".
- No "guaranteed" language anywhere in the proposal.
- ZATCA-required fields are populated for any tax-bearing proposal.

## 5. KPIs

- Proposals issued per week.
- Sign rate per template.
- Time from meeting → proposal sent.
- Time from proposal sent → signed.

## 6. Banned patterns

- ❌ Auto-sending proposals to email lists.
- ❌ Pricing outside the guardrails table.
- ❌ Guarantees or promised KPIs.
- ❌ One-side contracts; the customer always gets the bilingual draft.
