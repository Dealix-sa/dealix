# Revenue Factory OS

The set of machines that take an **approved-to-pursue** account from
the distribution layer all the way to a **signed scope, captured
payment, kicked-off delivery, and shipped proof**.

## 1. Stations on the line

| # | Station | Output | Owner |
|---|---|---|---|
| 1 | Lead Intelligence | A scored, evidence-backed account view. | growth_strategist |
| 2 | Lead Scoring | A 0-100 score with tier label. | account_scoring_machine |
| 3 | Approval Queue | Founder-approved drafts and decisions. | approvals_os |
| 4 | Sample Factory | Diagnostic / sample artifacts on demand. | offer_architect |
| 5 | Proposal Factory | Scoped proposals from a template. | offer_architect |
| 6 | Payment Capture | ZATCA-compliant invoice + capture record. | finance_copilot |
| 7 | Delivery Trigger | Project kicked off + Day-1 pack. | delivery_copilot |
| 8 | Retention | Health scoring + renewal motion. | delivery_copilot |
| 9 | Referral Ask | Structured referral request post-success. | growth_strategist |
| 10 | Proof Approval | Consented case study + proof pack. | content_strategist |

## 2. Hand-off contracts (mandatory)

Each station has a strict input / output contract. A station refuses
to run when its input is missing fields. Stations never call each
other directly — they read and write through ledgers.

## 3. Trust gate per station

| Station | Approval required for |
|---|---|
| Lead Intelligence | None (read-only). |
| Lead Scoring | None (writes to ledger). |
| Approval Queue | The action itself is the approval. |
| Sample Factory | Each sample is approved before release. |
| Proposal Factory | Founder signs the scope and pricing. |
| Payment Capture | Founder confirms invoice (and ZATCA fields). |
| Delivery Trigger | Founder confirms kick-off and owner. |
| Retention | Founder reviews health & renewal decisions. |
| Referral Ask | Founder approves the ask draft. |
| Proof Approval | Customer consent recorded; founder reviews. |

## 4. Ledgers

- `revenue/lead_intelligence.csv`
- `revenue/sample_releases.csv`
- `revenue/proposal_register.csv`
- `revenue/payment_register.csv`
- `revenue/delivery_register.csv`
- `revenue/retention_register.csv`
- `revenue/referral_register.csv`
- `revenue/proof_register.csv`

## 5. KPIs

- Time from approved draft → meeting booked.
- Time from meeting → proposal sent.
- Time from proposal → payment captured.
- Time from payment → delivery kick-off.
- Time from kick-off → first proof artifact.

## 6. Banned patterns

- ❌ Auto-issuing invoices.
- ❌ Auto-capturing payment from a saved instrument without consent.
- ❌ Auto-promising delivery dates.
- ❌ Auto-publishing proof.
