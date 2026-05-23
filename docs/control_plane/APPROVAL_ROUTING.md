# Approval Routing

Every action is routed to one of four approval levels.

| Level | Meaning |
|---|---|
| `A0` | Automatic internal — system executes without review |
| `A1` | Review recommended — AI drafts, human edits before use |
| `A2` | Explicit human approval required before external execution |
| `A3` | Never auto-execute — founder-only |

## Default Routes

| Action | Level |
|---|---|
| `lead_scoring` | A0 |
| `crm_update` | A0 |
| `lead_enrichment` | A0 |
| `message_draft` | A1 |
| `first_outbound` | A1 |
| `followup_outbound` | A1 |
| `proposal_draft` | A2 |
| `proposal_send` | A2 |
| `payment_terms_change` | A2 |
| `public_content_publish` | A2 |
| `public_compliance_claim` | A2 |
| `contract_change` | A3 |
| `nda_sign` | A3 |
| `refund` | A3 |
| `sensitive_data_export` | A3 |
| `regulator_communication` | A3 |
| `guaranteed_revenue_claim` | A3 |
| `full_compliance_claim` | A3 |

## Default for Unknown Actions

Unknown actions are routed to `A2` — never `A0`. The router fails closed.

## Customization

Pass an override dict to `ApprovalRouter(routes=...)` to extend or replace
the default mapping. New actions should be added to this document and to
`DEFAULT_ROUTES` in the same change.
